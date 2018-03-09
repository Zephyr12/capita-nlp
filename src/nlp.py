from nltk.sentiment.vader import SentimentIntensityAnalyzer
from difflib import SequenceMatcher
import nltk
import re

from . import models, pipes, sources


class sentiment:
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()


    def __call__(self, msg):
        augment = {
                "sentiment": self.sid.polarity_scores(msg["raw_text"])["compound"]
                }
        return [{**msg, **augment}]

def fuzz(msg):
    fuzz = " ?".join("(?:" + ".?".join(c + "?" if i not in (0, len(w)-1) else c for i, c in enumerate(w)) + ")?" for w in nltk.word_tokenize(msg) )
    print(fuzz)
    return fuzz

def initialize(string):
    return "".join(word[0] for (word, pos) in nltk.pos_tag(nltk.word_tokenize(string)) if pos[:2] == "NN" and word[0] != '\'')

def initials_match(needle, haystack):
    return 1 if initialize(needle) in haystack else 0

def evaluate(cls, msg):
    found_text = "".join(re.findall(cls[1], msg["raw_text"]))
    ratio_score = SequenceMatcher(None, found_text, cls[0]).ratio() 
    initials_score = initials_match(cls[0], msg["raw_text"])
    if (initials_score > 0):
        print("RATIO_SCORE:", ratio_score)
        print("INITALS_SCORE:", initials_score)
        print("FOR:", cls)
        print("WITH:", found_text)
        print()
    return ratio_score + initials_score

class fuzzy_classifier:

    def __init__(self, classifications):
        self.classes = [(cls, re.compile(fuzz(cls), flags=re.IGNORECASE)) for cls in classifications]

    def __call__(self, msg):
        best_phrase = max(self.classes, key=lambda cls: evaluate(cls, msg))
        augment = {
                "concerns": best_phrase[0]
                }
        return [{**msg, **augment}]

class ner_classifier:
    def __init__(self, classifications):
        self.classes = classifications
        #self.parser  = nltk.RegexpParser(self.grammar)


    def __call__(self, msg):
        ner_chunked_data = nltk.ne_chunk(nltk.pos_tag(msg["raw_text"].split()), binary=True)
        print(ner_chunked_data)
        noun_phrases = [" ".join(l[0] for l in s.leaves()) for s in ner_chunked_data.subtrees() if s.label() == "NE"]
        print(noun_phrases)
        best_phrase  = max(self.classes, key=lambda cls: sum(SequenceMatcher(None, np.lower(), cls.lower()).ratio() for np in noun_phrases))
        print(sum(SequenceMatcher(None, np.lower(), best_phrase.lower()).ratio() for np in noun_phrases))

        augment = {
                "concerns": best_phrase
                }
        return [{**msg, **augment}]


if __name__ == "__main__":
    for item in models.get_school_list():
        print(item, " => ", initialize(item))
