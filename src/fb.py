import facebook
import datetime
import json
import requests
import pandas
import csv
import datetime
import os


my_token = 'EAACEdEose0cBAHWa4BK9jakIkabJ4agIFvU7XW8MAL61lO5teZC1gHmhc6oDYt5fxnWaH5cClAKtGFYNjPmqtY07MNhKkD6f8n6tLcXvqzoXnCcqPNgwbQosm8Avf3htcm6Xhfr2TaZB7epACrKudho6A43xgJ3T3mSyTRntNGfGzgghtDAJP6QyNMqUe5vDIV8uH6UgZDZD'
BASE_URL = 'https://graph.facebook.com/'
counter = 0

graph = facebook.GraphAPI(my_token)

#schools = pandas.read_csv("EduBase_Schools_UTF-8.csv").school_name.tolist()
schools = ['UCL']


def get_data(school,since):
    global data, events, next_page
    data = graph.request('search', {'q': school, 'type': 'event', 'since':since})
    events = json.dumps(data, indent=4, sort_keys=True)
    try:
        next_page = data["paging"]["next"]
    except KeyError:
        next_page = None


#get_data()


def print_event_name_and_description(since):
    global counter
    for my_data in data["data"]:
        try:
            country = my_data['place']['location']['country']
        except KeyError:
            country = "Country not displayed"

        if country == "United Kingdom":# or country == "Country not displayed":
            counter += 1
            try:
                description = my_data['description'].replace('\n',' ')
            except KeyError:
                break

            try:
                location = my_data['place']['location']['city']
            except KeyError:
                location = "No location displayed"

            time = datetime.datetime.now()
            # print(str(counter) + ": " + name + " \n " + "Location: " + location + "\n" + description + "\n\n" + "----------------------------------------------------" + "\n")
            fields = [location + description, time]
            file_name = since + ".csv"
            with open('data/'+file_name, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
                f.close()

            yield { "raw_text": location + description, "timestamp": time }

def print_pretty_events(events):
    print (json.dumps(events,indent=4,sort_keys=True))

#new_events = json.loads(requests.get(next_page).text)
#new = json.dumps(new_events, indent=4, sort_keys=True)

#print(events)

#events = data


def iterate_throught_pages(since):
    global data, events, next_page
    while next_page:
        data = events
        for i in print_event_name_and_description(since):
            yield i
        print_pretty_events(data)
        events = json.loads(requests.get(next_page).text)
        try:
            next_page = events["paging"]["next"]
        except KeyError:
            break


#iterate_throught_pages()



def run():
    global data, events, next_page
    for school in schools:
        now = datetime.datetime.now()
        since = str(2017) + "-" + str(10) + "-" + str(1)
        try:
            with open('data/'+since+'.csv') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row = {"raw_text": row["raw_text"], "timestamp": datetime.datetime.now()}
                    yield row
        except IOError as e:
            file_name = since + ".csv"
            with open('data/' + file_name, 'a') as f:
                writer = csv.DictWriter(f, fieldnames=["location", "raw_text", "timestamp"])
                writer.writeheader()
            get_data(school, since)
            events = data
            for i in iterate_throught_pages(since):
                yield i
