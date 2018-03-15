import scrapy
import re
import json


class TheStudentRoom(scrapy.Spider):
    name = "student_room"
    #First three subforums include 'Find your flatmates' forum together with only universities.
    subforums_counter = 0

    def start_requests(self):
        url = 'https://www.thestudentroom.co.uk/forumdisplay.php?f=307'
        yield scrapy.Request(url=url, callback=self.parse)

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
                if university_name not in self.mismatched_universities:
                    request = response.follow(university_url, self.parse2)
                    request.meta["concerns"] = university_name
                    yield request

    def parse2(self, response):
        """ This function parses a sample response. Some contracts are mingled
            with this docstring.

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

        #Printing each post from the current page.
        with open("the_student_room_posts.txt", "a") as myfile:
            for post in response.css('.post-content .postcontent'):
                post_text = post.css('.restore::text').extract()
                print("---------------------------------------")
                encoded_post = [x.encode('utf-8') for x in post_text]
                encoded_post = "".join(encoded_post)
                #print(response.meta["concerns"])
                result = dict()
                result['concerns'] = response.meta.get('concerns')
                result['raw_text'] = encoded_post
                yield result
                # yield {"concerns:":response.meta.get('concerns'),
                #        "raw_text:":encoded_post}




