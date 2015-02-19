import cherrypy
import src.nlp.parsing as parsing
import src.tools.templates as templates
from mako.template import Template
from mako.lookup import TemplateLookup


class Root(object):
	@cherrypy.expose
	def index(self):
		mytemplate = lookup('index.html')
		return mytemplate.render()

	@cherrypy.expose
	def recipes(self, name="Cherry Pie"):
		mytemplate = templates.lookup('recipe.html')
		return mytemplate.render(title=name,
			ingredients=["Coffee","Tea","Milk"],
			instructions=["Put the egg in the milk"],
			transform_categories=[{"Name" : "Varieties", "Categories" : ["Italian", "French"]}])

	@cherrypy.expose
	def search(self, q=""):
		qstring = parsing.parseHtml(q)
		raise cherrypy.HTTPRedirect("/recipes/" + qstring)

