import pymongo, re

def DBconnect():
	client = pymongo.MongoClient('mongodb://localhost:27017/')
	db = client.recipes

	return db


def encode(name, descriptor):
	return name + "}" + descriptor


def decode(word):
	 items = word.split("}")

	 if len(items) > 2:
	 	print item
	 	raise Exception()

	 ingredient = {
	 "name" : items[0],
	 "descriptor" : items[1] if len(items) == 2 else ""
	 }
	 return ingredient


def queryDbForName(name):

 	db = DBconnect()

 	name_regex = re.compile(name, re.IGNORECASE)

	pipe = [
		{"$unwind": "$ingredients"},
		{"$match": {"ingredients.ingredient" : name_regex}}
	]

	results = db.posteriors.aggregate(pipe)["result"]

	return len(results)