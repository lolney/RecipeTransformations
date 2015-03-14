import operator
import recipetransform.tools.yummly as yum 
from recipetransform.tools.dictionary_ops import addItemToDict, addDict



def findAverageTaste():
	""" Find average taste for each ingredient """
	cats = yum.getCats()
	
	ingredients_to_flavors = {}
	for cat in cats:
		for recipe in cats[cat]:
			for ingredient in recipe["ingredients"]:
				addItemToDict(ingredient, ingredients_to_flavors, recipe["flavors"])

	avg_flavors = {}
	for ingredient in ingredients_to_flavors:
		total_flavors = {}
		if len(ingredients_to_flavors[ingredient]) < 10:
			continue
		else:
			for flavors_dict in ingredients_to_flavors[ingredient]:
				if flavors_dict is None:
					continue
				for flavor in flavors_dict:
					addItemToDict(flavor, total_flavors, flavors_dict[flavor])

			averages = {}
			for flavor in total_flavors:
				averages[flavor] = sum(total_flavors[flavor]) / float(len(total_flavors[flavor]))

			if averages != {}:
				avg_flavors[ingredient] = averages

	return avg_flavors


def get5Highest(str, ids_to_flavors):

	key_maker = lambda key : lambda a : operator.itemgetter(1)(a)[key]
	return [x[0] for x in sorted(ids_to_flavors.items(), key=key_maker(str))[0:5]]


def findHighestFlavor():

	""" Find average taste for each ingredient """
	cats = yum.getCats()
	
	ids_to_flavors = {}
	for cat in cats:
		for recipe in cats[cat]:
			id = recipe["id"]
			flavors = recipe["flavors"]
			if flavors is not None:
				ids_to_flavors[id] = flavors


	print get5Highest("sweet", ids_to_flavors)
	print get5Highest("sour", ids_to_flavors)
	print get5Highest("salty", ids_to_flavors)
	print get5Highest("bitter", ids_to_flavors)
	print get5Highest("meaty", ids_to_flavors)


def printHighest():

	avg_flavors = findAverageTaste()

	key_maker = lambda key : lambda a : operator.itemgetter(1)(a)[key]
	print max(avg_flavors.items(), key=key_maker("sweet"))
	print max(avg_flavors.items(), key=key_maker("sour"))
	print max(avg_flavors.items(), key=key_maker("salty"))
	print max(avg_flavors.items(), key=key_maker("bitter"))
	print max(avg_flavors.items(), key=key_maker("meaty"))	


def main():

	findHighestFlavor()



if __name__ == "__main__":
	main()



