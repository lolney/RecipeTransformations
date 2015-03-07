import pymongo, nltk


def setDict(key, dict, value):

	if key in dict:
		return dict[key]
	else:
		dict[key] = {}
		return dict[key]


def addDict(key, dict, value):

	if key in dict:
		dict[key] = dict[key] + value
	else:
		dict[key] = value
	return dict


def findWordCountForRecipe(recipe, freqdist):

	for word in nltk.tokenize.word_tokenize(recipe):
		freqdist = addDict(word, freqdist, 1)

	return freqdist


def findWordCounts(freqdists):

	aggregate = {}
	for cat in freqdists:
		for word in freqdists[cat]:
			addDict(word, aggregate, freqdists[cat][word])

	return aggregate


def DBconnect():
	client = pymongo.MongoClient('mongodb://localhost:27017/')
	db = client.recipes

	return db

def findPosteriors(download_function=downloadRecipe):
	"""
	Count words for each recipe type : p(word | recipe)
	Get count for each recipe type : p(recipe)
	Merge counts : p(word)
	Find p(word | recipe) * p(recipe) / p(word) for each word
	Store this somewhere
	"""
	freqdists = {}
	for x in xrange(10000): # loop over recipes
		recipe, cat = download_function(x)
		freqdist = setDict(cat, freqdists, {})
		findWordCountForRecipe(recipe, freqdist)

	# total count of each word
	word_counts = findWordCounts(freqdists)

	posteriors = {}
	for word in word_counts:
		posteriors[word] = {}
		for cat in freqdists:
			if word not in freqdists[cat]:
				freqdists[cat][word] = 0
			# p(recipe | word)
			posteriors[word][cat] = float(freqdists[cat][word]) / float(word_counts[word])

	return posteriors

def main():

	posteriors = findPosteriors()
	db = DBconnect()
	db.posteriors.drop()
	db.posteriors.insert(posteriors)


if __name__ == "__main__":
	main()


