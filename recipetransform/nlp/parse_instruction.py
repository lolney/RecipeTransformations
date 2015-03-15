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
	"corkscrew", "thermometer", "measuring cups", "salad spinners", "colander", "cutting board", "bowl", "saucepan", "pan", "baking sheet", "baking dish", "pot", "skillet", "fork", "forks", "oven", "griddle"]
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
	
	tools = []
	i = 0
	j = 0
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
			elif item.lower() in toolTransDict.keys():
				tools.append(toolTransDict[item.lower()])
			i = i + 1
			j = j + 1


	if primaryMethod == "none" and "cook" in firstWord:
		primaryMethod = "cook"

	#print("Primary method:\n" + str(primaryMethod))
	tools = list(set(tools))
	#print("Tools:\n" + str(tools))


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

	instrDict = dict()
	instrDict["allMethods"] = firstWord1
	instrDict["primaryMethod"] = primaryMethod
	instrDict["tools"] = tools
	instrDict["steps"] = stepList

	print("\nPrimary Method:\n" + instrDict["primaryMethod"])
	print("All Methods:\n" + str(instrDict["allMethods"]))
	print("Tools:\n" + str(instrDict["tools"]))
	print("Steps:\n" + str(instrDict["steps"]))


	return {
		"cooking method" : primaryMethod,
		"secondary cooking methods" : firstWord1,
		"cooking tools" : tools,
		"cook steps" : stepList
	}
