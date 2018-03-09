import tweepy
import queue
import nltk
from . import models, nlp, pipes
import nltk.corpus
import datetime

class S:
    def __init__(self, t):
        self.text = t

net = nltk.corpus.wordnet

class TweetStreamerSource(tweepy.StreamListener):
    
    def __init__(self):
        self.buffer = queue.Queue()

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
        '''
        self.stream.filter(track= [" ".join(lemma2.lower().split("_"))
            for syn in net.synsets("educational_institution")
            for hypo in syn.hyponyms()
            for lemma in hypo.lemma_names()
            for syn2 in net.synsets(lemma)
            for hypo2 in syn2.hyponyms()
            for lemma2 in hypo2.lemma_names()])
        '''
        self.stream.filter(follow=["4273627119"], async=True)
        return self
