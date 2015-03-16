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

import sys
import nltk
import re


def regexSearch(keywords, text):

	regex = "|".join([r'\b' + method for method in keywords])
	regex = re.compile(regex, re.IGNORECASE)
	return re.findall(regex, text)


def primaryMethodDecisionTree(firstWord, methods_found, instructions, tools, name_str):
	"""
	Classifiers are expensive to train. Here are some heuristics that I think approximate
	how a well-trained decision tree or maximum entropy classifier would look
	"""
	
	primaryMethods = ["bake","grill","simmer","cook","slow cook","stir-fry","fry","roast","saute","broil"]
	primary_method_candidates = set(primaryMethods).intersection(set(methods_found))
	candidates_in_name = regexSearch(methods_found, name_str)

	# first check in name
	if len(candidates_in_name) > 0:
		# try to disambiguate by looking for primary methods
		if len(candidates_in_name) > 1:
			first_word_primaries = set(firstWord).intersection(set(primaryMethods))
			if len(first_word_primaries) > 0:
				return first_word_primaries[0]
		
		return candidates_in_name[0]

	# next, check for keywords
	if "oven" in tools:
		if "bake" in methods_found:
			return "bake"
	if "grill" in tools:
		if "grill" in methods_found:
			return "grill"

	# next, check for temperature
	temperatureRegex = "(medium[- ]low)|((?<!medium[- ])low)|(medium(?![- ]low))"
	regex = re.compile(temperatureRegex, re.IGNORECASE)
	matches = regex.search(instructions)

	med_low = matches.group(0) if matches else None
	low = matches.group(1) if matches else None
	med = matches.group(2) if matches else None

	# look for primary methods in the first words
	filtered_candidates = set(firstWord).intersection(primary_method_candidates)
	if len(filtered_candidates) > 0:
		if len(filtered_candidates) > 1:
			if med_low or low:
				if "slow cook" in methods_found:
					return "slow cook"
				if "simmer" in methods_found:
					return "simmer"
			if med and not (low or med_low):
				if "cook" in methods_found:
					return "cook"

		return list(filtered_candidates)[0]

	# finally, look for primary methods generally
	if len(primary_method_candidates) > 0:
		if len(filtered_candidates) > 1:
			if med_low or low:
				if "slow cook" in methods_found:
					return "slow cook"
				if "simmer" in methods_found:
					return "simmer"
			if med and not (low or med_low):
				if "cook" in methods_found:
					return "cook"

		return list(primary_method_candidates)[0]

	# if nothing succeeds, return none
	return "none"




def parse_instruction(list_of_str, name_str, foodDict):
	
	instruction = list_of_str
	
	name = nltk.word_tokenize(name_str)

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
			while i < len(words) and words[i] != '.' and words[i] != ';' and words[i] != ',':
				str1 = str1 + " " + words[i]
				i = i + 1
			firstWord.append(str1.lower())
		else:
			firstWord.append(words[0].lower())
	firstWord1 = list(set(firstWord))
	#print("\nAll methods:\n" + str(firstWord1))

	cookingMethods = ["bake", "baked", "barbecue", "barbecued", "boil", "boiled", "braise", "braised", "broil", "broiled",
	 "(?<!stir[- ])fry", "fried", "grill", "grilled" "microwave", "microwaved", "poach", "poached", "roast", "roasted", "saute", "sauted",
	 "smoke", "smoked", "steam", "steamed", r"stir[ -]fry", "season", "stir", "drain", "arrange", "cool", "simmer", "rinse",
	 "remove", "preheat", "mix", "whip", "mince", "knead", "grind", "glaze", "combine", "cut", "dice", "chop", "peel",
	 "cover", "beat", "grate", "serve", "form", "pour", "dissolve", "whisk", "blend", "add", "place", "heat", "tenderize",
	 "mash", "set", "insert", "cream", "spoon", "brush", "soak", "sift", "(?<!french )toast", "sprinkle", "fold", "drop",
	 "transfer", "turn", "shake", "mince", "crush", "squeeze", "flip","melt","coat", "spread", "marinate", "barbeque",
	 "spray", r"fill\b", "clean", r"reduce\b", "chill", "garnish", "warm", r"crumble\b", "flatten", "knead", r"divide\b",
	 "bring", "slow cook", "refrigerate", "split", r"cook\b", "peel", "toss", "puree", "pulse", "spoon off", "deglaze",
	 "pierce",r"tie\b","scatter","pat\b","scrape","trim"]
	
	# Search for cooking methods
	text = " ".join([name_str] + instruction)
	methods_found = regexSearch(cookingMethods, text)
	methods_found = [mth.lower() for mth in methods_found]
	
	

	cookingTools = ["ladle", "tongs", "spoon", "spatula", "whisk", "knife", "grater", "peeler", "wok",
	"garlic press", "lemon press", "shears", "can opener", "corkscrew", "thermometer", "measuring cup",
	"salad spinners", "colander", "cutting board", "bowl", "saucepan", "(?<!frying|baking)pan", "baking sheet",
	"baking dish", "pot", "skillet", "fork", "forks", "oven", "griddle", "microwave", "hot plate",
	"rice cooker", "baster", "cookie cutter", "pastry brush", "rolling pin", "sieve", "stove", "oven",
	r"(?<=the )grill", "tin", "tongs", "cookie sheet", "plate", "bag", "foil", "blender", "mixer", "slow cooker",
	"refrigerator", "liner", "toothpick", "cooking spray", "container", "waffle iron", "towel", 
	"roasting rack", "deep fryer", "steamer", "meat grinder", "cutting plate", "paper towel", "Dutch oven",
	"stockpot","sauceboat","skewer","string","frying pan","baking pan"]
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
	toolTransDict["cupcake"] = "muffin pan"
	toolTransDict["muffin"] = "muffin pan"
	toolTransDict["fold"] = "spatula"
	toolTransDict["grate"] = "grater"
	toolTransDict["refrigerate"] = "refrigerator"
	toolTransDict["measure"] = "measuring cup"
	
	tools = regexSearch(cookingTools, " ".join(instruction))
	tools = [tool.lower() for tool in tools]

	for instr in instruction:
		for item in nltk.word_tokenize(instr):
			if item.lower() in toolTransDict.keys():
				tools.append(toolTransDict[item.lower()])


	#print("Primary method:\n" + str(primaryMethod))
	tools = list(set(tools))
	#print("Tools:\n" + str(tools))

	# Find primary method
	primaryMethod = primaryMethodDecisionTree(firstWord, methods_found, " ".join(instruction), tools, name_str)

	#STEPS

	#foodDict = dict()
	#foodDict["peppers"] = [["2", "green bell", ["sliced"], []], ["1", "red bell", ["sliced"], []]]
	#foodDict["onion"] = [["1", "", ["sliced"], ["thinly"]]]
	#foodDict["mix"] = [["1", "package dry Italian-style salad dressing", [], []]]
	#foodDict["mushrooms"] = [["1 cup", "fresh", ["sliced"], []]]
	#foodDict["potatoes"] = [["1 ounce", "cheesy", ["sliced"], []]]

	timeWords = ["minutes", "seconds", "minute", "second", "hour", "hours"]
	
	#for key in foodDict.keys():
	#	print(nltk.word_tokenize(key))

	stepList = []
	i = 0
	j = 0
	k = 0
	l = 0
	for instr in temp2:
		method = firstWord[k]
		k = k + 1
		stepTools = []
		stepIngred = []
		stepTime = ""
		untilInstr = ""
		timeFlag = 0
		perFlag = 0
		index = 0
		m = 0
		for item in nltk.word_tokenize(instr):
			if item.lower() in [",", ";", ".", "and"]:
				m = 0
			if m == 1:
				untilInstr = untilInstr + " " + item.lower()
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
			if item.lower() == "until":
				m = 1
				untilInstr = "until"
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
						n = 0
						for item1 in foodDict[key]:
							if nltk.word_tokenize(instr)[index-1] in nltk.word_tokenize(item1[1]):
								stepIngred.append(str(item1[1] + " " + key))
								n = 1
							if n == 0:
								n = 1
								stepIngred.append(item.lower())
					elif len(nltk.word_tokenize(key)) > 1:
						if len(nltk.word_tokenize(instr)) > (index + 1) and nltk.word_tokenize(key)[1] == nltk.word_tokenize(instr)[index + 1]:
							stepIngred.append(key)
					else:
						stepIngred.append(key)
			index = index + 1
		if timeFlag == 0:
			stepTime = ""
		if stepTime == "":
			stepTime = untilInstr
		elif not(stepTime == "") and not(untilInstr == ""):
			stepTime = stepTime + " or " + untilInstr
		stepList.append([method, stepIngred, stepTools, stepTime])
	#print("Steps:")
	#print(stepList)

	instrDict =  {
		"cooking method" : primaryMethod.lower(),
		"secondary cooking methods" : list(set(firstWord1 + methods_found)),
		"cooking tools" : tools,
		"cook steps" : stepList
	}
	"""
	for key in instrDict:
		print key + ": ", instrDict[key]"""

	return instrDict

