import json

def fixNutrients(file):
    nutList = ["Fiber, total dietary", "Sodium, Na", "Protein", "Carbohydrate, by difference", "Sugars, total", "Energy"]
    with open(file) as fl:
        items = json.load(fl)

        for ing in items:
            for nut in nutList:
                if(ing[nut] != "--"):
                    newVal = float(ing[nut])
                else:
                    newVal = "--"
                ing[nut]=newVal

    with open("nutrients3.json", "w+") as file:
                json.dump(items, file)

		
