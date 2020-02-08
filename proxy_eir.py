import json
import requests

# Article about the eir proxy https://zattoo2.atlassian.net/wiki/spaces/BBEN/pages/1234567668/Eir+production+accounts+and+Network+Setup

base = "https://tvis.eir.ie/"

req = requests.session()

data = {
	"expires":"2020-02-25T18:13:18.000Z",
	"ipv4":"86.42.126.201", #EIR IP-Adresse
	"proxy":"109.41.1.217" #Meine IP-Adresse
}

r = req.put(base + 'addresses/proxies', data = json.dumps(data), headers = {'content-type':'application/json'})

print(r.content)