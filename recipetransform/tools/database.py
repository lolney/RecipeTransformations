import pymongo

def DBconnect():
	client = pymongo.MongoClient('mongodb://localhost:27017/')
	db = client.recipes

	return db