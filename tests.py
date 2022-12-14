import json
import gzip
import requests

prefix = "https://pub.drednot.io/"
mid = "/econ/"
instance = "prod"
itemschemaurl = prefix+instance+mid+"item_schema.json"

items = json.loads(requests.get(itemschemaurl).text)

itemDict = {}
for item in items:
    itemDict[item["id"]] = item["name"]

itemDict[3] = "silica"
itemDict[225] = "manual turret"

results = []

datestr = str(2022)+"_"+str(11)+"_"+str(24)+"/"
summaryurl = prefix+instance+mid+datestr+"summary.json"
logurl = prefix+instance+mid+datestr+"log.json.gz"
shipurl = prefix+instance+mid+datestr+"ships.json.gz"

print("unzipping")
with gzip.open(requests.get(logurl, stream=True).raw, "rt") as f:
    print("unpacking json")
    logjson = json.load(f)

with gzip.open(requests.get(shipurl, stream=True).raw, "rt") as f:
    print("unpacking json")
    shipjson = json.load(f)


tot = len(logjson)
result = ""
for i in range(0, tot):
    print(i, tot)
    item = logjson[i]
    if item["zone"][:8] != "Freeport":
        result += itemDict[item["item"]]
        result += ": "+ str(item["count"])+" "
        result +=item["src"]+"-->"
        result +=item["dst"]+"\n"

print("writing")
with open("output.txt", "w") as f:
    f.write(result)
