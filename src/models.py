import csv

def get_school_list(location=None, type=None):
    return [
            row["EstablishmentName"] 
            for row in csv.DictReader(open("data/schools.csv"))
            if 
                (location is None or row["Town"] == location)
                and
                (type == None or row["TypeOfEstablishment (name)"] == type)
           ]
