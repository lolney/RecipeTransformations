from mako.template import Template
from mako.lookup import TemplateLookup

def lookup(templatename):
	mylookup = TemplateLookup(directories=['templates'])
	mytemplate = mylookup.get_template(templatename)
	return mytemplate