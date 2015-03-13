from urllib2 import urlopen
import urllib, urllib2, os, json
#from recipetransform.tools.usda import makeUSDARequst
from recipetransform.tools.dictionary_ops import *

api_key = 'sFchHANvtaKnCEJyRKVYIlOpsa8MDFrTDunVXwdx'


def makeUSDARequstNutrient(endpoint, query, fg2, auth_key=None):
    if auth_key is None:
        auth_key = os.environ.get('USDAKey')

    query['api_key'] = auth_key
    query['format'] = 'json'
    fgstring = ''
    nutstring = ''
    fgstring2=''
    
    for fg in query['fg']:
      fgstring += 'fg='+fg+ '&'

    for fg in fg2:
      fgstring2 += 'fg='+fg+ '&'
      
    for nut in query['nutrients']:
        nutstring += 'nutrients=' +nut+ '&'

    qstring = fgstring+nutstring+'api_key='+ query['api_key'] + '&max='+query['max'] + '&offset='+query['offset']
    qstring2 = fgstring2+nutstring +'api_key='+ query['api_key'] + '&max='+query['max']+ '&offset='+query['offset']

    url = 'http://api.nal.usda.gov/usda/ndb/' +endpoint + qstring
    result_string = urllib.urlopen(url).read()
    
    url2 = 'http://api.nal.usda.gov/usda/ndb/' +endpoint + qstring2
    result_string2 = urllib.urlopen(url2).read();
    
    results = json.loads(result_string)['report']['foods']
    results2 = json.loads(result_string2)['report']['foods']
    #print len(resultSodCal)
    #print len(resultSodCal2)
    #print
    results = results+ results2;
    #print len(resultSodCal)
        
    return results

def getFoodList(offset=0):
    endpoint = "nutrients/?"
    query ={
        'fg': ['0100','0200','0400','0500', '0600', '0700','0900','1000','1100', '1200'],
        'nutrients': ['208', '307', '205', '269','203','291'],
        'max': '1500',
        'offset': str(offset)
    }
    fg2= ['1300', '1400','1500','1600','1700','1800','1900','2000']

    result = makeUSDARequstNutrient(endpoint, query, fg2, api_key)
    
    if(len(result) == 3000):
        offset+=1500
        return result + getFoodList(offset)
    else:
    	return result

def buildDB():
    #results = makeUSDARequstNutrient('nutrients/?', query, api_key)
    results = getFoodList()
    nutrients = []
    
    for item in results:
        d = {}
        d['name'] = item['name']
        for nut in item['nutrients']:
            d[nut['nutrient']] = nut['value']
        
        nutrients.append(d)

    print len(nutrients)

    return nutrients

def main():
    nutList = buildDB()
    with open("nutrients.json", "w+") as file:
            json.dump(nutList, file)

if __name__ == "__main__":
    main()
'''
calories = [{
    'name': 'cheddar cheese',
    'calories': 400
}, {
    'name': 'cottage cheese'
    'calories': 100
]

sodium = [{
    'name': 'cheddar cheese',
    'sodium': 400
}, {
    'name': 'cottage cheese'
    'sodium': 100
]



'''
