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
