import facebook
import json
import requests
import pandas

my_token = 'your token'
BASE_URL = 'https://graph.facebook.com/'
counter = 0

graph = facebook.GraphAPI(my_token)

schools = pandas.read_csv("data/EduBase_Schools_UTF-8.csv").school_name.tolist()


def get_data(school):
    global data, events, next_page
    data = graph.request('search', {'q': school, 'type': 'event'})
    events = json.dumps(data, indent=4, sort_keys=True)
    try:
        next_page = data["paging"]["next"]
    except KeyError:
        next_page = None


#get_data()


def print_event_name_and_description():
    global counter
    for my_data in data["data"]:
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

def print_pretty_events(events):
    print (json.dumps(events,indent=4,sort_keys=True))

#new_events = json.loads(requests.get(next_page).text)
#new = json.dumps(new_events, indent=4, sort_keys=True)

#print(events)

#events = data


def iterate_throught_pages():
    global data, events, next_page
    while next_page:
        data = events
        print_event_name_and_description()
        #print_pretty_events(data)
        events = json.loads(requests.get(next_page).text)
        try:
            next_page = events["paging"]["next"]
        except KeyError:
            break


#iterate_throught_pages()

for school in schools:
    get_data(school)
    events = data
    iterate_throught_pages()
