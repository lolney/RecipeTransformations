from recipetransform.nlp.find_posterior_probabilities import findPosteriors
import random, string

cats = range(5)

def genRandomString(alphabet):
	return ''.join([random.choice(alphabet) for _ in range(1)])


def downloadRecipe(x):
	
	data = [{"name" : genRandomString(string.ascii_uppercase), "descriptor": genRandomString(string.ascii_lowercase)} for x in xrange(200)]

	return data


def genIds():
	return {x : random.sample(cats, 2) for x in xrange(1000)}


def test_posteriors():

	ids = genIds()
	results = findPosteriors(ids, downloadRecipe)

	# Make sure posterior probabilities are reasonable
	for word in results:
		for cat in results[word]:
			assert (results[word][cat] > 0) and (results[word][cat] < 1)

	# Make sure all letters, categories are present
	for letter in string.ascii_uppercase:
		ingredient = (letter + '&')
		assert ingredient in results.keys()
		for cat in cats:
			assert cat in results[ingredient].keys()

	return results


def main():
	print test_posteriors()


if __name__ == "__main__":
	main()
