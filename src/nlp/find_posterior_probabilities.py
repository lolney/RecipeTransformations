import pymongo, nltk

# Download a bunch of classified recipes
def downloadRecipe(x):

	with open ("test.txt", "r") as myfile:
    	data=myfile.read()

	return (data, "category")


def setDict(key, dict, value):

	if key in dict:
		return dict[key]
	else:
		dict[key] = {}
		return dict[key]


def addDict(key, dict, value):

	if key in dict:
		dict[key] = dict[key] + value
	else;
		dict[key] = value
	return dict


def findPosteriors(recipe, freqdist):

	for word in nltk.tokenize.word_tokenize(recipe)
		addDict(word, freqdist, 1)

	return freqdist


def findWordCounts(freqdists):

	aggregate = {}
	for cat in freqdists:
		for word in freqdists[cat]:
			addDict(word, aggregate, freqdists[cat][word])

	return aggregate


def DBDump(posteriors, db):
	pass 

def DBconnect():
	client = MongoClient('mongodb://localhost:27017/')
	db = client.recipes

	return db

def main():

"""
Count words for each recipe type : p(word | recipe)
Get count for each recipe type : p(recipe)
Merge counts : p(word)
Find p(word | recipe) * p(recipe) / p(word) for each word
Store this somewhere
"""

	freqdists = {}
	for x in xrange(1): # loop over recipes
		recipe, cat = downloadRecipe(x)
		freqdist = setDict(cat, freqdists, {})
		findPosteriors(recipe, freqdist)

	# total count of each word
	word_counts = findWordCounts(freqdists)

	posteriors = {}
	for word in word_counts:
		posteriors[word] = {}
		for cat in recipe_counts:
			# p(recipe | word)
			posteriors[word][cat] = float(freqdists[cat][word]) / float(word_counts[word])

	db = DBconnect()
	DBDump(posteriors, db)


if __name__ == "__main__":
	main()


