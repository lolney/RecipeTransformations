""" Break down ingredients as specified in inferface below 

Quantity and descriptor should be easy - these are contained in the quantity_string. 
The rest will be a bit harder, but we can probably use pos and syntactic parsing:

words that indicate preparation:
minced lemon zest		<- participle
pork tenderloin, cut into 1 1/2 inch pieces 	<- participle phrase
"""

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
}

def parseQuantity(string):
	tokens = nltk.word_tokenize(string)
	return [tokens[0]," ".join(tokens[1:])]

def parseIngredient(string):
	pos_str = nltk.pos_tag(nltk.word_tokenize(u"Add in the " + unicode(string)))[3:]
	VBNitr = (i for i, v in enumerate(pos_str) if v[1] == 'VBN')
	VBNnext = next(VBNitr,None)
	
	if VBNnext is None:
		ing_split = splitIngPhrase(pos_str)
		return [ing_split[0],ing_split[1],[],[]]

	if (',',',') not in pos_str or VBNnext < pos_str.index((',',',')):
		while VBNnext is not None:
			VBNlast = VBNnext
			VBNnext = next(VBNitr,None)

		prep_split = splitPrepPhraseList(pos_str[:VBNlast + 1],True)
		ing_split = splitIngPhrase(pos_str[VBNlast + 1:])
		return [ing_split[0],ing_split[1],prep_split[0],prep_split[1]]

	ing_split = splitIngPhrase(pos_str[:VBNnext])
	prep_split = splitPrepPhraseList(pos_str[VBNnext:],False)
	if ing_split is None:
		print "ing"
	if prep_split is None:
		print "prep"
	return [ing_split[0],ing_split[1],prep_split[0],prep_split[1]]

def splitIngPhrase(pos_str):
	return [pos_str[-1][0]," ".join([x[0] for x in pos_str[:-1]])]

def splitPrepPhraseList(pos_str,prepended):
	if pos_str is None:
		print "pos_str is None!"
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
	if pos_prep[0][0] == "and":
		pos_prep = pos_prep[1:]
	if prepended:
		prep = pos_prep[-1][0]
		desc = " ".join([x[0] for x in pos_prep[:-1]])
	else:
		prep = pos_prep[0][0]
		desc = " ".join([x[0] for x in pos_prep[1:]])
	return [prep,desc]
