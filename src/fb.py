import facebook
import json
import requests

my_token = 'EAACEdEose0cBAJJfUEiNDEARrfZC5lTWZBkZBMNv6HIvqDZBUx2yDI3J5laFEca8DhtB0524KevX2ZAlSyt4hn1JF8hH4CW7JOfdJTPOfs4iL6j4fZAw8LLs8bbUhbeFSsm8AKBUj4CBfwO7aMNERiX9hgRMLv1oOzmhyjSTcZAHriJpThekQ09qMZCFJZCj98eZASRsnDxgZAjXGDRa49UGUqP'
BASE_URL = 'https://graph.facebook.com/'
counter = 0

graph = facebook.GraphAPI(my_token)
data = graph.request('search', {'q': 'school', 'type': 'event'})

events = json.dumps(data, indent=4, sort_keys=True)
paging = json.loads(events)
next_page = paging["paging"]["next"]


def print_event_name_and_description():
    global counter
    for my_data in data["data"]:
        counter += 1
        try:
            name = my_data['name']
            description = my_data['description']
        except KeyError:
            break
        print(str(counter) + ": " + name + " : " + description + "\n\n" + "----------------------------------------------------" + "\n")

def print_pretty_events(events):
    print (json.dumps(events,indent=4,sort_keys=True))

#new_events = json.loads(requests.get(next_page).text)
#new = json.dumps(new_events, indent=4, sort_keys=True)

#print(events)

events = data

while next_page:
    data = events
    print_event_name_and_description()
    #print_pretty_events(data)
    events = json.loads(requests.get(next_page).text)
    try:
        next_page = events["paging"]["next"]
    except KeyError:
        break


