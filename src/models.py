import csv

def get_school_list():
    return [row["EstablishmentName"] for row in csv.DictReader(open("data/schools.csv"))]
