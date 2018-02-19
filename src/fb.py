import facebook
import json
import requests
import pandas
import csv
import datetime
import os


my_token = 'EAACEdEose0cBADtRyv4Vq5IoA0buSOpmKj2TozAADMzKvzlNija2T4UOTKWNkBI30TeQuPBS5knzZA4jJCEAIOWWoRwLuAzSwtDxkUsZAqBZCluTP6lXqeOfpM7m7QLesQU19g2ZB0AW3UVNvg9x3yZAOuWW8vCJdXlN4awMWRHJgrZBZBM7UQmhxpUtPxCoIU0Tfv2bDKlVO5Hm5aWc7nG'
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
        if country == "United Kingdom" or country == "Country not displayed":
            counter += 1
            try:
                name = my_data['name']
                description = my_data['description']
            except KeyError:
                break
            try:
                location = my_data['place']['location']['city']
            except KeyError:
                location = "No location displayed"
            print(str(counter) + ": " + name + " \n " + "Location: " + location + "\n" + description + "\n\n" + "----------------------------------------------------" + "\n")
            fields = [name, location, description]
            file_name = since + ".csv"
            with open(file_name, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
                f.close()




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
        print_event_name_and_description(since)
        #print_pretty_events(data)
        events = json.loads(requests.get(next_page).text)
        try:
            next_page = events["paging"]["next"]
        except KeyError:
            break


#iterate_throught_pages()




for school in schools:
    now = datetime.datetime.now()
    since = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
    try:
        with open(since+'.csv') as file:
            print("Queries up-to-date.")
    except IOError as e:
        get_data(school, since)
        events = data
        iterate_throught_pages(since)
