from recipetransform.nlp.find_posterior_probabilities import findPosteriors

cats = ['a','b','c']

def downloadRecipe(x):

	import random, string
	data = ' '.join(random.choice(string.ascii_uppercase) for _ in range(500))
	category = random.choice(cats)

	return (data, category)

def test_posteriors():

	results = findPosteriors(downloadRecipe)

	# Make sure posterior probabilities are reasonable
	for word in results:
		for cat in results[word]:
			assert (results[word][cat] > 0) and (results[word][cat] < 1)

	# Make sure all letters, categories are present
	for letter in string.ascii_uppercase:
		assert letter in results.keys()
		for cat in cats:
			assert cat in results[letter].keys()
