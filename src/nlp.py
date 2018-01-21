from nltk.sentiment.vader import SentimentIntensityAnalyzer
from difflib import SequenceMatcher
import nltk
import re

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

def fuzz(msg):
    return " ?".join(".?".join(c + "?" if i not in (0, len(w)-1) else c for i, c in enumerate(w)) for w in nltk.word_tokenize(msg))

class fuzzy_classifier:

    def __init__(self, classifications):
        self.classes = [(cls, re.compile(fuzz(cls), flags=re.IGNORECASE)) for cls in classifications]

    def __call__(self, msg):
        print(fuzz(msg["raw_text"]))
        best_phrase = max(self.classes, key=lambda cls: SequenceMatcher(None, "".join(re.findall(cls[1], msg["raw_text"])), cls[0]).ratio())
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
    source = sources.TweetStreamerSource()
    sentiment_analyser = pipes.Processor(sentiment())
    ner = pipes.Processor(ner_classifier(["School", "Work", "Other BS"]))
    sink = pipes.Sink(lambda x: print(x))

    source.add_out_pipe(sentiment_analyser)
    sentiment_analyser.add_out_pipe(ner)
    ner.add_out_pipe(sink)
    source.run().join()
