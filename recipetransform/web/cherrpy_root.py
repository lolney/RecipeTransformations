import cherrypy
import urllib, ast, json
import recipetransform.nlp.parsing as parsing
import recipetransform.tools.templates as templates
import recipetransform.web.allrecipes as allrecipes
from recipetransform.nlp.transform_recipe import transform_recipe
import recipetransform.tools.database as tools


def getRecipe(url):

	db = tools.DBconnect()
	recipe_dict = db.recipe_cache.find_one({"url" : url})

	if recipe_dict is None:
		recipe_dict = parsing.parseHtml(url)
		recipe_dict["url"] = url
		db.recipe_cache.insert(recipe_dict)

	# Need to wrap in list, if necessary
	instructions = recipe_dict["instructions"]
	instructions = instructions if type(instructions) == type([]) else [instructions]

	return recipe_dict["name"], instructions, recipe_dict["ingredients"]
	


def getTransformCategories(transform_category=None):

	db = tools.DBconnect()

	query1 = {"ingredients": {"$elemMatch" : {"transform_type" : "cuisine"}}}
	query2 = {"ingredients": {"$elemMatch" : {"transform_type" : "diet"}}}
	projection = {"_id": 0, 'ingredients.$': 1}

	cuisines = db.posteriors.find(query1, projection).limit(1)[0]["ingredients"][0]
	diets = db.posteriors.find(query2, projection).limit(1)[0]["ingredients"][0]

	getItems = lambda items : [item for item in items if item not in ["ingredient","transform_type","_id"]]

	diets = getItems(diets)
	cuisines = getItems(cuisines)

	return [
		{"Name" : "Diet", "Categories" : diets},
		{"Name" : "Cuisine", "Categories" : cuisines},
		{"Name" : "Sodium", "Categories" : ["Low","High"]},
		{"Name" : "Calories", "Categories" : ["Low","High"]}
	]

def getIngredientStrings(ingredients):

	ingredient_strings = []
	for ingredient in ingredients:
		"""
		preps = []
		for i in range(len(ingredient["prep_descriptor"])):
			preps.append(ingredient["preparation"][i] + " " + ingredient["prep_descriptor"][i])
		print ingredient
		ingredient["preparation"] = preps"""
		string = " ".join([str(ingredient["quantity"])[:4], ingredient["measurement"], ingredient["descriptor"], ingredient["name"]])
		ingredient_strings.append(string)

	return ingredient_strings
	

class Root(object):
	@cherrypy.expose
	def index(self):
		mytemplate = templates.lookup('index.html')
		return mytemplate.render()

	@cherrypy.expose
	def random(self):
		url = allrecipes.random_recipe()
		raise cherrypy.HTTPRedirect("/search?q=" + urllib.quote_plus(url))

	@cherrypy.expose
	def recipes(self, name="Cherry Pie"):
		mytemplate = templates.lookup('recipe.html')
		return mytemplate.render(title=name,
			ingredients=[{"q":"1","n":"Coffee"}],
			instructions=["Put the egg in the milk", "Put the jam in the marshmellow"],
			transform_categories=getTransformCategories())

	@cherrypy.expose
	def search(self, q=""):

		name, instructions, ingredients = getRecipe(q)

		ingredient_strings = getIngredientStrings(ingredients)

		print ingredients

		mytemplate = templates.lookup('recipe.html')
		return mytemplate.render(title=name,
			ingredients=ingredient_strings,
			url=q,
			instructions=instructions,
			transformation="",
			transform_categories=getTransformCategories())

	"""
	@cherrypy.expose
	def replace(self, **kwargs):

		cat = kwargs["transform_category"]
		typ = kwargs["transform_type"]
		
		cook_steps, prep_steps = getRecipe(kwargs)
		transformed_recipe = transform_recipe(ingredients, cook_steps+prep_steps, cat, typ)
		
		transformed_recipe = {"instructions":cat, "ingredients": typ}
		return json.dumps(transformed_recipe)
	"""

	@cherrypy.expose
	def replace(self, **kwargs):

		name, instructions, ingredients = getRecipe(kwargs["q"])

		cat = kwargs["transform_category"]
		typ = kwargs["transform_type"].lower()
		
		ingredients, instructions = transform_recipe(ingredients, instructions, cat, typ)

		ingredient_strings = getIngredientStrings(ingredients)

		mytemplate = templates.lookup('recipe.html')
		return mytemplate.render(title=name,
			ingredients=ingredient_strings,
			url=kwargs["q"],
			transformation=cat,
			instructions=instructions,
			transform_categories=getTransformCategories(cat))




