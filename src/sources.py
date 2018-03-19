import tweepy
import queue
import nltk
import models
import nlp
import pipes
import nltk.corpus
import datetime


class TweetStreamerSource(tweepy.StreamListener):
    
    def __init__(self, terms):
        self.buffer = queue.Queue()
        self.terms = terms

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
        self.api = tweepy.API(self.auth)
        self.stream = tweepy.Stream(self.api.auth, self)
        print(self.terms)
        self.stream.filter(track=self.terms, async=True)
        return self
