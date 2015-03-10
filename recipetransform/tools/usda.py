import urllib, urllib2, os, json
import recipetransform.tools.database as tools


def makeUSDARequst(endpoint, query):

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
	"offset" : 0
	}

	result = makeUSDARequst(endpoint, query)

	if(num_elem == 1000):
		return list_of_foods + getFoodList(food_group, offset+1000)
	else:
		return list_of_foods


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


def getFoodGroupLists():
	
	food_groups = getFoodGroups()
	food_groups_dict = {}

	for food_group in food_groups:

		foods = getFoodList(food_group)
		food_groups_dict[food_group] = foods


	return result


def main():

	food_groups_dict = getFoodGroupLists()

	db = tools.DBconnect()
	db.food_groups.drop()
	db.food_groups.insert(food_groups_dict)


if __name__ == "__main__":
	main()


