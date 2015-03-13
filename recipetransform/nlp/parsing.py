from BeautifulSoup import BeautifulSoup
from recipetransform.nlp.parse_instruction import parse_instructions
from recipetransform.nlp.parse_ingredient import parse_ingredient
import urllib2

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
			parsed_ingred = {"quantity": ingredient_amount, "name": ingredient_name}
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
		instructions.append(instruction_text)

	#parsed_instructions = parse_instructions(instructions)
	# TODO: possibly separate prep instructions, cook instructions in the interface
	return instructions


def getName(html):
	return html.body.find(id="itemTitle").text


def parseHtml(url):
	
	parsed_html = parse_raw(url)

	name = getName(parsed_html)
	ingredients = getIngredients(parsed_html)
	instructions = getInstructions(parsed_html)

	return {"name" : name,
	 "ingredients" : ingredients,
	 "instructions" : instructions}
