from nltk.sentiment.vader import SentimentIntensityAnalyzer
from difflib import SequenceMatcher
import nltk

import models
import pipes
import sources


class sentiment:
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()


    def __call__(self, msg):
        augment = {
                "sentiment": self.sid.polarity_scores(msg["raw_text"])["compound"]
                }
        return [{**msg, **augment}]

class ner_classifier:
    def __init__(self, classifications):
        self.classes = classifications
        self.grammar = "NP: {<DT>?<JJ.*>*<NN.*>+}"
        self.parser  = nltk.RegexpParser(self.grammar)


    def __call__(self, msg):
        noun_phrases = [" ".join(l[0] for l in s.leaves()) for s in self.parser.parse(nltk.pos_tag(nltk.word_tokenize(msg["raw_text"]))).subtrees() if s.label() == "NP"]
        best_phrase  = max(self.classes, key=lambda cls: sum(SequenceMatcher(None, np.lower(), cls.lower()).ratio() for np in noun_phrases))

        augment = {
                "school_id": best_phrase
                }
        return [{**msg, **augment}]


def topic_model(db):
    pass
