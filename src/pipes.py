import threading
import fb
import nlp
#from src.db import MyDB
from db import MyDB

Message = dict

#class BufferedIterator():

class Source:

    def __init__(self, sinks, source):
        self.source = source
        self.processors = sinks
        thread = threading.Thread(target=lambda: self.start())
        thread.start()
    
    def start(self):
        for item in self.source():
            for processor in self.processors:
                processor.queue(item)

class Processor:

    def __init__(self, sinks, process):
        self.process = process
        self.todo = []
        self.sinks = sinks

    def dispatch(self, item):
        for output in self.process(item):
            for sink in self.sinks:
                sink.queue(output)


    def queue(self, item):
        threading.Thread(target=lambda: self.dispatch(item)).start()

class Writer:

    def __init__(self, writer):
        self.writer = writer
        #self.mydb1 = MyDB

    def queue(self, item):
        threading.Thread(target=lambda: self.writer(item)).start()

if __name__ == "__main__":
    db = MyDB("dbname=capita user=amartya password=test")
    db.create_table('reviews', {'raw_text': 'text', 'concern_id': 'integer', 'sentiment': 'real', 'concerns': 'text'})
    src = Source([
                    Processor(
                            [Writer(lambda x: db.add_row("reviews", x))],
                            lambda x: [x, x])],
                    lambda: [{"raw_text": "this works", "concern_id": 1, "sentiment": 1.4782374, "concerns": "UCL"}]
                )
