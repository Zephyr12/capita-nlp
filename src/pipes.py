import threading
import fb
import nlp
#from src.db import MyDB
from db import MyDB

Message = dict

#class BufferedIterator():

class Source:
    '''
    A node that produces a stream of objects
    '''

    def __init__(self, sinks, source):
        '''
        :param sinks: A list of nodes that the output of this source needs to be sent to
        :param source: A function that returns an iterable of objects
        '''
        self.source = source
        self.processors = sinks
        thread = threading.Thread(target=lambda: self.start())
        thread.start()
    
    def start(self):
        for item in self.source():
            for processor in self.processors:
                processor.queue(item)

class Processor:
    '''
    A node that performs an operation on a stream of objects
    '''

    def __init__(self, sinks, process):
        '''
        :param sinks: A list of nodes that the output of this processor needs
        to be sent to

        :param process: A function takes an object and returns an iterable of
        objects this describes the operator that the processor node defines
        '''
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
    '''
    A node that fuses two or more streams of objects
    '''

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
    '''
    A node that consumes a stream of objects
    '''

    def __init__(self, writer):
        '''
        :param writer: A function takes an object and consumes it not passing it on any further
        '''
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


