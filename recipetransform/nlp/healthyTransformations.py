import testParsedRecipe as test
from pprint import pprint

import recipetransform.tools.database as tools
import pymongo
import re
from bson.son import SON
import recipetransform.tools.database as tools
from recipetransform.tools.database import encode, decode
from recipetransform.tools.dictionary_ops import *

def transformHealthy(parsedIngs, transformCat, transformType):
    if (transformCat== "calories"):
        if(transformType=="low"):
            transform(parsedIngs, "Energy", 1)
        else:
            transform(parsedIngs, "Energy", -1)
    else:
        if(transformType=="low"):
            transform(parsedIngs, "Sodium,Na", 1)
        else:
            transform(parsedIngs, "Sodium,Na", -1)

def transform(parsedIngs, cat, sort):
    """
    Get replacement ingredients
    """
    # Search db for each ingredients in the
    for ing in parsedIngs:
        print "Ingredient " + ing["name"]
        replacement = getReplacement(ing["name"], cat, sort)
        print "Replacement is " +replacement
        print

def getReplacement(ingredient, cat, sort):
    """
    Query nutrient database
    """
    #queryName = "/^"+ingredient+".*/i"
    #also should consider descriptors
    pipe = [
        {"$match": {"name": re.compile("^" +ingredient+"+", re.IGNORECASE)}},
        {"$sort": SON({cat: sort})}
    ]

    pipeline = list(pipe)
    results = queryDB(pipe)
    #return lowest calory ingredient that matches
    #print results["result"]    
    
    if (results["result"] !=[]):
        print len(results["result"])
        print results["result"][0]["Energy"]
        return results["result"][0]["name"]
    else:
        return ingredient

def queryDB(pipeline):
    db = tools.DBconnect()

    return db["nutrients"].aggregate(pipeline)
