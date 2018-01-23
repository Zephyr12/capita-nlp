import threading

Message = dict

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

    def queue(self, item):
        threading.Thread(target=lambda: self.writer(item)).start()

if __name__ == "__main__":
    src = Source([
                Processor(
                        [Writer(lambda x: print("WRITTEN", x))],
                        lambda x: [x * x])],
                lambda: range(100000)
            )
