""" Break down ingredients as specified in API below 

Quantity and descriptor should be easy - these are contained in the quantity_string. 
The rest will be a bit harder, but we can probably use pos and syntactic parsing:

words that indicate preparation:
minced lemon zest		<- participle
pork tenderloin, cut into 1 1/2 inch pieces 	<- participle phrase
"""

def parse_ingredient(quantity_string, rest):
	return {
		"name":	"salt",
		"quantity":	1,
		"measurement":	"pinch",
		"descriptor":	"table",
		"preparation":	"none"
	}