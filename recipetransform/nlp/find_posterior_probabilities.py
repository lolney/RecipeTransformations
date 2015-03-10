import pymongo, nltk
import recipetransform.tools.database as tools
import recipetransform.nlp.yummly as yum
from recipetransform.nlp.parse_ingredient import parse_ingredient


def setDict(keys, dict, value):

	for key in keys:
		if key not in dict:
			dict[key] = {}

	return dict

def addDict(key, dict, value):

	if key in dict:
		dict[key] = dict[key] + value
	else:
		dict[key] = value

	return dict


def encode(name, descriptor):
	return name + "&" + descriptor


def decode(word):
	return name.split("&")


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


def findPosteriors(ids, download_function):
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
			# p(recipe | word)
			posteriors[word][cat] = float(freqdists[cat][word]) / float(word_counts[word])

	return posteriors


def sanitize(lst):
	import re

	try:
		lst = [re.search("[\w\s]+$", item).group(0) for item in lst]
	except AttributeError:
		print lst

	return lst


def main():


	ids_to_cats, ids_to_ingredients = yum.idsToCategories()
	print ids_to_ingredients
	get_ingredients = lambda id : ids_to_ingredients[id]

	posteriors = findPosteriors(ids_to_cats, get_ingredients)

	print sanitize(["(   oz.) tomato paste"])

	db = tools.DBconnect()
	db.posteriors.drop()
	db.posteriors.insert(posteriors)


if __name__ == "__main__":
	main()


