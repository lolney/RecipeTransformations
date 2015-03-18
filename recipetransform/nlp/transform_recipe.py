import pymongo, re, nltk, operator
from bson.son import SON
import recipetransform.tools.database as tools
from recipetransform.tools.database import encode, decode
from recipetransform.tools.dictionary_ops import *
from recipetransform.nlp.transform_instructions import updateAllInstructions
import recipetransform.nlp.healthyTransformations as ht



def replaceIngredient(ingredient, candidate):

	new_ingredient = {}

	for key in ingredient:
		new_ingredient[key] = ingredient[key]

	for key in candidate:
		new_ingredient[key] = candidate[key]


	return new_ingredient


def tryExclusionTable(food_group, transform_category):

	db = tools.DBconnect()
	query = {"diet": transform_category}

	result = db.exclusion_table.find_one(query)

	if result is not None:
		if food_group in result["excluded"]:
			return "Legumes and Legume Products"

	return None


def getScore(ingredient, food_group, transform_category):
	""" 
	lookup encoded ingredient in db for given cuisine style
	"""
	score = None

	makeQuery = lambda str : {"ingredients.ingredient" : str}

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
	else:
		print "no results: ", ingredient, food_group

	return score


def findIngredientAboveScore(score, food_groups, transform_category, addl_query=[]):

	db = tools.DBconnect()

	pipe1 = [
	{"$match": {"food_group": {"$in": food_groups}}},
	{"$unwind": "$ingredients"},
	{"$match": {"ingredients." + transform_category: {"$gt":.05+2*score}}}]

	pipe2 =	[{"$sort": SON({"ingredients." + transform_category: -1})}]

	results = db.posteriors.aggregate(pipe1 + addl_query + pipe2)["result"]

	return results


def getReplacementCandidate(ingredient, score, food_group, transform_category, index=0):
	"""
	Look in food_group 
	Return the highest-scored ingredient x such that scoreOf(x) > score
	"""

	db = tools.DBconnect()

	addl_group = tryExclusionTable(food_group, transform_category)
	food_groups = [food_group]
	if addl_group is not None:
		food_groups.append(addl_group)

	name = ingredient["name"]
	name_regex = [re.compile(word, re.IGNORECASE) for word in nltk.word_tokenize(name)]
	query = [{"$match": {"ingredients.ingredient" : {"$in" : name_regex}}}]
	results = findIngredientAboveScore(score, food_groups, transform_category, query)

	if len(results) > index:
		#print len(results), results[0]["ingredients"][transform_category]
		return decode(results[index]["ingredients"]["ingredient"])
	
	results = findIngredientAboveScore(score, food_groups, transform_category)

	if len(results) > index:
		return decode(results[index]["ingredients"]["ingredient"])

	return ingredient


def reduceResults(results):

	food_groups_counts = {};
	for result in results:
		for food_group in result:
			food_groups_counts = addDict(food_group, food_groups_counts, 1)

	return sorted(food_groups_counts.items(), key=operator.itemgetter(1), reverse=True)[0][0]


def doAggregation(pipe, query, collection, query_index):

	db = tools.DBconnect()

	pipeline = list(pipe)
	pipeline[query_index] = {"$match":query}

	return db[collection].aggregate(pipeline)["result"]


def ingredientSearchAggregate(ingredient, makeQuery, collection, pipe, query_index):

	try:
		descriptor_strings = nltk.word_tokenize(ingredient["descriptor"])
		name_list = nltk.word_tokenize(ingredient["name"])
		name_regex = "|".join([r"(\b"+n+r"\b)" for n in name_list])
		print name_regex
		name = re.compile(name_regex, re.IGNORECASE)
		name_front = re.compile("^" + ingredient["name"] + ".*", re.IGNORECASE)
	
		# try name and descriptors
		q = makeQuery(name)
		if len(descriptor_strings) == 0:
			query = makeQuery(ingredient["name"])
		else:
			descriptors = [re.compile(descriptor, re.IGNORECASE) for descriptor in descriptor_strings]
			query = {"$and": ([q] + [makeQuery(descriptor) for descriptor in descriptors])}
		results = doAggregation(pipe, query, collection, query_index)
		
		"""
		# try just name (first the front of the string)
		query = makeQuery(name_front)
		if len(results) == 0:
			results = doAggregation(pipe, query, collection, query_index)
		"""

		# then in the remainder
		if len(results) == 0:
			results = doAggregation(pipe, q, collection, query_index)

	except:
		print "compile error: ", ingredient
		return []

	return results


def checkFoodGroupsList(name):
	tokens = nltk.word_tokenize(name)
	query = {"food_group": {"$in" : tokens}}

	db = tools.DBconnect()
	results = db.food_groups_list.find(query)

	if results.count() > 0:
		return results[0]["food_group"]
	else:
		return None


def getFoodGroup(ingredient):
	"""
	Depending on quality of USDA data, may need to reconsider how this is chosen
	"Beef products" and "Baked products" seem to include everything
	"""

	food_group = checkFoodGroupsList(ingredient["name"])

	if food_group is None:
		makeQuery = lambda name: {"food":name}


		pipe = [
		{},
		{"$unwind": "$food_groups"},
		{"$group": {"_id": "$food_groups", "count": {"$sum": 1}}},
		{"$sort": SON([("count", -1), ("_id", -1)])}
		]

		results = ingredientSearchAggregate(ingredient, makeQuery, "food_groups", pipe, 0)
		if len(results) > 0:
			food_group = results[0]['_id']
			print results
			print food_group


	return food_group


def transformDietCuisine(parsed_ingredients, parsed_instructions, transform_category):

	replacement_counter = {}
	new_ingredients = [ingredient for ingredient in parsed_ingredients]

	for i, ingredient in enumerate(parsed_ingredients):

		ingredient["descriptor"] = "" if "descriptor" not in ingredient.keys() else ingredient["descriptor"]
		food_group = getFoodGroup(ingredient)
		score = getScore(ingredient, food_group, transform_category)

		if score is None: # couldn't find ingredient in db, so don't try to replace
			continue

		try:
			index = replacement_counter[food_group]
		except:
			index = 0

		candidate = getReplacementCandidate(ingredient, score, food_group, transform_category, index)
		replacement_counter = addDict(food_group, replacement_counter, 1)

		if candidate is not None:
			new_ingredient = replaceIngredient(ingredient, candidate)
			new_ingredients[i] = (new_ingredient)

	
	new_instructions = updateAllInstructions(parsed_instructions, parsed_ingredients, new_ingredients)
			

	return new_ingredients, new_instructions


def transform_recipe(parsed_ingredients, parsed_instructions, transform_category, transform_type):
	
	if transform_type in ["cuisine","diet"]:
		result = transformDietCuisine(parsed_ingredients, parsed_instructions, transform_category)

	else:
		if transform_type in ["calories","sodium"] and transform_category in ["Low","High"]:
			result = ht.transformHealthy(parsed_ingredients, parsed_instructions, transform_category, transform_type)
		else:
			raise ValueError("unexpected transform_type: " + transform_type + ", " + transform_category)

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
	},
	{
	"name":"soy sauce",
	"descriptor": ""
	},
	{
	"name":"bacon",
	"descriptor": ""
	},
	{
	"name":"beef",
	"descriptor": ""
	},
	{
	"name":"fruit",
	"descriptor": ""
	},
	{
	"name":"soy sauce",
	"descriptor": ""
	},
	{
	"name":"sugar",
	"descriptor": "brown"
	},
	{
	"name":"fillets",
	"descriptor": ""
	},
	{
	"name":"fillet",
	"descriptor": ""
	},
	{
	"name":"ice",
	"descriptor": ""
	}]
	
	for ingredient in ingredients:
		print (ingredient["name"], getFoodGroup(ingredient))


def testIdReplacements():

	water = {
	"name":"water",
	"descriptor": ""
	}
	fava_beans = {
	"name":"fava beans",
	"descriptor": ""
	}
	print getReplacementCandidate(water, 0, "Beverages", "Pescetarian")
	print getReplacementCandidate(water, 0, "Beverages", "Pescetarian")
	print getReplacementCandidate(fava_beans, .1, "Legumes and Legume Products", "Pescetarian")
	print getReplacementCandidate(fava_beans, .2, "Legumes and Legume Products", "Pescetarian")

	print getReplacementCandidate(fava_beans, 0, "Legumes and Legume Products", "Italian")
	print getReplacementCandidate(fava_beans, 0, "Legumes and Legume Products", "Japanese")
	print getReplacementCandidate(fava_beans, 0, "Legumes and Legume Products", "Chinese")
	print getReplacementCandidate(fava_beans, 0, "Legumes and Legume Products", "American")
	print getReplacementCandidate(fava_beans, 0, "Legumes and Legume Products", "Mexican")

	print getScore({"name":"beans","descriptor":"cannellini"}, "Legumes and Legume Products", "Italian")
	print getScore({"name":"water","descriptor":""}, "Beverages", "Pescetarian")
	print getScore({"name":"spaghetti","descriptor":""}, "Meals, Entrees, and Side Dishes", "Italian")
	print getScore({"name":"parmesan cheese","descriptor":""}, "Dairy and Egg Products", "Pescetarian")
	print getScore({"name":"cheese","descriptor":""}, "Baked Products", "Pescetarian")
	print getScore({"name":"root","descriptor":"fresh ginger"}, "Baked Products", "Pescetarian")
	print getScore({"name":"root","descriptor":"fresh ginger"}, "Baked Products", "Greek")
	

def main():

	testIdReplacements()
	testFoodGroups()

	

if __name__ == "__main__":
	main()

