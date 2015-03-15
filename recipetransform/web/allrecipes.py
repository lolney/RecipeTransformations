import BeautifulSoup, random, re
import recipetransform.nlp.parsing as parsing


def get_allrecipes_urls():
	url = "http://allrecipes.com/recipes/main.aspx?Page=" + str(random.randint(1,10))
	html = parsing.parse_raw(url);

	link_containers = html.body.findAll(id='divGridItemWrapper')

	links = []
	for l in link_containers:
		link = l.find('a')
		href = "http://allrecipes.com" + link['href']
		links.append(href)

	return links


def random_recipe():
	links = get_allrecipes_urls()
	link = random.choice(links)
	return re.search('^.*(?=Detail.aspx)', link).group(0)
