import pymongo, re, nltk, operator
import recipetransform.tools.database as tools
from recipetransform.tools.dictionary_ops import *



def replaceIngredient(ingredients, index, new_ingredient):

	return ingredients



def getScore(ingredient, food_group, transform_category):
	""" 
	lookup encoded ingredient in db for given cuisine style
	"""
	makeQuery = lambda str : {"food_group": food_group, "ingredients":{"$elemMatch" : {"ingredient" : str}}}
	results = runGauntlet(ingredient, makeQuery, "posteriors")

	results = results.sort(transform_category, pymongo.DESCENDING)

	return results[0]["ingredients"][0][transform_category]



def updateInstruction(parsed_instructions, old_ingredient, new_ingredient):

	return parsed_instructions



def getReplacementCandidate(encoded_ingredient, score, food_group, transform_category, transform_type):
	"""
	Look in food_group 
	Return the highest-scored ingredient x such that scoreOf(x) > score
	"""

	db = tools.DBconnect()

	query = {transform_category : {"$gt" : score}}
	query_outside = {"food_group":food_group, "ingredients":{"$elemMatch" : query}}

	results = db.posteriors.find(query_outside).sort(transform_category, pymongo.DESCENDING)


	return results[0]["ingredients"][0]["ingredient"]



def reduceResults(results):


	food_groups_counts = {};
	for result in results:
		for food_group in result:
			food_groups_counts = addDict(food_group, food_groups_counts, 1)

	return sorted(food_groups_counts.items(), key=operator.itemgetter(1), reverse=True)[0][0]



def runGauntlet(ingredient, makeQuery, collection):

	db = tools.DBconnect()


	descriptor_strings = nltk.word_tokenize(ingredient["descriptor"])
	descriptors = [re.compile(descriptor, re.IGNORECASE) for descriptor in descriptor_strings]
	name = re.compile(ingredient["name"], re.IGNORECASE)
	name_front = re.compile("^" + ingredient["name"] + ".*", re.IGNORECASE)

	q = makeQuery(name)
	# try name and descriptors
	results = db[collection].find({"$and": ([q] + [makeQuery(descriptor) for descriptor in descriptors])})
	
	# try just name (first the front of the string)
	if results.count() == 0:
		results = db[collection].find(makeQuery(name_front))

	# try name anywhere 
	if results.count() == 0:
		results = db[collection].find(q)

	return results



def getFoodGroup(ingredient):

	food_group = None

	makeQuery = lambda name: {"food":name}
	results = runGauntlet(ingredient, makeQuery, "food_groups")

	if results.count() != 0:

		items = [item["food_groups"] for item in results]
		food_group = reduceResults(items)


	return food_group



def transform_recipe(parsed_ingredients, parsed_instructions, transform_category, transform_type):
	
	for i, ingredient in parsed_ingredients:

		encoded_ingredient = encode(ingredient)
		score = getScore(ingredient, transform_category)

		if score is None: # couldn't find ingredient in db, so don't try to replace
			continue

		candidate = getReplacementCandidate(score, food_group, transform_category, transform_type)

		if candidate is not None:
			parsed_ingredients = replaceIngredient(parsed_ingredients, i, candidate)
			parsed_instructions = updateInstruction(parsed_instructions, ingredient, candidate)

	return parsed_ingredients, parsed_instructions


def testFoodGroups():

	ingredients = [
	{
	"name": "chicken",
	"descriptor": "fried, breaded"
	},
	{
	"name": "water",
	"descriptor": ""
	},
	{
	"name": "beef",
	"descriptor": ""
	}
	]
	
	print [getFoodGroup(ingredient) for ingredient in ingredients]


def main():
	
	print getReplacementCandidate("water", 0, "Beef Products", "Pescetarian", "diet")
	print getScore({"name":"water","descriptor":""}, "Beef Products", "Pescetarian")
	

if __name__ == "__main__":
	main()

