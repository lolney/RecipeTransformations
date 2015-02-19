def lookup(templatename):
	mylookup = TemplateLookup(directories=['templates'])
	mytemplate = mylookup.get_template(templatename)
	return mytemplate