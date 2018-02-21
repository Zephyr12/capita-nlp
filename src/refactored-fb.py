import facebook
import json
import requests
import pandas
import csv
import datetime





class FacebookData:
    BASE_URL = 'https://graph.facebook.com/'
    facebook_token = 'EAACEdEose0cBADWdYqmZCOkZAyr0zk0Bz689mr7XIkfqiSNYhtaiD6PJrDzLMV2zHBk3WhoiTfFQhXPlAp8KaPgENL4fFQvxqpunPsyUkkFOth9EhAb4bwk2kbswrVKuZBkVLwv10VmH7xYfzZAKaeUefnR57HZAxT7PbstzsZC1Je0FfIkf5VHL68KrkIvnM5NI3peKG5U3E3JtSZBMwDH'

    graph = facebook.GraphAPI(facebook_token)

    counter = 0

    # schools = pandas.read_csv("EduBase_Schools_UTF-8.csv").school_name.tolist()
    schools = ['UCL','University College London', 'Kings College London','Imperial College London']

    def __init__(self):
        self.data = None
        self.events = None
        self.next_page = None

    def get_school_events(self, school, since):
        self.data = self.graph.request('search', {'q': school, 'type': 'event', 'since': since})
        self.events = json.dumps(self.data, indent=4, sort_keys=True)
        try:
            self.next_page = self.data["paging"]["next"]
        except KeyError:
            self.next_page = None


    def get_event_details(self, since):
        for my_data in self.data["data"]:
            country = self.get_event_country(my_data)
            if country == "United Kingdom":  # or country == "Country not displayed":
                self.counter += 1
                try:
                    name = my_data['name']
                    description = my_data['description'].replace('\n', ' ')
                except KeyError:
                    break
                location = self.get_event_location(my_data)
                # print(str(counter) + ": " + name + " \n " + "Location: " + location + "\n" + description + "\n\n" + "----------------------------------------------------" + "\n")
                self.add_event_details_to_cache_file(description, location, name, since)
                yield from self.yield_event_details(description, location, name)

    def yield_event_details(self, description, location, name):
        yield (str(
            self.counter) + ": " + name + " \n " + "Location: " + location + "\n" + description + "\n\n" + "----------------------------------------------------" + "\n")

    def add_event_details_to_cache_file(self, description, location, name, since):
        fields = [name, location, description]
        with open('data/' + self.get_cache_ID(since), 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            f.close()

    def get_event_location(self, event):
        try:
            location = event['place']['location']['city']
        except KeyError:
            location = "No location displayed"
        return location

    def get_event_country(self, event):
        try:
            country = event['place']['location']['country']
        except KeyError:
            country = "Country not displayed"
        return country

    def print_pretty_events(self, events):
        print(json.dumps(events, indent=4, sort_keys=True))


    def iterate_throught_pages(self, since):
        while self.next_page:
            self.data = self.events
            for i in self.get_event_details(since):
                yield i
            # print_pretty_events(data)
            self.events = json.loads(requests.get(self.next_page).text)
            try:
                self.next_page = self.events["paging"]["next"]
            except KeyError:
                break


    def run(self):
        since = self.get_todays_date()
        try:
            yield from self.yield_rows_from_cache_file(since)
        except IOError as e:
            self.create_cache_header(since)
            for school in self.schools:
                self.get_school_events(school, since)
                self.events = self.data
                for i in self.iterate_throught_pages(since):
                    # print(i)
                    yield i

    def create_cache_header(self, since):
        file_name = self.get_cache_ID(since)
        with open('data/' + file_name, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=["name", "location", "raw_text"])
            writer.writeheader()

    def get_cache_ID(self, since):
        file_name = since
        for school in self.schools:
            file_name += "-"
            file_name += str(school)
        file_name += ".csv"
        return file_name

    def yield_rows_from_cache_file(self, since):
        with open('data/' + self.get_cache_ID(since)) as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row

    def get_todays_date(self):
        now = datetime.datetime.now()
        since = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
        return since


x = FacebookData()
for i in x.run():
    print(i)



