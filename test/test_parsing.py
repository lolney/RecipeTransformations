import recipetransform.nlp.parsing as parsing
from recipetransform.web.allrecipes import get_allrecipes_urls
import BeautifulSoup


def try_link(link):

	result = parsing.parseHtml(link)
	# Make sure format is as expected
	assert type(result['name']) == type(u"")
	assert type(result['ingredients']) == type([])
	assert type(result['instructions']) == type([])

	# Lists contain a reasonable number of elements
	assert len(result['ingredients']) > 1
	assert len(result['instructions']) > 0

	for elem in result['ingredients']:
		assert type(elem['q']) == type(u"")
		assert type(elem['n']) == type(u"")

	for elem in result['instructions']:
		assert type(elem) == type(u"")


def test_parsing():
	links = get_allrecipes_urls()
	for link in links[:5]:
		try_link(link)

if __name__ == "__main__":
	test_parsing()
