import testParsedRecipe as test
from pprint import pprint
import recipetransform.tools.database as tools
import pymongo
import re
from bson.son import SON
import recipetransform.tools.database as tools
from recipetransform.tools.database import encode, decode
from recipetransform.tools.dictionary_ops import *

def transformHealthy(parsedIngs, parsedIns, transformType, transformCat):
    transformedIngs = []
    transIns= []
    if (transformCat== "calories"):
        if(transformType=="Low"):
            (transformedIngs, transIns) = transform(parsedIngs, "Energy", 1, parsedIns)
        elif (transformType=="High"):
            (transformedIngs, transIns) = transform(parsedIngs, "Energy", -1, parsedIns)
    elif (transformCat=="sodium"):
        if(transformType=="Low"):
            (transformedIngs, transIns) = transform(parsedIngs, "Sodium, Na", 1, parsedIns)
        elif (transformType=="High"):
            (transformedIngs, transIns) = transform(parsedIngs, "Sodium, Na", -1, parsedIns)
    return (transformedIngs, transIns)

def transform(parsedIngs, cat, sort, parsedIns):
    """
    Get replacement ingredients
    """
    # Search db for each ingredients in the
    transRec =[]
    newIns = parsedIns
    for ing in parsedIngs:
        newIng = {}
        (replacement, energy, sodium) = getReplacement(ing["name"], cat, sort)

        #Split into name and descriptors
        (name, delim, desc) = replacement.partition(',')

        if(cat =="Energy" and energy != '0'):
            newIng["name"] = name + ' ('+str(energy)+' kcal)'
        elif (sodium != '0'):
            newIng["name"] = name + ' ('+str(sodium)+' g)'
        else:
            newIng["name"] = ing["name"]
            
        newIng["descriptor"] = desc
        newIng["quantity"] = ing["quantity"]
        newIng["measurement"] = ing["measurement"]
        
        newIns = updateInstructionsHealthy(newIns, ing, newIng);
        transRec.append(newIng)

    return (transRec, newIns)

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
        return (results["result"][0]["name"], results["result"][0]["Energy"], results["result"][0]["Sodium, Na"])
    else:
        return (ingredient,'0','0')

def queryDB(pipeline):
    """
    Make aggregated query in MongoDB
    """
    db = tools.DBconnect()

    return db["nutrients"].aggregate(pipeline)

def updateInstructionsHealthy(instructions, oldIng, newIng):
    return instructions
