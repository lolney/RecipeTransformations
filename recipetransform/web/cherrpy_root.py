import cherrypy
import urllib, ast
import recipetransform.nlp.parsing as parsing
import recipetransform.tools.templates as templates
import recipetransform.web.allrecipes as allrecipes
from recipetransform.nlp.transform_recipe import transform_recipe
import recipetransform.tools.database as tools


def getRecipe(kwargs):

	ingredients = [];
	for item in kwargs["ingredients"]: # Cherrypy turns the dictionaries into strings
		ingredients.append(ast.literal_eval(item))

	# Need to wrap in list, if necessary
	cook_steps = kwargs["cook steps"]
	cook_steps = cook_steps if type(cook_steps) == type([]) else [cook_steps]

	prep_steps = kwargs["prep steps"]
	prep_steps = prep_steps if type(prep_steps) == type([]) else [prep_steps]

	return ingredients, cook_steps, prep_steps


def getTransformCategories():

	db = tools.DBconnect()

	query1 = {"ingredients": {"$elemMatch" : {"transform_type" : "cuisine"}}}
	query2 = {"ingredients": {"$elemMatch" : {"transform_type" : "diet"}}}
	projection = {"_id": 0, 'ingredients.$': 1}

	cuisines = db.posteriors.find(query1, projection).limit(1)[0]["ingredients"][0]
	diets = db.posteriors.find(query2, projection).limit(1)[0]["ingredients"][0]

	getItems = lambda items : [item for item in items if item not in ["ingredient","transform_type","_id"]]
	print getItems(cuisines)

	return [
		{"Name" : "Diet", "Categories" : getItems(diets)},
		{"Name" : "Cuisine", "Categories" : getItems(cuisines)},
		{"Name" : "Sodium", "Categories" : ["Low","High"]},
		{"Name" : "Calories", "Categories" : ["Low","High"]}
	]
	


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
	def parsed_recipe(self, **kwargs):

		ingredients, cook_steps, prep_steps = getRecipe(kwargs)

		mytemplate = templates.lookup('recipe.html')
		return mytemplate.render(title=kwargs["name"],
			ingredients=ingredients,
			prep_steps=prep_steps,
			cook_steps=cook_steps,
			transform_categories=getTransformCategories())

	@cherrypy.expose
	def search(self, q=""):
		recipe_dict = parsing.parseHtml(q)
		qstring = urllib.urlencode(recipe_dict, doseq=True)
		print qstring
		raise cherrypy.HTTPRedirect("/parsed_recipe?" + qstring)


	@cherrypy.expose
	def replace(self, **kwargs):

		ingredients, cook_steps, prep_steps = getRecipe(kwargs)
		cat = kwargs[transform_category]
		typ = kwargs[transform_type]
		
		ingredients, instructions = transform_recipe(ingredients, cook_steps+prep_steps, cat, typ)

		raise cherrypy.HTTPRedirect("/parsed_recipe?" + "")



