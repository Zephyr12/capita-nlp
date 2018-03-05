import tweepy
import nltk
import models
import nltk.corpus
import nlp
import datetime
import pipes

# class S:
#     def __init__(self, t):
#         self.text = t
# 
# net = nltk.corpus.wordnet
# 
# class TweetStreamerSource(pipes.Source):#, tweepy.StreamListener):
#     
#     def __init__(self):
#         #super(TweetStreamerSource, self).__init__(self)
#         self.s = nlp.sentiment()
#         self.n = nlp.ner_classifier(models.get_school_list())
# 
#     def on_status(self, status):
#         print(self.n(self.s({
#                 "raw_text": status.text,
#                 "id": hash(datetime.datetime.now())
#             })[0])[0])
# 
#     def __call__(self, x):
#         self.auth = tweepy.OAuthHandler("TWg3Ywvoa1xzvEim97ww3Roxm", "CBW1yVZwizeTqW2u1UHD1BWuYLjJejptwdiApydAOJs7RUX2kq")
#         self.auth.set_access_token("4273627119-IUdTBDAT4YnWxJ6ND2MilBK7fTQ5tGQNjTM5cVX", "LeTYK0GZoIQNdp8HRKsaYbsDtST3psdLpCTSebThV5D8i")
#         self.api = tweepy.API(self.auth)
#         self.stream = tweepy.Stream(self.api.auth, self)
#         '''
#         self.stream.filter(track= [" ".join(lemma2.lower().split("_"))
#             for syn in net.synsets("educational_institution")
#             for hypo in syn.hyponyms()
#             for lemma in hypo.lemma_names()
#             for syn2 in net.synsets(lemma)
#             for hypo2 in syn2.hyponyms()
#             for lemma2 in hypo2.lemma_names()])
#         '''
#         self.stream.filter(follow=["4273627119"], async=True)
# 
# if __name__ == "__main__":
#     ts = TweetStreamerSource()
#     ts(None)
#     while True:
#         ts.on_status(S(input(">> ")))
