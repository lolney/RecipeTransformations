""" Break down ingredients as specified in inferface below 

Quantity and descriptor should be easy - these are contained in the quantity_string. 
The rest will be a bit harder, but we can probably use pos and syntactic parsing:

words that indicate preparation:
minced lemon zest		<- participle
pork tenderloin, cut into 1 1/2 inch pieces 	<- participle phrase
"""
import nltk, re

def convert_ingredient(name,parse_list):
	quant_list = parseQuantity(parse_list[0])
	return {
		"name":	name,
		"quantity":	quant_list[0],
		"measurement":	quant_list[1],
		"descriptor":	parse_list[1],
		"preparation":	parse_list[2],
		"prep_descriptor": parse_list[3]
	}

def parseQuantity(string):
	string = re.sub(r"\(.*\)","",string)
	tokens = re.split(r"\s+(?=[a-zA-Z])", string)
	quantity = tokens[0]
	if re.search(r"\d+/\d+", quantity) is not None:
		ints = re.split(r"[\s+/]", quantity)
		if len(ints) == 2:
			quantity = float(ints[0]) / float(ints[1])
		elif len(ints) == 3:
			quantity = float(ints[0]) + (float(ints[1]) / float(ints[2]))
	elif re.search("[Oo]ne", quantity) is not None:
		quantity = 1
	return [float(quantity)," ".join(tokens[1:])]

def parseIngredient(string):
	string = string.replace(', or more to taste','')
	string = string.replace(' to taste','')
	string = string.replace(', or more as needed','')
	pos_str = nltk.pos_tag(nltk.word_tokenize(u"Add in the " + unicode(string)))[3:]
	pos_str = punctSanitize(pos_str)
	VBNitr = (i for i, v in enumerate(pos_str) if v[1] == 'VBN' or v[1] == 'VBD')
	VBNnext = next(VBNitr,None)
	
	if VBNnext is None:
		ing_split = splitIngPhrase(pos_str)
		return [ing_split[0],ing_split[1],[],[]]

	if (',',',') not in pos_str or VBNnext < pos_str.index((',',',')):
		while VBNnext is not None:
			VBNlast = VBNnext
			VBNnext = next(VBNitr,None)
		
		if VBNlast == len(pos_str) - 1:
			ing_split = splitIngPhrase(pos_str)
			return [ing_split[0],ing_split[1],[],[]]
		prep_split = splitPrepPhraseList(pos_str[:VBNlast + 1],True)
		ing_split = splitIngPhrase(pos_str[VBNlast + 1:])
		return [ing_split[0],ing_split[1],prep_split[0],prep_split[1]]

	ing_split = splitIngPhrase(pos_str[:VBNnext])
	prep_split = splitPrepPhraseList(pos_str[VBNnext:],False)
	return [ing_split[0],ing_split[1],prep_split[0],prep_split[1]]

def splitIngPhrase(pos_str):
	parendesc = ''
	if pos_str[-1][0] == ',':
		del pos_str[-1]
	if pos_str[-1][1] == 'PARENPHRASE':
		parendesc = ' ' + pos_str[-1][0]
		del pos_str[-1]
	return [pos_str[-1][0]," ".join([x[0] for x in pos_str[:-1]]) + parendesc]


def splitPrepPhraseList(pos_str,prepended):
	commaitr = (i for i,v in enumerate(pos_str) if v == (',',','))
	commapos = next(commaitr,None)

	if commapos is not None:
		prepList = []
		prepDescList = []
		commas = [-1,commapos]
		while commas[1] is not None:
			[prep,desc] = splitPrepPhrase(pos_str[commas[0]+1:commas[1]],prepended)
			prepList.append(prep)
			prepDescList.append(desc)
			commas = [commas[1],next(commaitr,None)]

		[prep,desc] = splitPrepPhrase(pos_str[commas[0]+1:],prepended)
		prepList.append(prep)
		prepDescList.append(desc)
		return [prepList,prepDescList]

	[prep,desc] = splitPrepPhrase(pos_str,prepended)
	return [[prep],[desc]]

def splitPrepPhrase(pos_prep,prepended):
	parendesc = ''
	if pos_prep[0][0] == "and":
		pos_prep = pos_prep[1:]
	if prepended:
		if pos_prep[-1][1] == 'PARENPHRASE':
			parendesc = ' ' + pos_prep[-1][0]
			del pos_prep[-1]
		prep = pos_prep[-1][0]
		desc = " ".join([x[0] for x in pos_prep[:-1]]) + parendesc
	else:
		if pos_prep[0][1] == 'PARENPHRASE':
			parendesc = ' ' + pos_prep[0][0]
			del pos_prep[0]
		prep = pos_prep[0][0]
		desc = " ".join([x[0] for x in pos_prep[1:]]) + parendesc
	return [prep,desc]

def punctSanitize(pos_str):
	parenitr = (i for i,v in enumerate(pos_str) if v[0] == '(')
	parenpos = next(parenitr,None)
	while parenpos is not None:
		endparenpos = next((i for i,v in enumerate(pos_str) if v[0] == ')' and i > parenpos),None)
		if endparenpos is not None:
			after = []
			if len(pos_str) > endparenpos + 1:
				after = pos_str[endparenpos + 1:]
			pos_str = pos_str[:parenpos] + [(pos_str[parenpos][0] + ' '.join([x[0] for x in pos_str[parenpos + 1:endparenpos]]) + pos_str[endparenpos][0],'PARENPHRASE')]  + after
		else:
			del pos_str[parenpos]
		parenpos = next(parenitr,None)
	return [x for x in pos_str if x[1] != '.']
