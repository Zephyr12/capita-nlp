"""
    This script yields all the events
    found related to all the educational
    institutions in UK.
    It runs an event query search for
    every institution name.
    The events are yielded through the
    run() function.
    It either yields results stored in
    a cache file or starts searching for
    events if no relevant cache file
    exists.
    The new results are also stored in
    the cache file.
    However, the script is not very
    efficient because it sleeps the
    thread 1 second after every API
    call in order to avoid getting
    the Facebook Token banned for
    "Running to many API calls".
    However, this can be solved
    if the user would have access
    to a special token provided by
    Facebook as a result of a
    specific request.
"""

import facebook
import json
import requests
import pandas
import csv
import datetime
import hashlib
import base64
import time


educatinal_institutions = pandas.read_csv("data/schools.csv", low_memory=False).EstablishmentName.tolist()

class FacebookData:
    BASE_URL = 'https://graph.facebook.com/'
    facebook_token = 'EAACEdEose0cBAG0ZAkiW7iXdEHRWG25V2k3RWkDD3QUDwOmcWMvmcvADK73OAUH31gZC5SZAXV88blN3WDmZCNeZCFiy81aI4ZCTYHwdIWBakHnC42ZBc4mSW0KJg4s94eqUhRKRkkyR1PWft8ZBvlkumBI0pgiC9F6vCZBl0nHRmoS3EJUUKm7D9xD09LrzfSz4NxFcZCrmSurJckiYPWHYCW'

    graph = facebook.GraphAPI(facebook_token)

    counter = 0

    #schools = pandas.read_csv("EduBase_Schools_UTF-8.csv").school_name.tolist()

    def __init__(self, educational_institutions=['UCL', 'University College London', 'Kings College London', 'Imperial College London']):
        self.data = None
        self.events = None
        self.next_page = None
        self.schools = educational_institutions

    def get_school_events(self, educational_institution, since):
        """
        Gets school events as a result of the search query.
        Also saves a pointer to the next page if there are many results for the specific query.
        :param educational_institution: school's name passed to the search query
        :param since: lowest accepted start date for found events
        """
        self.data = self.graph.request('search', {'q': educational_institution, 'type': 'event', 'since': since})
        time.sleep(1)
        self.events = json.dumps(self.data, indent=4, sort_keys=True)
        try:
            self.next_page = self.data["paging"]["next"]
        except KeyError:
            self.next_page = None


    def get_event_details(self, since, educational_institution):
        """
        For every event, extracts the relevant information such as event name and description.
        """
        for my_data in self.data["data"]:
            country = self.get_event_country(my_data)
            #Filters results outside UK.
            if country == "United Kingdom":  # or country == "Country not displayed":
                self.counter += 1
                try:
                    name = my_data['name']
                    description = my_data['description'].replace('\n', ' ')
                except KeyError:
                    break
                location = self.get_event_location(my_data)
                # print(str(counter) + ": " + name + " \n " + "Location: " + location + "\n" + description + "\n\n" + "----------------------------------------------------" + "\n")
                self.add_event_details_to_cache_file(description, location, name, since, educational_institution)
                yield from self.yield_event_details(description, location, name)

    def yield_event_details(self, description, location, name):
        yield (str(
            self.counter) + ": " + name + " \n " + "Location: " + location + "\n" + description + "\n\n" + "----------------------------------------------------" + "\n")

    def add_event_details_to_cache_file(self, description, location, name, since, educational_institution):
        """
        Stored the information related to a specific event to the cache file.
        :param description: Event description 
        :param location: Event location
        :param name: Event name
        :param educational_institution: Concerned educational institution
        """
        fields = [educational_institution, name, location, description]
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


    def iterate_throught_pages(self, since, educational_institution):
        """
        As an initial search query result might not display all the events,
        it can display a path to the next page of results related
        to our desired educational institutions.
        This function follows those next pages of results.
        """
        while self.next_page:
            self.data = self.events
            for i in self.get_event_details(since, educational_institution):
                yield i
            # Updates the events list with those found in the next page.
            self.events = json.loads(requests.get(self.next_page).text)

            #Try to check if there is another next page until exchausted.
            try:
                self.next_page = self.events["paging"]["next"]
            except KeyError:
                break


    def run(self):
        """
        Main function that runs the entire script.
        It yields all the events one by one, providing relevant information such as event name,
        location and description, but also the search query under which it was found i.g. the institution name.

        Running this function daily produces new results. It uses the since parameter in order to detect if a similar
        query was already made in the same day. If a similar query was already made the same day, then it returns the
        results stored in cache.
        """

        since = self.get_todays_date()

        #Try get results from cache file if existent.
        try:
            yield from self.yield_rows_from_cache_file(since)

        #Else, start querying for events.
        except IOError as e:
            self.create_cache_header(since)
            for school in self.schools:
                print("Searching events for: " + school)
                self.get_school_events(school, since)
                self.events = self.data
                for i in self.iterate_throught_pages(since, school):
                    # print(i)
                    yield i

    def create_cache_header(self, since):
        file_name = self.get_cache_ID(since)
        with open('data/' + file_name, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=["query", "name", "location", "raw_text"])
            writer.writeheader()

    def get_cache_ID(self, since):
        file_name = since
        for school in self.schools:
            file_name += "-"
            file_name += str(school)
        file_name += ".csv"
        return hashlib.sha1(bytes(file_name, encoding='UTF-8')).hexdigest()

    def yield_rows_from_cache_file(self, since):
        with open('data/' + self.get_cache_ID(since)) as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row

    def get_todays_date(self):
        now = datetime.datetime.now()
        since = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
        return since


#x = FacebookData(list(map(lambda r: r["EstablishmentName"], filter(lambda e: e["Town"] == "London", csv.DictReader(open("data/schools.csv"))))))
x = FacebookData(educatinal_institutions)
for i in x.run():
    print(i)



