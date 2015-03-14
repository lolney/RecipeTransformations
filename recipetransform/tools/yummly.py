import urllib, urllib2, os, json
from sets import Set
import recipetransform.tools.database as tools
from recipetransform.tools.dictionary_ops import *


def getAuthInfo():
	app_id = os.environ.get('YummlyId')
	auth_key = os.environ.get('YummlyKey')

	query = {
	"_app_id":app_id,
	"_app_key":auth_key
	}

	return query


# Yummly expects a format different from what urlencode outputs
def listToQueryString(query_param, lst):
	formated_items = []
	for item in lst:
		tmp = query_param + "=" + item
		formated_items.append(tmp)

	return "&".join(formated_items)


def doQuery(endpoint, query, addl_parms=""):
	qstring = urllib.urlencode(query)
	url = "http://api.yummly.com/v1/api/" + endpoint + qstring + addl_parms
	print url
	result_string = urllib.urlopen(url).read()
	result = json.loads(result_string)

	return result


def getRecipesList(search_params, max_result=100):
	# do a query for every category we might want
	query = getAuthInfo()
	return doQuery("recipes?", query, "&" + search_params + "&maxResult=" + str(max_result))["matches"]


def getRecipe(id):
	query = getAuthInfo()

	result = doQuery("recipe/" + id + "?", query)
	return result["ingredientLines"]


def getDescription(item):
	desc = ""
	try:
		desc = item["shortDescription"]
	except KeyError:
		desc = item["description"]

	return desc


def getSearchParams(category):

	endpoint = "metadata/" + category + "?"
	query = getAuthInfo()
	qstring = urllib.urlencode(query)
	url = "http://api.yummly.com/v1/api/" + endpoint + qstring
	print url
	jsonp = urllib2.urlopen(url).read()

	json_str = jsonp[ jsonp.index("[") : jsonp.rindex(")") ]
	json_obj = json.loads(json_str)

	print json_obj

	return ([getDescription(item) for item in json_obj], [item["searchValue"] for item in json_obj])


def insertResults(collection, results):
	db = tools.DBconnect()
	for result in results:
		db[collection].insert(result)


def getCats():
	with open("outfile_ingredients.json", "r") as file:
		return json.load(file)


def idsToCategories():

	ids_to_cats = {}
	ids_to_ingredients = {}
	categories = getCats()

	for cat in categories:
		for recipe_dictionary in categories[cat]:
			id = recipe_dictionary["id"]
			ingredients = recipe_dictionary["ingredients"]
			ids_to_cats = addItemToDict(id, ids_to_cats, cat)
			ids_to_ingredients = addListToDict(id, ids_to_ingredients, ingredients)

	return ids_to_cats, ids_to_ingredients


def doDownload():
	attributes = {"diet":"allowedDiet[]","cuisine":"allowedCuisine[]"}
	results_dictionary = {}

	# other attributes (doesn't work very well)
	"""
	for attribute in attributes:
		categories, search_terms_list = getSearchParams(attribute)
		search_terms_string = listToQueryString(attributes[attribute], search_terms_list)
		results = getRecipesList(search_terms_string, 50)

		for result in results:
			for category in result["attributes"][attribute]:
				results_dictionary = addItemToDict(category, results_dictionary, result["id"]) """

	for attribute in attributes:
		categories, search_terms_list = getSearchParams(attribute)
		for category, search_term in zip(categories, search_terms_list):
			print search_term
			search_terms_string = listToQueryString(attributes[attribute], [search_term])
			max_results = 600 if attribute == "diet" else 400
			results = getRecipesList(search_terms_string, max_results)

			for result in results:
				id = result["id"]
				ingredients = result["ingredients"]
				flavors = result["flavors"]
				recipe_dict = {"id":id, "ingredients":ingredients, "flavors" : flavors}
				results_dictionary = addItemToDict(category, results_dictionary, recipe_dict)


	

	with open("outfile_ingredients.json", "w+") as file:
		json.dump(results_dictionary, file) 
	
	
	#insertResults("categories", results_dictionary)
	#insertResults("recipe_ids", list(ids))


def main():
	doDownload()
	ids_to_cats, ids_to_ingredients = idsToCategories()
	print len(ids_to_ingredients)


if __name__ == "__main__":
	main()
