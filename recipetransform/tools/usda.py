import urllib, urllib2, os, json
import recipetransform.tools.database as tools
from recipetransform.tools.yummly import addItemToDict


def makeUSDARequst(endpoint, query, auth_key=None):

	if auth_key is None:
		auth_key = os.environ.get('USDAKey')
	query["api_key"] = auth_key
	query["format"] = "json"

	qstring = urllib.urlencode(query)
	url = "http://api.nal.usda.gov/usda/ndb/" + endpoint + qstring
	print url
	result_string = urllib.urlopen(url).read()
	result = json.loads(result_string)["list"]["item"]

	return [dict["name"] for dict in result]


def getFoodList(food_group, offset=0):
	
	endpoint = "search/?"
	query = {
	"fg" : food_group,
	"max" : 1000,
	"offset" : offset
	}

	result = makeUSDARequst(endpoint, query)

	if(len(result) == 1000):
		return result + getFoodList(food_group, offset+1000)
	else:
		return result


def downloadFoodGroups():
	
	endpoint = "list?"
	query = {
	"lt" : "g"
	}

	result = makeUSDARequst(endpoint, query)
	return items


def getFoodGroups():

	with open("food_groups.json", "r") as file:
		return json.load(file)


def reOrganize(food_groups):

	foods_to_foodgroups = {}
	for fg in food_groups:
		for food in food_groups[fg]:
			foods_to_foodgroups = addItemToDict(food, foods_to_foodgroups, fg)

	result = [{"food": food, "food_groups": foods_to_foodgroups[food]} for food in foods_to_foodgroups]

	return result


def getFoodGroupLists():
	
	food_groups = getFoodGroups()
	#food_groups_dicts = []
	food_groups_dict = {}

	for food_group in food_groups:

		try:
			foods = getFoodList(food_group)
		except:
			print "Can't get results: ", food_group
			continue
		food_groups_dict[food_group] = foods
		#food_groups_dicts.append({"food_group":food_group, "foods":[{"name": food} for food in foods]})

	food_groups_dicts = reOrganize(food_groups_dict)
	return food_groups_dicts


def main():

	food_groups_dicts = getFoodGroupLists()

	db = tools.DBconnect()
	db.food_groups.drop()
	for group in food_groups_dicts:
		db.food_groups.insert(group)


if __name__ == "__main__":
	main()


