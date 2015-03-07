import urllib, urllib2, os, json
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

	return "&".join(formated_items)


def doQuery(endpoint, query, addl_parms=""):
	qstring = urllib.urlencode(query)
	url = "http://api.yummly.com/v1/api/" + endpoint + qstring + addl_parms
	result_string = urllib2.urlopen(url).read()
	result = json.loads(result_string)

	return result


def getRecipesList(search_params):
	# do a query for every category we might want

	query = getAuthInfo()
	query["allowedCuisine[]"] = "cuisine^cuisine-american"

	return doQuery("recipes?", query)["matches"]

	#return recipe_ids


def getRecipe(id):
	query = getAuthInfo()

	return doQuery("recipe/" + id + "?", query)


def getSearchParams(category):
	endpoint = "metadata/" + category + "?"
	query = getAuthInfo()
	qstring = urllib.urlencode(query)
	url = "http://api.yummly.com/v1/api/" + endpoint + qstring
	jsonp = urllib2.urlopen(url).read()

	json_str = jsonp[ jsonp.index("[") : jsonp.rindex(")") ]
	json_obj = json.loads(json_str)

	return ([item["shortDescription"] for item in json_obj], [item["searchValue"] for item in json_obj])


def insertResults(result):
	db = tools.DBconnect()
	db.recipes.insert(result)


def doDownload():
	diets, diet_search_terms = getSearchParams("diet")
	cuisines, cuisine_search_terms = getSearchParams("cuisine")

	for category in categories:
		search_terms = listToQueryString(cuisine_search_terms)
		results = getRecipesList(search_terms)
		for recipe in results:
			id = recipe["id"]
			getRecipe(id)