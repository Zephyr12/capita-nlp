import tweepy
import uuid
import datetime
import queue
import nltk
import models
import nlp
import pipes
import nltk.corpus
import datetime
import random
import conf

class TweetStreamerSource(tweepy.StreamListener):
    
    def __init__(self, terms=conf.twitter_followed_schools, num_days=conf.twitter_update_rate):
        self.buffer = queue.Queue()
        self.terms = terms
        self.num_days = num_days

    def on_status(self, status):
        self.buffer.put({
                "raw_text": status.text,
                "id": hash(datetime.datetime.now())
            })

    def __iter__(self):
        return self

    def __next__(self):
        return self.buffer.get()

    def __call__(self):
        self.auth = tweepy.OAuthHandler("TWg3Ywvoa1xzvEim97ww3Roxm", "CBW1yVZwizeTqW2u1UHD1BWuYLjJejptwdiApydAOJs7RUX2kq")
        self.auth.set_access_token("4273627119-IUdTBDAT4YnWxJ6ND2MilBK7fTQ5tGQNjTM5cVX", "LeTYK0GZoIQNdp8HRKsaYbsDtST3psdLpCTSebThV5D8i")
        self.api = tweepy.API(
                self.auth,
                wait_on_rate_limit=True
                )
        for term in self.terms:
            page = 1
            
            for result in tweepy.Cursor(
                    self.api.search,
                    since=datetime.datetime.now().date() - datetime.timedelta(days=self.num_days),
                    q=term + " -filter:retweets", 
                    tweet_mode='extended',
                    lang="en").items(10000):
                yield {
                        "id": uuid.uuid4().int,
                        "raw_text": result.full_text,
                        "concerns": term,
                        "timestamp": result.created_at
                   }
        #
        #self.stream = tweepy.Stream(self.api.auth, self)
        #print(self.terms)
        #self.stream.filter(track=self.terms, languages=["en"], async=True)
        #return self
