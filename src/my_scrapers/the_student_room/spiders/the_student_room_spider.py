"""
This script scrapes the www.thestudentroom.co.uk forum for all the posts related to universities.
"""

import pdb
import uuid
from twisted.internet import reactor
import datetime
import scrapy
import logging
from scrapy.crawler import CrawlerProcess, Crawler, CrawlerRunner
from scrapy.settings import Settings
import queue
import re
import json
import threading

class TheStudentRoom(scrapy.Spider):
    name = "student_room"
    custom_settings = {
           "LOG_LEVEL": logging.ERROR,
           "ITEM_PIPLINES": {__name__+".TSRSource": 1}
            }
    #First three subforums include 'Find your flatmates' threads at the end of universities list. Hence, we count them in order to be eliminated.
    subforums_counter = 0
    
    def __init__(self, allowed_schools={}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buffer = queue.Queue()
        self.allowed_schools = allowed_schools

    def __iter__(self):
        return self

    def __next__(self):
        try:
            item = self.buffer.get(timeout=5)
            self.buffer.task_done()
            return item
        except queue.Empty:
            raise StopIteration()

    def start_requests(self):
        url = 'https://www.thestudentroom.co.uk/forumdisplay.php?f=307'
        yield scrapy.Request(url=url, callback=self.parse)

    #Some of the thread names amongst universities are not relevent for our search, thus we avoid scraping them.
    mismatched_universities = ['International Postgraduate Study',
                               'Humanitas University',
                               'Masdar Institute',
                               'TSR International Freshers blogs',
                               'Studying in North America',
                               'Studying in Australia',
                               'Studying in the Netherlands',
                               '[Archived]Studying abroad - Your questions answered',
                               'North of England',
                               'Midlands',
                               'South of England',
                               'Greater London',
                               'Scotland',
                               'Wales',
                               'Northern Ireland',
                               'Distance Learning',
                               'International Study']

    def parse(self, response):
        """ This function parses a sample response. Some contracts are mingled
            with this docstring.

            This function is the FIRST LEVEL PARSE, which follows all university
            related threads.

            @url https://www.thestudentroom.co.uk/forumdisplay.php?f=307
            @returns items 0
        """

        forums = response.css('.forum-category .forum .info')
        forums.pop(0)
        for subforum_page in forums:
            universities = subforum_page.css('td a')
            if self.subforums_counter < 3 :
                universities = universities[:-1] #Pops 'Find your flatmates' subforum.
                self.subforums_counter += 1
            for university in universities:
                university_name = university.css('a::text').extract_first()
                university_name = university_name.replace("\n", "").replace("  ","")
                university_url = 'https://www.thestudentroom.co.uk/' + \
                                 university.css('a::attr(href)').extract_first()
                if university_name in self.allowed_schools:
                    request = response.follow(university_url, self.parse2)
                    #Stores the university name in the meta of the yielded request, in order to identify every post to its concerned university.
                    request.meta["concerns"] = self.allowed_schools[university_name]
                    yield request

    def parse2(self, response):
        """ This function parses a sample response. Some contracts are mingled
            with this docstring.

            This is the SECOND LEVEL PARSE, which is called for every university
            thread. For every university thread, it follows all the topics, and
            also calls back the same function on the next page of topics
            is existent.

            @url https://www.thestudentroom.co.uk/forumdisplay.php?f=55
            @returns items 0

            @url https://www.thestudentroom.co.uk/forumdisplay.php?f=845
            @returns items 0

            @url https://www.thestudentroom.co.uk/forumdisplay.php?f=58
            @returns items 0

            @url https://www.thestudentroom.co.uk/forumdisplay.php?f=158
            @returns items 0

            @url https://www.thestudentroom.co.uk/forumdisplay.php?f=21
            @returns items 0
        """
        #Pagination in university threads
        try:
            next_page = response.css('ul.pager .pager-ff::attr(href)').extract_first()
            next_page_url = 'https://www.thestudentroom.co.uk/' + next_page
            request = response.follow(next_page_url, self.parse2)
            request.meta["concerns"] = response.meta.get('concerns')
            yield request
        except TypeError:
            #Thread does not have more pages
            pass

        #Moving forward to each thread on the page
        for thread_line in response.css('body .thread '):
            for thread in thread_line.css('td a'):
                thread_name = thread.css('a::text').extract_first()
                thread_url = 'https://www.thestudentroom.co.uk/' + \
                             thread.css('a::attr(href)').extract_first()
                request = response.follow(thread_url, self.parse3)
                request.meta["concerns"] = response.meta.get('concerns')
                yield request


    def parse3(self, response):
        """ This function parses a sample response. Some contracts are mingled
            with this docstring.

            This is the THIRD and LAST LEVEL PARSE that extracts all the posts
            present in a topic, and also repeats the procedure for every next
            page if existent.

            This function yields the desired results: raw_text post together
            with the university name that it relates to.

            @url https://www.thestudentroom.co.uk/showthread.php?t=5152190
            @returns items 1
            @scrapes concerns raw_text

            @url https://www.thestudentroom.co.uk/showthread.php?t=4922988
            @returns items 1
            @scrapes concerns raw_text

            @url https://www.thestudentroom.co.uk/showthread.php?t=4961436
            @returns items 1
            @scrapes concerns raw_text

            @url https://www.thestudentroom.co.uk/showthread.php?t=5030830
            @returns items 1
            @scrapes concerns raw_text

            @url https://www.thestudentroom.co.uk/showthread.php?t=2008015
            @returns items 1
            @scrapes concerns raw_text

            @url https://www.thestudentroom.co.uk/showthread.php?t=5129204
            @returns items 1
            @scrapes concerns raw_text
        """
        #Pagination to move to next page of each topic.
        try:
            next_page = response.css('ul.pager .pager-ff::attr(href)').extract_first()
            next_page_url = 'https://www.thestudentroom.co.uk/' + next_page
            request = response.follow(next_page_url, self.parse3)
            request.meta["concerns"] = response.meta.get('concerns')
            yield request
        except TypeError:
            #Topic does not have more pages.
            pass

        #Yielding each post from the current page.
        for post in response.css(".post"):#('.post-content .postcontent'):
            timestamp = datetime.datetime.strptime(" ".join(post.css(".date-full .datestamp::text").extract() +  post.css(".date-full .timestamp::text").extract()), "%d-%m-%Y %H:%M")
            post_text = post.css('.post-content .postcontent').css('.restore::text').extract()
            encoded_post = "".join(post_text)
            result = dict()
            result["timestamp"] = timestamp
            result['concerns'] = response.meta.get('concerns')
            result['raw_text'] = encoded_post
            result["id"] = uuid.uuid4().int
            self.buffer.put({**result})
            
            yield result


def tsr_source(allowed):
    def src():
        tsr = TheStudentRoom
        crawler_process = Crawler(tsr, Settings())
        crawler_process.crawl(allowed_schools=allowed)
        
        tp = reactor.getThreadPool()
        tp.adjustPoolsize(maxthreads=4)
        threading.Thread(target=lambda: reactor.run(installSignalHandlers=False)).start()
     
        #threading.Thread(target=crawler_process.start).start()

        for x in crawler_process.spider:#.crawlers.__iter__().__next__().spider:
            yield x
    return src

if __name__ == "__main__":
    pass
