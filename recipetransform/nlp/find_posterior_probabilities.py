import pymongo, nltk, re
import recipetransform.tools.database as tools
import recipetransform.nlp.yummly as yum
from recipetransform.nlp.parse_ingredient import parse_ingredient
from recipetransform.nlp.transform_recipe import getFoodGroup
from recipetransform.tools.dictionary_ops import *
from recipetransform.tools.database import encode, decode





def findWordCountForRecipe(cats, ingredients, freqdists):
	""" 
	cats -  a list of strings
	ingredients - a list of ingredient dictionaries
	"""
	ingredients = sanitize(ingredients)
	for category in cats:
		freqdist = freqdists[category]
		for ingredient in ingredients:
			freqdist = addDict(ingredient, freqdist, 1)
			"""
			word1 = encode(ingredient["name"], ingredient["descriptor"])
			word2 = encode(ingredient["name"], "")
			freqdist = addDict(word1, freqdist, 1)
			freqdist = addDict(word2, freqdist, 1)"""

	return freqdists


def findWordCounts(freqdists):

	aggregate = {}
	for cat in freqdists:
		for word in freqdists[cat]:
			addDict(word, aggregate, freqdists[cat][word])

	return aggregate


def findPosteriors(ids, download_function, penalize_below_n=10):
	"""
	ids: dictionary of id -> list of cats
	download_function: takes an id and returns a list of strings (representing ingredients)

	Count words for each recipe type : p(word | recipe)
	Get count for each recipe type : p(recipe)
	Merge counts : p(word)
	Find p(word | recipe) * p(recipe) / p(word) for each word
	In this case, freqdists[cat][word] is  #(word and cat), so we just need to divide by #(word)
	to get p(cat | word)
	Store this somewhere
	"""
	# freqdists: dictionary keyed by category, with values as dictionaries keyed by word
	freqdists = {}
	for id in ids: # loop over recipes
		ingredients = download_function(id)
		cats = ids[id]
		# TODO: write parser
		#parsed_ingredients = [parse_ingredient(ingredient) for ingredient in ingredients]
		# add all the categories to the freqdists
		freqdists = setDict(cats, freqdists, {})
		# set word counts for each word in each category
		findWordCountForRecipe(cats, ingredients, freqdists)

	# total count of each word
	word_counts = findWordCounts(freqdists)

	posteriors = {}
	for word in word_counts:
		posteriors[word] = {}
		for cat in freqdists:

			if word not in freqdists[cat]:
				freqdists[cat][word] = 0

			# penalize ingredients with lower word_counts[word]
			penalty = 1
			if word_counts[word] < penalize_below_n:
				penalty =  1 + penalize_below_n - word_counts[word]
				print penalty

			# p(recipe | word)
			posteriors[word][cat] = (float(freqdists[cat][word]) / float(word_counts[word])) / penalty

	return posteriors


def sanitize(lst):

	try:
		lst = [re.search("[\w\s]+$", item).group(0) for item in lst]
	except AttributeError:
		print lst

	return lst


def splitCategories(posteriors):

	diets = "Paleo", "[Vv]egetarian", "Pescetarian", "Vegan"
	regex = "|".join(diets)

	new_posteriors = {}
	for word in posteriors:

		new_posteriors[word] = {"cuisine": {}, "diet": {}}

		for cat in posteriors[word]:

			if re.search(regex, cat) is None:
				new_posteriors[word]["cuisine"][cat] = posteriors[word][cat]
			else:
				new_posteriors[word]["diet"][cat] = posteriors[word][cat]

	return new_posteriors

"""
{
food_group:""
ingredients:{"ingredient":name, posteriors: {"cuisine":{},"diet":{}}}
}
"""

"""
{
food_group:""
ingredients:{"ingredient":name, transform_type:diet, cats ... }
}
"""

def addFoodGroups(ingredients):

	print "creating food groups dict"
	food_groups = {}
	for encoded_ingredient in ingredients:
		ingredient = decode(encoded_ingredient)
		food_group = getFoodGroup(ingredient)
		print food_group
		addItemToDict(food_group, food_groups, encoded_ingredient)

	print "creating mongodb representation"
	output = []
	for food_group in food_groups:
		dict = {"food_group":food_group}

		ingredients_mongo = []
		for ingredient in food_groups[food_group]:


			inner_dict1 = ingredients[ingredient]["diet"].copy()
			inner_dict1.update({"ingredient":ingredient, "transform_type": "diet"})

			inner_dict2 = ingredients[ingredient]["cuisine"].copy()
			inner_dict2.update({"ingredient":ingredient, "transform_type": "cuisine"})

			ingredients_mongo.append(inner_dict1)
			ingredients_mongo.append(inner_dict2)


		dict["ingredients"] = ingredients_mongo
		output.append(dict)

	return output


def main():


	ids_to_cats, ids_to_ingredients = yum.idsToCategories()
	get_ingredients = lambda id : ids_to_ingredients[id]

	posteriors = findPosteriors(ids_to_cats, get_ingredients)
	posteriors = splitCategories(posteriors)
	food_groups = addFoodGroups(posteriors)

	db = tools.DBconnect()
	db.posteriors.drop()
	for food_group in food_groups:
		db.posteriors.insert(food_group)


if __name__ == "__main__":
	main()


