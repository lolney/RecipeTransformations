import pymongo, re, nltk, operator
from bson.son import SON
import recipetransform.tools.database as tools
from recipetransform.tools.dictionary_ops import *



def replaceIngredient(ingredients, index, new_ingredient):
	"""
	replace parsed ingredient (full ingredient dictionary) at index 
	with new ingredient (ingredient dictionary with name, descriptor)
	"""

	return ingredients


def updateInstruction(parsed_instructions, old_ingredient, new_ingredient):
	"""
	update instructions, replacing old_ingredient (full ingredient dictionary)
	with new_ingredient (ingredient dictionary with name, descriptor)
	"""
	return parsed_instructions


def getScore(ingredient, food_group, transform_category):
	""" 
	lookup encoded ingredient in db for given cuisine style
	"""
	score = None

	makeQuery = lambda str : {"food_group": food_group, "ingredients.ingredient" : str}

	pipe = [
	{"$unwind": "$ingredients"},
	{},
	{"$match": {"ingredients." + transform_category: {"$gte":0}}},
	{"$sort": SON({"ingredients." + transform_category: -1})}
	]

	results = ingredientSearchAggregate(ingredient, makeQuery, "posteriors", pipe, 1)

	if len(results) != 0:
		#print results[0]["ingredients"]["ingredient"]
		results = [result["ingredients"][transform_category] for result in results]
		score = results[0]

	return score


def getReplacementCandidate(encoded_ingredient, score, food_group, transform_category):
	"""
	Look in food_group 
	Return the highest-scored ingredient x such that scoreOf(x) > score
	"""

	db = tools.DBconnect()

	match1 = {"$match": {"food_group": food_group}}
	unwind = {"$unwind": "$ingredients"}
	match2 = {"$match": {"ingredients." + transform_category: {"$gte":score}}}
	sort = {"$sort": SON({"ingredients." + transform_category: -1})}	

	results = db.posteriors.aggregate([match1, unwind, match2, sort])["result"]

	if len(results) > 0:
		#print len(results), results[0]["ingredients"][transform_category]
		return results[0]["ingredients"]["ingredient"]
	else:
		return encoded_ingredient



def reduceResults(results):

	food_groups_counts = {};
	for result in results:
		for food_group in result:
			food_groups_counts = addDict(food_group, food_groups_counts, 1)

	return sorted(food_groups_counts.items(), key=operator.itemgetter(1), reverse=True)[0][0]



def ingredientSearch(ingredient, makeQuery, collection):

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


def doAggregation(pipe, query, collection, query_index):

	db = tools.DBconnect()

	pipeline = list(pipe)
	pipeline[query_index] = {"$match":query}

	return db[collection].aggregate(pipeline)["result"]


def ingredientSearchAggregate(ingredient, makeQuery, collection, pipe, query_index):

	descriptor_strings = nltk.word_tokenize(ingredient["descriptor"])
	name = re.compile(ingredient["name"], re.IGNORECASE)
	name_front = re.compile("^" + ingredient["name"] + ".*", re.IGNORECASE)

	# try name and descriptors
	q = makeQuery(name)
	if len(descriptor_strings) == 0:
		query = makeQuery(ingredient["name"])
	else:
		descriptors = [re.compile(descriptor, re.IGNORECASE) for descriptor in descriptor_strings]
		query = {"$and": ([q] + [makeQuery(descriptor) for descriptor in descriptors])}
	results = doAggregation(pipe, query, collection, query_index)
	
	# try just name (first the front of the string)
	query = makeQuery(name_front)
	if len(results) == 0:
		results = doAggregation(pipe, query, collection, query_index)

	# then in the remainder
	if len(results) == 0:
		results = doAggregation(pipe, q, collection, query_index)

	return results


def getFoodGroup(ingredient):
	"""
	Depending on quality of USDA data, may need to reconsider how this is chosen
	"Beef products" and "Baked products" seem to include everything
	"""

	food_group = None

	makeQuery = lambda name: {"food":name}

	"""
	results = ingredientSearch(ingredient, makeQuery, "food_groups")
	if results.count() != 0:

		items = [item["food_groups"] for item in results]
		food_group = reduceResults(items) """

	pipe = [
	{},
	{"$unwind": "$food_groups"},
	{"$group": {"_id": "$food_groups", "count": {"$sum": 1}}},
	{"$sort": SON([("count", -1), ("_id", -1)])}
	]

	results = ingredientSearchAggregate(ingredient, makeQuery, "food_groups", pipe, 0)
	if len(results) > 0:
		print results
		food_group = results[0]['_id']


	return food_group


def transformDietCuisine(parsed_ingredients, parsed_instructions, transform_category):

	for i, ingredient in parsed_ingredients:

		encoded_ingredient = encode(ingredient)
		score = getScore(ingredient, transform_category)

		if score is None: # couldn't find ingredient in db, so don't try to replace
			continue

		candidate = getReplacementCandidate(score, food_group, transform_category, transform_type)

		if candidate is not None:
			parsed_ingredients = replaceIngredient(parsed_ingredients, i, candidate)
			parsed_instructions = updateInstruction(parsed_instructions, ingredient, candidate)


	return {"ingredients":parsed_ingredients, "instructions":parsed_instructions}


def transform_recipe(parsed_ingredients, parsed_instructions, transform_category, transform_type):
	
	if transform_type in ["cuisine","diet"]:
		result = transformDietCuisine(parsed_ingredients, parsed_instructions, transform_category)

	else:
		if transform_type in ["calories","sodium"] and transform_category in ["low","high"]:
			result = transformHealthy(parsed_ingredients, parsed_instructions, transform_category, transform_type)
		else:
			raise ValueError("unexpected transform_type")

	return result



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
	},
	{
	"name": "beans",
	"descriptor": "fava"
	},
	{
	"name": "beans",
	"descriptor": ""
	},
	{
	"name": "parmesan cheese",
	"descriptor": ""
	},
	{
	"name": "cheese",
	"descriptor": ""
	},
	{
	"name": "cheese",
	"descriptor": "parmesan"
	},
	{
	"name": "spaghetti",
	"descriptor": ""
	},
	{
	"name":"oregano",
	"descriptor": ""
	},
	{
	"name":"miso",
	"descriptor": ""
	},
	{
	"name":"meat",
	"descriptor": ""
	}]
	
	for ingredient in ingredients:
		print (ingredient["name"], getFoodGroup(ingredient))


def testIdReplacements():

	print getReplacementCandidate("water", 0, "Beverages", "Pescetarian")
	print getReplacementCandidate("water", 0, "Beverages", "Pescetarian")
	print getReplacementCandidate("fava beans", .1, "Legumes and Legume Products", "Pescetarian")
	print getReplacementCandidate("fava beans", .2, "Legumes and Legume Products", "Pescetarian")

	print getReplacementCandidate("fava beans", 0, "Legumes and Legume Products", "Italian")
	print getReplacementCandidate("fava beans", 0, "Legumes and Legume Products", "Japanese")
	print getReplacementCandidate("fava beans", 0, "Legumes and Legume Products", "Chinese")
	print getReplacementCandidate("fava beans", 0, "Legumes and Legume Products", "American")
	print getReplacementCandidate("fava beans", 0, "Legumes and Legume Products", "Mexican")

	print getScore({"name":"water","descriptor":""}, "Beverages", "Pescetarian")
	print getScore({"name":"spaghetti","descriptor":""}, "Meals, Entrees, and Side Dishes", "Italian")
	print getScore({"name":"parmesan cheese","descriptor":""}, "Dairy and Egg Products", "Pescetarian")
	print getScore({"name":"cheese","descriptor":""}, "Baked Products", "Pescetarian")


def main():

	testIdReplacements()
	testFoodGroups()

	

if __name__ == "__main__":
	main()

