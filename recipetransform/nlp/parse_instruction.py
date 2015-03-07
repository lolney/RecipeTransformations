"""
Find cooking methods (e.g. saute, broil, boil, poach, etc.) - primary and secondary - and tools
(Parts of speech and syntactic parsing will be important here)

"Remove the pork to a serving platter"
"into a plastic bag"
(prepositional phrases)

Probably also want to pass the ingredient list, to filter those words out,
and the name, which will be important in deciding the primary cooking method
"""

def parse_instructions(instruction_list):
	return {
		"cooking method" : "primary",
		"secondary cooking methods" : ["",""],
		"cooking tools" : ["",""],
		"prep steps" : ["",""],
		"cook steps" : ["",""]
	}