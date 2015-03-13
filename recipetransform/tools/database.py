import pymongo

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