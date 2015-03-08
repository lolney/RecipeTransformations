import urllib, urllib2, os, json
from sets import Set
import recipetransform.tools.database as tools


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

	return urllib.quote_plus("&".join(formated_items))


def doQuery(endpoint, query, addl_parms=""):
	qstring = urllib.urlencode(query)
	url = "http://api.yummly.com/v1/api/" + endpoint + qstring + addl_parms
	result_string = urllib2.urlopen(url).read()
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
	jsonp = urllib2.urlopen(url).read()

	json_str = jsonp[ jsonp.index("[") : jsonp.rindex(")") ]
	json_obj = json.loads(json_str)

	print json_obj

	return ([getDescription(item) for item in json_obj], [item["searchValue"] for item in json_obj])


def insertResults(collection, results):
	db = tools.DBconnect()
	for result in results:
		db[collection].insert(result)


def addItemToDict(key, dict, value):

	if key in dict:
		dict[key].append(value)
	else:
		dict[key] = [value]
	return dict


def getCats():
	with open("outfile.json", "r") as file:
		return json.load(file)


def idsToCategories():

	ids = {}
	categories = getCats()

	for cat in categories:
		for id in categories[cat]:
			ids = addItemToDict(id, ids, cat)

	return ids


def doDownload():
	attributes = {"cuisine":"allowedCuisine[]"}
	results_dictionary = {}

	# diet
	categories, search_terms_list = getSearchParams("diet")
	for category, search_term in zip(categories, search_terms_list):
		print search_term
		search_terms_string = listToQueryString("allowedDiet[]", [search_term])
		results = getRecipesList(search_terms_string)

		for result in results:
			id = result["id"]
			results_dictionary = addItemToDict(category, results_dictionary, id)


	# other attributes
	for attribute in attributes:
		categories, search_terms_list = getSearchParams(attribute)
		search_terms_string = listToQueryString(attributes[attribute], search_terms_list)
		results = getRecipesList(search_terms_string, 2000)

		for result in results:
			for category in result["attributes"][attribute]:
				addItemToDict(category, results_dictionary, result["id"])
	

	with open("outfile.json", "w+") as file:
		json.dump(results_dictionary, file) 
	
	
	#insertResults("categories", results_dictionary)
	#insertResults("recipe_ids", list(ids))
