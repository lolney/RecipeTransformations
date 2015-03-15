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
            transformedIngs = transform(parsedIngs, "Energy", 1)
        else:
            transformedIngs = transform(parsedIngs, "Energy", -1)
    else:
        if(transformType=="low"):
            transformedIngs = transform(parsedIngs, "Sodium,Na", 1)
        else:
            transformedIngs = transform(parsedIngs, "Sodium,Na", -1)
    return transformedIngs

def transform(parsedIngs, cat, sort):
    """
    Get replacement ingredients
    """
    # Search db for each ingredients in the
    transRec = []
    for ing in parsedIngs:
        newIng = {}
        replacement = getReplacement(ing["name"], cat, sort)

        #Split into name and descriptors
        (name, delim, desc) = replacement.partition(',')

        newIng["name"] = name
        newIng["descriptor"] = desc

        transRec.append(newIng)
    return transRec

def getReplacement(ingredient, cat, sort):
    """
    Query nutrient database
    """
    pipe = [
        {"$match": {"name": re.compile("^" +ingredient+"[a-z]?[^ ],?( [-\w]+[^(ed)](,)?)?( [-\w]+[^(ed)](,)?)?( [-\w]+[^(ed)](,)?)?$", re.IGNORECASE)}},
        {"$sort": SON({cat: sort})}
    ]

    pipeline = list(pipe)
    results = queryDB(pipe)
    
    if (results["result"] !=[]):
        return results["result"][0]["name"]
    else:
        return ingredient

def queryDB(pipeline):
    """
    Make aggregated query in MongoDB
    """
    db = tools.DBconnect()

    return db["nutrients"].aggregate(pipeline)
