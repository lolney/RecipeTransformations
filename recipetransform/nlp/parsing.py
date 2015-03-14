from BeautifulSoup import BeautifulSoup
from recipetransform.nlp.parse_instruction import parse_instruction
from recipetransform.nlp.parse_ingredient import parse_ingredient, parseIngredient, convert_ingredient
import urllib2


def parse_raw(url):

	resp = urllib2.urlopen(url)
	html = resp.read();
	parsed_html = BeautifulSoup(html)

	return parsed_html

def getIngredients(html):
	content = html.body.find(id='zoneIngredients')

	ingredient_lis = content.findAll(id='liIngredient')
	ingDict = dict()
	for ingredient in ingredient_lis:
		try:
			ingredient_amount = ingredient.find('span', attrs={'class':'ingredient-amount'}).text
			ingParse = parseIngredient(ingredient.find('span', attrs={'class':'ingredient-name'}).text)
			if ingParse[0] not in ingDict:
				ingDict[ingParse[0]] = []

			ingDict[ingParse[0]].append([ingredient_amount, ingParse[1],ingParse[2],ingParse[3]])
			#parsed_ingred = parse_ingredient(ingredient_amount, ingredient_name)
			
		except AttributeError: # expected, because some table elements contain no ingredients
			pass

	return ingDict
	
def getInstructions(html,ingDict):
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
	ingDict = getIngredients(parsed_html)
	instructions = getInstructions(parsed_html,ingDict)
	ingredients = []
	for x in ingDict.keys():
		for y in ingDict[x]:
			ingredients.append(convert_ingredient(x,y))

	return {"name" : name, "ingredients" : ingredients, "instructions" : instructions}
