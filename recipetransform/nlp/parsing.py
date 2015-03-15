from BeautifulSoup import BeautifulSoup
from recipetransform.nlp.parse_ingredient import parseIngredient, convert_ingredient
from recipetransform.nlp.parse_instruction import parse_instruction
from collections import OrderedDict
import urllib2


def parse_raw(url):

	resp = urllib2.urlopen(url)
	html = resp.read();
	parsed_html = BeautifulSoup(html)

	return parsed_html

def getIngredients(html):
	content = html.body.find(id='zoneIngredients')

	ingredient_lis = content.findAll(id='liIngredient')
	ingDict = OrderedDict()
	for ingredient in ingredient_lis:
		try:
			ingredient_amount = ingredient.find('span', attrs={'class':'ingredient-amount'}).text
			ingParse = parseIngredient(ingredient.find('span', attrs={'class':'ingredient-name'}).text)
			if ingParse[0] not in ingDict:
				ingDict[ingParse[0]] = []

			ingDict[ingParse[0]].append([ingredient_amount, ingParse[1],ingParse[2],ingParse[3]])
			
		except AttributeError: # expected, because some table elements contain no ingredients
			pass

	return ingDict
	
def getInstructions(html):
	content = html.body.find('div', attrs={'class':'directions'})

	instruction_lis = content.findAll('li')

	instructions = []
	for instruction in instruction_lis:
		instruction_text = instruction.find('span').text;
		instructions.append(instruction_text)

	return instructions


def getName(html):
	return html.body.find(id="itemTitle").text


def parseHtml(url):
	parsed_html = parse_raw(url)

	name = getName(parsed_html)
	ingDict = getIngredients(parsed_html)
	instructions = getInstructions(parsed_html)
	ingredients = []
	for x in ingDict.keys():
		for y in ingDict[x]:
			ingredients.append(convert_ingredient(x,y))

	return {"name" : name, "ingredients" : ingredients, "instructions" : instructions}


def parseHtmlforProgramInterface(url):

	parsed_html = parse_raw(url)
	ingDict = getIngredients(parsed_html)
	instructions = getInstructions(parsed_html)
	name = getName(parsed_html)

	ingredients = []
	for x in ingDict.keys():
		for y in ingDict[x]:
			ingredients.append(convert_ingredient(x,y))
	parsed_instructions = parse_instruction(instructions, name, ingDict)

	return {
		"ingredients" : ingredients,
		"primary cooking method" : parsed_instructions["cooking method"],
		"cooking methods" : parsed_instructions["secondary cooking methods"],
		"cooking tools" : parsed_instructions["cooking tools"]
	}


def main(url="http://allrecipes.com/Recipe/Easy-Garlic-Broiled-Chicken/"):

	print parseHtmlforProgramInterface(url)


if __name__ == "__main__":
	main()






