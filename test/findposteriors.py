from recipetransform.nlp.find_posterior_probabilities import findPosteriors

def downloadRecipe(x):

	import random, string
	data = ' '.join(random.choice(string.ascii_uppercase) for _ in range(100))
	category = random.choice(['a','b','c'])

	return (data, category)

def test_posteriors():

	results = findPosteriors(downloadRecipe)

	for word in results:
		for cat in results[word]:
			assert (results[word][cat] > 0) and (results[word][cat] < 1)