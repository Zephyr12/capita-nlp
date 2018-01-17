import threading

Message = dict

class Node:
    def __init__(self, operation):
        self.out_pipes = []
        self.operation = operation
    
    def add_out_pipe(self, pipe):
        self.out_pipes.append(pipe)

    def process(self, msg):
        results = self.operation(msg)
        for result in results:
            for pipe in self.out_pipes:
                pipe.process(result)

class Source(Node):
    
    def run(self):
        t = threading.Thread(target=lambda: self.process(None))
        t.daemon = False
        t.start()
        return t

class Sink(Node):
    pass

class Merge(Node):
    
    def __init__(self, join_key, is_complete):
        super().__init__(lambda x: x)
        self.join_key = join_key
        self.is_complete = is_complete
        self.cached = {}

    def process(self, msg):
        key = self.join_key(msg)
        if key in self.cached:
            self.cached[key].update(msg)
            if self.is_complete(self.cached[key]):
                cached = self.cached[key]
                del self.cached[key]
                super().process([cached])
        else:
            self.cached[key] = msg


class Processor(Node):
    pass
