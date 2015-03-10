import pymongo, re, nltk, operator
import recipetransform.tools.database as tools
from recipetransform.nlp.find_posterior_probabilities import addDict



def replaceIngredient(ingredients, index, new_ingredient):

	return ingredients


def updateInstruction(parsed_instructions, old_ingredient, new_ingredient):

	return parsed_instructions


def getReplacementCandidate(encoded_ingredient, score, food_group):
	"""
	Look in food_group 
	Return the highest-scored x ingredient such that scoreOf(x) > score
	"""


def reduceResults(results):


	food_groups_counts = {};
	for result in results:
		for food_group in result:
			food_groups_counts = addDict(food_group, food_groups_counts, 1)

	return sorted(food_groups_counts.items(), key=operator.itemgetter(1), reverse=True)[0]


def getFoodGroup(ingredient):

	db = tools.DBconnect()
	food_group = None

	descriptor_strings = nltk.word_tokenize(ingredient["descriptor"])
	descriptors = [re.compile(descriptor, re.IGNORECASE) for descriptor in descriptor_strings]
	name = re.compile(ingredient["name"], re.IGNORECASE)


	# try name and descriptors
	results = db.food_groups.find({"$and": ([{"food":name}] + [{"food": descriptor} for descriptor in descriptors])})
	
	# try just name
	if results.count() == 0:
		results = db.food_groups.find({"food": name})

	if results.count() != 0:

		items = [item["food_groups"] for item in results]
		food_group = reduceResults(items)


	return food_group



def transform_recipe(parsed_ingredients, parsed_instructions):
	
	for i, ingredient in parsed_ingredients:

		food_group = getFoodGroup(ingredient)
		encoded_ingredient = encode(ingredient)
		score = lookup(encoded_ingredient, food_group)
		candidate = getReplacementCandidate(score, food_group)

		if candidate is not None:
			parsed_ingredients = replaceIngredient(parsed_ingredients, i, candidate)
			parsed_instructions = updateInstruction(parsed_instructions, ingredient, candidate)

	return parsed_ingredients, parsed_instructions


def main():

	ingredients = [
	{
	"name": "chicken",
	"descriptor": "fried, breaded"
	},
	{
	"name": "beef",
	"descriptor": ""
	}
	]
	
	print [getFoodGroup(ingredient) for ingredient in ingredients]

if __name__ == "__main__":
	main()

