from testParsedRecipe import parsedRecipe2
from testParsedRecipe import parsedRecipe
from HealthyTransformationKB import lowCalSubs
from HealthyTransformationKB import highCalBad
from HealthyTransformationKB import lowCalGood
from InternalRepresentationRecipe import internal
from autoOrgtoInternalOrgo import internal2
from autoOrgtoInternalOrgo import internal3
from HealthyTransformationKB import lowSodiumSub
from HealthyTransformationKB import highSodium

def toHealthyCal(recipe):
        """
        Takes in a recipe and replaces high calorie ingredients with
        low calorie ones.
        """
        for ing in recipe:
                for item in recipe[ing]:
                        desc = item[2]
                        for thing in highCalBad:
                                if ing == thing:
                                       replaceHighCal(ing, recipe, desc)
        return

def replaceHighCal(ing, recipe, desc):
        """
        Takes an ingredient, the recipe it is in, and its description and
        replaces the ingredient in the recipe list.
        """
        print "ingredient name " + ing
        for item in recipe[ing]:
                print item[2]
                print desc
                if item[2] == desc:
                        item[2] += ", " + lowCalSubs[ing][0]["descriptor"]
        return recipe

def toHealthySodium(recipe):
        """
        Takes in a recipe and replaces all high sodium ingredients with low
        sodium versions.
        """
        for ing in recipe:
                for item in recipe[ing]:
                        desc = item[2]
                        for thing in highSodium:
                                if ing == thing:
                                       replaceHighSod(ing, recipe, desc)

def replaceHighSod(ing, recipe, desc):
        """
        Takes an ingredient, the recipe it is in, and its description and
        replaces the ingredient with a low sodium substitution.
        """
        for item in recipe[ing]:
                print item[2]
                print desc
                if item[2] == desc:
                        item[2] += ", " + lowSodiumSub[ing][0]["descriptor"]
        return recipe

