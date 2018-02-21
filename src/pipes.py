import threading

from src.db import MyDB

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
    db = MyDB("dbname=ana9712 user=ana9712 password=test")
    # db.create_table("schools", {"id": "int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY", "URN": "integer", "establishment_number": "integer", "establishment_name": "text", "postcode": "text", "type_of_establishment": "text", "phase_of_education": "text" })
    # db.create_table("post", {"post_id": "int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY", "timestamp": "date", "raw_text": "text", "sentiment": "integer NOT NULL", "school_id": "integer references schools(id)"})
    # db.create_table("topic", {"id": "int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY", "school_id": "integer references schools(id)", "topic_description": "text"})
    # src = Source([
    #                 Processor(
    #                         [Writer(lambda x: db.add_row("reviews", x))],
    #                         lambda x: [x, x])],
    #                 lambda: [{"raw_text": "this works", "concern_id": 1, "sentiment": 1.4782374, "concerns": "UCL"}]
    #             )