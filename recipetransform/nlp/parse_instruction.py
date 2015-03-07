"""
Find cooking methods (e.g. saute, broil, boil, poach, etc.) - primary and secondary - and tools
(Parts of speech and syntactic parsing will be important here)

"Remove the pork to a serving platter"
"into a plastic bag"
(prepositional phrases)

Probably also want to pass the ingredient list, to filter those words out,
and the name, which will be important in deciding the primary cooking method
-Luke
"""
#Kristin's attempt

def parse_instructions(instruction_list):
	#instruction =  getInstructions(parse_raw("http://allrecipes.com/Recipe/Worlds-Best-Lasagna/Detail.aspx?evt19=1&referringHubId=80"))
	instruction = instruction_list

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
			firstWord.append(words[i+1])
		elif words[0].endswith("ly"):
			firstWord.append(words[1])
		elif words[1] == u'to' and words[0].endswith("ing"):
			i = 0
			str1 = ""
			while i < len(words) and words[i] != '.' and words[i] != ';':
				str1 = str1 + " " + words[i]
				i = i + 1
			firstWord.append(str1)
		else:
			firstWord.append(words[0])
	print("All methods:\n" + str(firstWord))

	cookingMethods = ["bake", "barbecue", "boil", "braise", "broil", "fry", "grill", "microwave", "poach", "roast", "saute", "smoke", "steam"]
	primaryMethod = "none"
	for item in firstWord:
		if item.lower() in cookingMethods:
			primaryMethod = item.lower()
	print("Primary method:\n" + str(primaryMethod))

	cookingTools = ["ladle", "tongs", "spoon", "spatula", "whisk", "knife", "grater", "peeler", "garlic press", "lemon press", "shears", "can opener", 
	"corkscrew", "thermometer", "measuring cups", "salad spinners", "colander", "cutting board", "bowl", "saucepan", "pan", "baking sheet", "baking dish", "pot"]
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
	
	tools = []
	#toolDict = dict()
	for instr in instruction:
		for item in nltk.word_tokenize(instr):
			if item.lower() == "baking":
				i = 0
			if i == 1 and item.lower() == "sheet":
				tools.append("baking sheet")
			if i == 1 and item.lower() == "dish":
				tools.append("baking dish")
			if item.lower() in cookingTools:
				tools.append(item.lower())
				#toolDict[item.lower()] = 1
			elif item.lower() in toolTransDict.keys():
				tools.append(toolTransDict[item.lower()])
			i = i + 1
	
	#for x in toolDict.keys():
	#	tools.append(x)
	tools = list(set(tools))
	print("Tools:\n" + str(tools))
	return {
		"cooking method" : "primary",
		"secondary cooking methods" : ["",""],
		"cooking tools" : ["",""],
		"prep steps" : ["",""],
		"cook steps" : ["",""]
	}
