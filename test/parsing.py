import recipetransform.nlp.parsing as parsing
import BeautifulSoup

def get_allrecipes_urls():
	url = "http://allrecipes.com/recipes/main.aspx?Page=1#recipes"
	html = parsing.parse_raw(url);

	link_containers = html.body.findAll(id='divGridItemWrapper')

	links = []
	for l in link_containers:
		link = l.find('a')
		href = "http://allrecipes.com" + link['href']
		links.append(href)

	return links

def try_link(link):

	result = parsing.parseHtml(link)

	assert type(result['name']) == type(u"")
	assert type(result['ingredients']) == type([])
	assert type(result['instructions']) == type([])

	for elem in result['ingredients']:
		assert type(elem['q']) == type(u"")
		assert type(elem['n']) == type(u"")

	for elem in result['instructions']:
		assert type(elem) == type(u"")


def test_parsing():
	links = get_allrecipes_urls()
	for link in links:
		try_link(link)
