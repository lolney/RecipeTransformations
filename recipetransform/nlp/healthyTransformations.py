import testParsedRecipe as test
from pprint import pprint
import recipetransform.tools.database as tools
import pymongo
import re
from bson.son import SON
import recipetransform.tools.database as tools
from recipetransform.tools.database import encode, decode
from recipetransform.tools.dictionary_ops import *
import transform_instructions as tI

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
    newIngs = []
    for ing in parsedIngs:
        newIng = dict()
        newIngforIns = dict()
        (replacement, energy, sodium) = getReplacement(ing["name"], cat, sort)

        #Split into name and descriptors
        (name, delim, desc) = replacement.partition(',')

        if(cat =="Energy" and energy != '0'):
            newIng["name"] = name + ' ('+str(energy)+' kcal)'
            newIng["descriptor"] = desc
            newIngforIns["name"] = name
            newIngforIns["descriptor"] = desc
        elif (sodium != '0'):
            newIng["name"] = name + ' ('+str(sodium)+' g)'
            newIng["descriptor"] = desc
            newIngforIns["name"] = name
            newIngforIns["descriptor"] = desc
        else:
            newIng["name"] = ing["name"]
            newIng["descriptor"] = ing["descriptor"]
            newIngforIns["name"] = ing["name"]
            newIngforIns["descriptor"] = ing["descriptor"]
        
        newIng["quantity"] = ing["quantity"]
        newIng["measurement"] = ing["measurement"]
        
        transRec.append(newIng)
        newIngs.append(newIngforIns)

    newIns = tI.updateAllInstructions(parsedIns, parsedIngs, newIngs);
    
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
