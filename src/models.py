import csv

def get_school_list(location=None, type=None):
    '''
        :param location: Optional. The town that the schools in the list should be from
        :param type: The type of establishments in the list
        :returns: [{school}]
    '''
    return [
            row["EstablishmentName"] 
            for row in csv.DictReader(open("data/schools.csv"))
            if 
                (location is None or row["Town"] == location)
                and
                (type == None or row["TypeOfEstablishment (name)"] == type)
           ]
