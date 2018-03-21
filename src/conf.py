db_path = "dbname=capita user=amartya password=test"

tsr_followed_schools = [
    "Cranfield University",
    "Birkbeck, University of London",
    "Brunel University London",
    "University of East London",
    "Goldsmiths University",
    "University of Greenwich",
    "King's College London",
    "Kingston University",
    "London School of Economics",
    "London Metropolitan University",
    "London South Bank University",
    "Middlesex University",
    "Queen Mary University London",
    "Ravensbourne",
    "University of Roehampton",
    "Royal Holloway",
    "St Mary's University, Twickenham",
    "University College, London",
    "University of West London",
    "University of Westminster",
]


twitter_followed_schools = [
    "Cranfield University",
    "Birkbeck College",
    "Brunel University",
    "University of East London",
    "Goldsmiths College, University of London",
    "University of Greenwich",
    "King's College London",
    "Kingston University",
    "London School of Economics and Political Science",
    "London Metropolitan University",
    "London South Bank University",
    "Middlesex University",
    "Queen Mary and Westfield College",
    "Ravensbourne",
    "Roehampton University",
    "Royal Holloway and Bedford New College",
    "St Mary's University, Twickenham",
    "University College London",
    "University of West London",
    "University of Westminster",
]

tsr_ner_shortcut = {k: v for (k,v) in zip(tsr_followed_schools, twitter_followed_schools)}

twitter_update_rate = 1 # days
