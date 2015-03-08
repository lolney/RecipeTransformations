from BeautifulSoup import BeautifulSoup
#from recipetransform.nlp.parse_instruction import parse_instruction
#from recipetransform.nlp.parse_ingredient import parse_ingredient
import parse_ingredient
import parse_instruction
import urllib2
import nltk
import sys

def parse_raw(url):

	resp = urllib2.urlopen(url)
	html = resp.read();
	parsed_html = BeautifulSoup(html)

	return parsed_html

def getIngredients(html):
	content = html.body.find(id='zoneIngredients')

	ingredient_lis = content.findAll(id='liIngredient')

	ingredients = []
	for ingredient in ingredient_lis:
		try:
			ingredient_amount = ingredient.find('span', attrs={'class':'ingredient-amount'}).text
			ingredient_name = ingredient.find('span', attrs={'class':'ingredient-name'}).text
			parsed_ingred = {"q": ingredient_amount, "n": ingredient_name}
			#parsed_ingred = parse_ingredient(ingredient_amount, ingredient_name)
			ingredients.append(parsed_ingred)
		except AttributeError: # expected, because some table elements contain no ingredients
			pass

	return ingredients


def getInstructions(html):
	content = html.body.find('div', attrs={'class':'directions'})

	instruction_lis = content.findAll('li')

	instructions = []
	for instruction in instruction_lis:
		instruction_text = instruction.find('span').text;
		#parsed_ingred = parse_instruction(instruction_text)
		instructions.append(instruction_text)

	return instructions


def getName(html):
	return html.body.find(id="itemTitle").text


def parseHtml(url):

	parsed_html = parse_raw(url)

	name = getName(parsed_html)
	ingredients = getIngredients(parsed_html)
	instructions = getInstructions(parsed_html)

	return {"name" : name, "ingredients" : ingredients, "instructions" : instructions}


def main():
	html = str(sys.argv[1])
	#instruction =  getInstructions(parse_raw("http://allrecipes.com/Recipe/Carrot-Cupcakes-with-White-Chocolate-Cream-Cheese-Icing/Detail.aspx?soid=home_pins_3"))
	#instruction =  getInstructions(parse_raw("http://allrecipes.com/Recipe/Sausage-and-Shrimp-Gumbo/Detail.aspx?soid=carousel_0_rotd&prop24=rotd"))
	#instruction =  getInstructions(parse_raw("http://allrecipes.com/Recipe/Camp-Cornbread/Detail.aspx?evt19=1&referringHubId=342"))
	#instruction =  getInstructions(parse_raw("http://allrecipes.com/Recipe/Worlds-Best-Lasagna/Detail.aspx?evt19=1&referringHubId=80"))
	#instruction = getInstructions(parse_raw("http://allrecipes.com/Recipe/Slow-Cooker-Carolina-BBQ/Detail.aspx?evt19=1&referringHubId=17678"))
	#name = getName(parse_raw("http://allrecipes.com/Recipe/Slow-Cooker-Carolina-BBQ/Detail.aspx?evt19=1&referringHubId=17678"))
	
	instruction = getInstructions(parse_raw(html))
	name = getName(parse_raw(html))
	
	name = nltk.word_tokenize(name)

	temp1 = []
	for instr in instruction:
		temp = instr.split('.')
		for inst in temp:
			if not(inst == ""):
				temp1.append(inst)
	temp2 = []
	for instr in temp1:
		temp3 = instr.split(';')
		for inst in temp3:
			if not(inst == ""):
				temp2.append(inst)
	firstWord = []
	for instr in temp2:
		#print(nltk.pos_tag(nltk.word_tokenize(instr)))
		#if not (instr == ""):
		words = nltk.word_tokenize(instr)
		if words[0] == u'In' or words[0] == u'To':
			i = 0
			while words[i] != u',':
				i = i + 1
			firstWord.append(words[i+1].lower())
		elif words[0].endswith("ly") and len(words) > 1:
			firstWord.append(words[1].lower())
		elif len(words) > 1 and words[1] == u'to' and words[0].endswith("ing"):
			i = 0
			str1 = ""
			while i < len(words) and words[i] != '.' and words[i] != ';':
				str1 = str1 + " " + words[i]
				i = i + 1
			firstWord.append(str1.lower())
		else:
			firstWord.append(words[0].lower())
	print("All methods:\n" + str(firstWord))

	cookingMethods = ["bake", "baked", "barbecue", "barbecued", "boil", "boiled", "braise", "braised", "broil", "broiled", "fry", "fried" "grill", "grilled" "microwave", "microwaved", "poach", "poached", "roast", "roasted", "saute", "sauted", "smoke", "smoked", "steam", "steamed"]
	primaryMethod = "none"
	for item in firstWord:
		if item.lower() in cookingMethods:
			primaryMethod = item.lower()
	i = 0
	for item in name:
		if item.lower() == "slow":
			i = 0
		if i == 1 and item.lower() == "cooker":
			primaryMethod = "slow cooker"
		if item.lower() in cookingMethods:
			primaryMethod = item.lower()
		i = i + 1

	

	cookingTools = ["ladle", "tongs", "spoon", "spatula", "whisk", "knife", "grater", "peeler", "garlic press", "lemon press", "shears", "can opener", 
	"corkscrew", "thermometer", "measuring cups", "salad spinners", "colander", "cutting board", "bowl", "saucepan", "pan", "baking sheet", "baking dish", "pot", "skillet", "fork", "forks", "oven"]
	toolTransDict = dict()
	toolTransDict["cut"] = "knife"
	toolTransDict["dice"] = "knife"
	toolTransDict["chop"] = "knife"
	toolTransDict["peel"] = "peeler"
	toolTransDict["stir"] = "spoon"
	toolTransDict["beat"] = "beaters"
	#toolTransDict["boil"] = "pot"
	toolTransDict["saute"] = "pan"
	toolTransDict["bake"] = "oven"
	toolTransDict["cupcake"] = "muffin tin"
	toolTransDict["muffin"] = "muffin tin"
	toolTransDict["fold"] = "spatula"
	toolTransDict["grate"] = "grater"
	toolTransDict["refrigerate"] = "refrigerator"
	
	tools = []
	i = 0
	j = 0
	#toolDict = dict()
	for instr in instruction:
		for item in nltk.word_tokenize(instr):
			if item.lower() == "baking":
				i = 0
			if i == 1 and item.lower() == "sheet":
				tools.append("baking sheet")
			if i == 1 and item.lower() == "dish":
				tools.append("baking dish")
			if item.lower() == "slow":
				j = 0
			if j == 1 and item.lower() == "cooker":
				tools.append("slow cooker")
				primaryMethod = "slow cooker"
			if item.lower() in cookingTools:
				tools.append(item.lower())
				#toolDict[item.lower()] = 1
			elif item.lower() in toolTransDict.keys():
				tools.append(toolTransDict[item.lower()])
			i = i + 1
			j = j + 1

	print("Primary method:\n" + str(primaryMethod))
	#for x in toolDict.keys():
	#	tools.append(x)
	tools = list(set(tools))
	print("Tools:\n" + str(tools))


	#STEPS

	foodDict = dict()
	foodDict["bell pepper"] = [["1", "fresh red", ["chopped"], ["finely"]]]
	timeWords = ["minutes", "seconds", "minute", "second", "hour", "hours"]
	foodDict["potatoes"] = [["1 ounce", "cheesy", ["sliced"], []]]
	for key in foodDict.keys():
		print(nltk.word_tokenize(key))

	stepList = []
	i = 0
	j = 0
	k = 0
	l = 0
	for instr in temp2:
		#words = nltk.word_tokenize(instr)
		method = firstWord[k]
		k = k + 1
		stepTools = []
		stepIngred = []
		stepTime = ""
		timeFlag = 0
		perFlag = 0
		index = 0
		for item in nltk.word_tokenize(instr):
			if perFlag == 1:
				stepTime = stepTime + item.lower()
				perFlag = 0
			elif l != 2 and item > "0" and item < "99":
				l = 0
				stepTime = item + " "
			elif l == 1 and item.lower() == u'to':
				stepTime = stepTime + item.lower() + " "
			elif l == 2 and item > "0" and item < "99":
				stepTime = stepTime + item + " "
			elif (l >= 1 or l <= 3) and item.lower() in timeWords:
				stepTime = stepTime + item.lower()
				timeFlag = 1
			elif (l == 2 or l == 4) and timeFlag == 1 and item.lower() == "per":
				stepTime = stepTime + " per "
				perFlag = 1
			if item.lower() == "baking":
				i = 0
			if i == 1 and item.lower() == "sheet":
				stepTools.append("baking sheet")
			if i == 1 and item.lower() == "dish":
				stepTools.append("baking dish")
			if item.lower() == "slow":
				j = 0
			if j == 1 and item.lower() == "cooker":
				stepTools.append("slow cooker")
				#primaryMethod = "slow cooker"
			if item.lower() in cookingTools:
				stepTools.append(item.lower())
			elif item.lower() in toolTransDict.keys():
				stepTools.append(toolTransDict[item.lower()])
			i = i + 1
			j = j + 1
			l = l + 1
			for key in foodDict.keys():
				if item.lower() in nltk.word_tokenize(key):
					if len(foodDict[key]) > 1:
						for item in foodDict[key]:
							if nltk.word_tokenize(instr)[index-1] in nltk.word_tokenize(item[1]):
								stepIngred.append(str(item[1] + " " + key))
					else:
						stepIngred.append(key)
			index = index + 1
		#stepDict = dict()
		if timeFlag == 0:
			stepTime = ""
		stepList.append([method, stepIngred, stepTools, stepTime])
	print(stepList)
		










if __name__ == "__main__":
    main()   
