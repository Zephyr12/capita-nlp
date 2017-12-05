from nltk.sentiment.vader import SentimentIntensityAnalyzer
from difflib import SequenceMatcher
import nltk


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
        best_phrase  = max(self.classes, key=lambda cls: sum(SequenceMatcher(None, np, cls).ratio() for np in noun_phrases))


        augment = {
                "concerns": best_phrase
                }
        return [{**msg, **augment}]


if __name__ == "__main__":
    import pipes
    source = pipes.Source(lambda x: [
        {"id": 1, "raw_text": "School is bad"},
        {"id": 2, "raw_text": "Work is good"},
        {"id": 3, "raw_text": "Hillside School is not bad"},
        {"id": 4, "raw_text": "Other BS is not very good"}
        ])
    sentiment_analyser = pipes.Processor(sentiment())
    ner = pipes.Processor(ner_classifier(["School", "Work", "Other BS"]))
    sink = pipes.Sink(lambda x: print(x))
    join = pipes.Merge(lambda s: s["id"], lambda s: len(s) == 4)

    source.add_out_pipe(sentiment_analyser)
    source.add_out_pipe(ner)
    sentiment_analyser.add_out_pipe(join)
    ner.add_out_pipe(join)
    join.add_out_pipe(sink)
    source.run()
