from nltk.sentiment.vader import SentimentIntensityAnalyzer
from difflib import SequenceMatcher
import nltk
import re

import models
import pipes
import sources


class sentiment:
    '''
    A callable object that computes the sentiment of any document and returns that updates that document's sentiment.
    Used as a Processor callable
    '''
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()


    def __call__(self, msg):
        augment = {
                "sentiment": self.sid.polarity_scores(msg["raw_text"])["compound"]
                }
        return [{**msg, **augment}]

def fuzz(msg):
    fuzz = " ?".join("(?:" + ".?".join(c + "?" if i not in (0, len(w)-1) else c for i, c in enumerate(w)) + ")?" for w in nltk.word_tokenize(msg) )
    return fuzz

def initialize(string):
    return "".join(word[0] for word in nltk.word_tokenize(string) if word[0] != '\'')

def initials_match(needle, haystack):
    return 1 if initialize(needle) in nltk.word_tokenize(haystack) else 0

def evaluate(cls, msg):
    found_text = "".join(re.findall(cls[1], msg["raw_text"]))
    ratio_score = SequenceMatcher(None, found_text, cls[0]).ratio() 
    initials_score = initials_match(cls[0], msg["raw_text"]) * 10
    return ratio_score + initials_score

class fuzzy_classifier:
    '''
        A fuzzy regexp based classifier that tries to recognize named entities from it's list of possible classifications.
    '''

    def __init__(self, classifications):
        self.classes = [(cls, re.compile(fuzz(cls), flags=re.IGNORECASE)) for cls in classifications]

    def __call__(self, msg):
        best_phrase = max(self.classes, key=lambda cls: evaluate(cls, msg))
        augment = {
                "concerns": best_phrase[0]
                }
        return [{**msg, **augment}]
