def replaceIngredient(ingredients, index, new_ingredient):

	return ingredients


def updateInstruction(parsed_instructions, old_ingredient, new_ingredient):

	return parsed_instructions


def getReplacementCandidate(encoded_ingredient, score, food_group):
	"""
	Look in food_group 
	Return the highest-scored x ingredient such that scoreOf(x) > score
	"""

def getFoodGroup(ingredient):

	return "Herbs and Spices"


def transform_recipe(parsed_ingredients, parsed_instructions):
	
	for i, ingredient in parsed_ingredients:

		food_group = getFoodGroup(ingredient)
		encoded_ingredient = encode(ingredient)
		score = lookup(encoded_ingredient, food_group)
		candidate = getReplacementCandidate(score, food_group)

		if candidate is not None:
			parsed_ingredients = replaceIngredient(parsed_ingredients, i, candidate)
			parsed_instructions = updateInstruction(parsed_instructions, ingredient, candidate)

	return parsed_ingredients, parsed_instructions

