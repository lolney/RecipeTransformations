from recipetransform.nlp.parsing import parserProgramInterface

def testPrimaryMethod():

	urls = [
	{
		"url":"http://allrecipes.com/Recipe/Delicious-Ham-and-Potato-Soup/",
		"method":"cook"
	},
	{
		"method":"simmer",
		"url":"http://allrecipes.com/Recipe/Catherines-Spicy-Chicken-Soup/"
	},
	{
		"method":"bake",
		"url":"http://allrecipes.com/Recipe/Ultimate-Twice-Baked-Potatoes/"
	},
	{
		"method":"roast",
		"url":"http://allrecipes.com/Recipe/Roast-Sticky-Chicken-Rotisserie-Style/"
	},
	{
		"method":"none",
		"url":"http://allrecipes.com/Recipe/Best-Bread-Machine-Bread/"
	},
	{
		"method":"slow cook",
		"url":"http://allrecipes.com/Recipe/Slow-Cooker-Pulled-Pork/"
	},
	{
		"method":"bake",
		"url":"http://allrecipes.com/Recipe/Classic-Peanut-Butter-Cookies/"
	},
	{
		"method":"bake",
		"url":"http://allrecipes.com/Recipe/Black-Magic-Cake/"
	},
	{
		"method":"cook",
		"url":"http://allrecipes.com/Recipe/Fluffy-French-Toast/"
	},
	{
		"method":"cook",
		"url":"http://allrecipes.com/Recipe/Awesome-Sausage-Apple-and-Cranberry-Stuffing/"
	},
	{
		"method":"bake",
		"url":"http://allrecipes.com/Recipe/Moms-Irish-Soda-Bread/"
	},
	{
		"method":"grill",
		"url":"http://allrecipes.com/Recipe/Yummy-Honey-Chicken-Kabobs/"
	},
	{
		"method":"bake",
		"url":"http://allrecipes.com/Recipe/One-Bowl-Chocolate-Cake-III/"
	},
	{
		"method":"simmer",
		"url":"http://allrecipes.com/Recipe/Broccoli-Cheese-Soup/"
	}]

	count = 0
	for item in urls:
		result = parserProgramInterface(item["url"])
		print item["url"], ": "
		print result["primary cooking method"], item["method"]
		print ""
		if result["primary cooking method"] == item["method"]:
			count = count + 1

	print "=== Accuracy"
	print "===", count/float(len(urls))