from testParsedRecipe import parsedRecipe2
from testParsedRecipe import parsedRecipe
from HealthyTransformationKB import lowCalSubs
from HealthyTransformationKB import highCalBad

for x in parsedRecipe2["ingredients"]:
	for item in highCalBad:
		if item in x["name"]:
			x["name"] = lowCalSubs[item][1]
			print item
