from BeautifulSoup import BeautifulSoup
import urllib2

def get_raw(url):

	resp = urllib2.urlopen(url)
	html = resp.read();
	parsed_html = BeautifulSoup(html)

	return parsed_html

def getIngredients(html):
	content = html.body.find(id='zoneIngredients')

	ingredient_lis = content.findAll(id='liIngredient')

	ingredients = [];
	for ingredient in ingredient_lis:
		ingredient_amount = ingredient.find('span', attrs={'class':'ingredient-amount'})
		ingredient_name = ingredient.find('span', attrs={'class':'ingredient-name'})
		ingredients.append({"q": ingredient_amount.text, "n": ingredient_name.text})

	return ingredients


def getInstructions(html):
	content = html.body.find('div', attrs={'class':'directions'})

	instruction_lis = content.findAll('li')

	instructions = []
	for instruction in instruction_lis:
		instruction_wrapper = instruction.find('span');
		instructions.append(instruction_wrapper.text)

	return instructions

def getName(html):
	return html.body.find(id="itemTitle").text


def parseHtml(url):

	parsed_html = get_raw(url)

	name = getName(parsed_html)
	ingredients = getIngredients(parsed_html)
	instructions = getInstructions(parsed_html)

	return {"name" : name, "ingredients" : ingredients, "instructions" : instructions}
