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

class Join:

    def __init__(self, sinks, key_func, count=2):
        self.key_func = key_func
        self.buffer = {}
        self.sinks = sinks
        self.count = count
    
    def dispatch(self, item):
        print(item)
        for sink in self.sinks:
            sink.queue({k: v for d in item for k, v in d.items()})

    def queue(self, item):
        if self.key_func(item) in self.buffer: 
            self.buffer[self.key_func(item)].append(item)
            if len(self.buffer[self.key_func(item)]) == self.count:
                threading.Thread(target=lambda: self.dispatch(self.buffer[self.key_func(item)])).start()
        else:
            self.buffer[self.key_func(item)] = [item]

class Writer:

    def __init__(self, writer):
        self.writer = writer

    def queue(self, item):
        threading.Thread(target=lambda: self.writer(item)).start()

if __name__ == "__main__":
    writer = Writer(print)
    
    join   = Join([writer], lambda d: d["id"])

    sqr    = Processor([join], lambda d: [{"squared": d["value"] ** 2, **d}])
    dbl    = Processor([join], lambda d: [{"doubled": [d["value"], d["value"]], **d}])

    src    = Source(
            [sqr, dbl],
            lambda: [{
                    "id": id,
                    "value": value
                } for id, value in enumerate([2,3,5,7,11,13,17])])


