import json
import requests
import collections

###############
# URL
url = 'https://caan.zattoo.com'
###############

# Credentials
login = 'caan-api-user@zattoo.com'
password = '54321'
###############

# Listing
ID = '310001'
###############

session = requests.session()

def test_api(): # only to check the connection
    r = session.get(url + '/status/healthcheck', data={login: password}).json()
    print(r)

def get_some_listing():
    get_listing = session.get(url + '/api/v2.0/listings/' + ID, ).json()
    print(json.dumps(get_listing, indent=2, sort_keys=True))


#test_api()
#get_some_listing()

##### work with json file localy #####

def data():
    with open("hotwire.json", "r") as file:
        jsonFile = file.read()
        return jsonFile

def convert(data):
    return json.loads(data)

def getdict(obj):
    for key in obj:
        return key

listingDict = getdict(convert(data()))

def get_items(obj):
    keys = []
    if isinstance(obj, list):
        for i in obj:
            if i not in keys:
                keys.append(i)
    elif(isinstance(obj, dict)):
        for i in obj.keys():
            if i not in keys:
                keys.append(i)
    return keys
#print(listingDict)

class Caan:
    def __init__(self, dic):
        if (isinstance(dic, list)):
            self.dic = dic #should be list
        elif(isinstance(dic, dict)):
            self.dic = dic
        else:
            print("It is not a dictionary and not a list")

    def get_structure(self):
        structure = self.dic
        for i in get_items(structure):
            print(i)

    def get_listing_id(self):
        listing = self.dic
        return listing["listing_id"]
    
    def get_name(self):
        name = self.dic
        return name["name"]
        
test = Caan(listingDict)

n = len(listingDict)

def tata(listingDict, n):
    keys = []
    test = list(listingDict)
    keys.append(test[n])
    if n == 0:
        return keys
    else:
        tata(test, n-1)

print(tata(listingDict, n))