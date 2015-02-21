import cherrypy
import urllib, ast
import src.nlp.parsing as parsing
import src.tools.templates as templates


class Root(object):
	@cherrypy.expose
	def index(self):
		mytemplate = templates.lookup('index.html')
		return mytemplate.render()

	@cherrypy.expose
	def recipes(self, name="Cherry Pie"):
		mytemplate = templates.lookup('recipe.html')
		return mytemplate.render(title=name,
			ingredients=[{"q":"1","n":"Coffee"}],
			instructions=["Put the egg in the milk", "Put the jam in the marshmellow"],
			transform_categories=[{"Name" : "Varieties", "Categories" : ["Italian", "French"]}])

	@cherrypy.expose
	def parsed_recipe(self, **kwargs):

		ingredients = [];
		for item in kwargs["ingredients"]: # Cherrypy turns the dictionaries into strings
			ingredients.append(ast.literal_eval(item))

		mytemplate = templates.lookup('recipe.html')
		return mytemplate.render(title=kwargs["name"],
			ingredients=ingredients,
			instructions=kwargs["instructions"],
			transform_categories=[{"Name" : "Varieties", "Categories" : ["Italian", "French"]}])

	@cherrypy.expose
	def search(self, q=""):
		recipe_dict = parsing.parseHtml(q)
		qstring = urllib.urlencode(recipe_dict, doseq=True)
		print qstring
		raise cherrypy.HTTPRedirect("/parsed_recipe?" + qstring)

