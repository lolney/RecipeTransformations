import nltk

def updateAllInstructions(instructions, old_ingredients, new_ingredients):
	new_instructions = []
	nameIngDict = dict()
	for i,ing in enumerate(old_ingredients):
		namestr = ing['name'].lower()
		if namestr not in nameIngDict:
			nameIngDict[namestr] = []

		changed = True
		new_ing = new_ingredients[i]
		if namestr == new_ing['name'].lower() and ing['descriptor'] == new_ing['descriptor']:
			changed = False
		nameIngDict[namestr].append([ing['descriptor'].lower(), changed, new_ing['name'].lower(),new_ing['descriptor'].lower().strip()])

	for instruction in instructions:
		tokens = nltk.word_tokenize(instruction.lower())
		for name in nameIngDict:
			temptokens = []
			ings = nameIngDict[name]
			choice = (len(ings)>1)
			lastmatch = -1
			matchitr  = (i for i,v in enumerate(tokens) if v == name)
			matchpos = next(matchitr,None)
			while matchpos is not None:
				descList = []
				if not choice:
					if ings[0][1]:
						descList = [x for x in nltk.word_tokenize(ings[0][0]) if x not in [',','.']]
						temptokens += repUpToIngPhrase(lastmatch, matchpos, tokens, descList, ings[0][2], ings[0][3])
				else:
					besting = None
					bestlen = 0
					bestDescList = []
					for ing in ings:
						descList = [x for x in nltk.word_tokenize(ing[0]) if x not in [',','.']]
						temppos = matchpos-1
						tempcount = 1
						while temppos > lastmatch and tokens[temppos] in descList:
							tempcount += 1
							temppos -= 1
						if tempcount > bestlen:
							besting = ing
							bestlen = tempcount
							bestDescList = descList
					if bestlen == 1:
						newings = list(set([ing[2] for ing in ings]))
						besting = ["",True, stringFromList(newings), ""]
					if besting[1]:
						temptokens += repUpToIngPhrase(lastmatch, matchpos, tokens, bestDescList, besting[2], besting[3])
				lastmatch = matchpos
				matchpos = next(matchitr,None)
			if temptokens:
				tokens = temptokens + tokens[lastmatch+1:]
		new_instructions.append(punctFriendlyJoin(tokens))
	return new_instructions

def repUpToIngPhrase(lastpos, namepos, instList, descList, newName, newDesc):
	temppos = namepos-1
	while temppos > lastpos and instList[temppos] in descList:
		temppos -= 1
	if len(newDesc) > 0:
		return instList[lastpos+1:temppos+1] + [newDesc + ' ' + newName]
	return instList[lastpos+1:temppos+1] + [newName]

def punctFriendlyJoin(lst):
	lst[0] = lst[0].title()
	for i,v in enumerate(lst):
		if i != 0 and lst[i-1] == '.':
			lst[i] = lst[i].title()
	return ''.join([' ' + x if x not in [',','.'] else x for x in lst])[1:]

def stringFromList(lst):
	if len(lst) < 2:
		return ''.join(lst)
	if len(lst) == 2:
		return ' and '.join(lst)
	if len(lst) > 2:
		return  ', '.join(lst[:-1]) + ', and ' + lst[-1]
