import urllib2, os

def getRecipesList():

	app_id = os.environ.get('YummlyId')
	auth_key = os.environ.get('YummlyKey')

	# do a query for every category we might want
	query = {
	"_app_id":app_id,
	"_app_key":auth_key,
	"allowedCuisine":["American", "Italian", "Asian", "Mexican"]
	}


	return recipe_ids


# Do we need to use getRecipe to get the ingredientLines, which is more descriptive?	
def downloadRecipe(x):

	app_id = os.environ.get('YummlyId')
	auth_key = os.environ.get('YummlyKey')

	# query for recipe id x

	return (data, categories)