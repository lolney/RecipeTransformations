import cherrypy
import urllib, ast
import recipetransform.nlp.parsing as parsing
import recipetransform.tools.templates as templates
import recipetransform.web.allrecipes as allrecipes


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
			transform_categories=[
			{"Name" : "Diet", "Categories" : ["Vegan", "Vegetarian"]},
			{"Name" : "Cuisine", "Categories" : ["Italian", "French"]}
			])

	@cherrypy.expose
	def parsed_recipe(self, **kwargs):

		ingredients = [];
		for item in kwargs["ingredients"]: # Cherrypy turns the dictionaries into strings
			ingredients.append(ast.literal_eval(item))

		# Need to wrap in list, if necessary
		cook_steps = kwargs["cook steps"]
		cook_steps = cook_steps if type(cook_steps) == type([]) else [cook_steps]

		prep_steps = kwargs["prep steps"]
		prep_steps = prep_steps if type(prep_steps) == type([]) else [prep_steps]

		mytemplate = templates.lookup('recipe.html')
		return mytemplate.render(title=kwargs["name"],
			ingredients=ingredients,
			prep_steps=prep_steps,
			cook_steps=cook_steps,
			transform_categories=[
			{"Name" : "Diet", "Categories" : ["Vegan", "Vegetarian"]},
			{"Name" : "Cuisine", "Categories" : ["Italian", "French"]}
			])

	@cherrypy.expose
	def search(self, q=""):
		recipe_dict = parsing.parseHtml(q)
		qstring = urllib.urlencode(recipe_dict, doseq=True)
		print qstring
		raise cherrypy.HTTPRedirect("/parsed_recipe?" + qstring)

