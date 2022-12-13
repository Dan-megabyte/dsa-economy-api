import json
import requests
import datetime

prefix = "https://pub.drednot.io/"
mid = "/econ/"
instance = "prod"
itemschemaurl = prefix+instance+mid+"item_schema.json"
date = datetime.date(2022, 11, 23)
enddate = datetime.date.today()# - datetime.timedelta(days=1)

items = json.loads(requests.get(itemschemaurl).text)

itemDict = {}
for item in items:
    itemDict[item["id"]] = item["name"]

results = []

date -= datetime.timedelta(days=1)
while date < enddate:
    date += datetime.timedelta(days=1)
    datestr = str(date.year)+"_"+str(date.month)+"_"+str(date.day)+"/"
    summaryurl = prefix+instance+mid+datestr+"summary.json"


    summary = json.loads(requests.get(summaryurl).text)

    result = {}
    for item in summary["items_new"]:
        itemtotal = item["total"]
        nameofsource = item["src"]
        nameofitem = itemDict[item["item"]]
        if not nameofsource in result.keys():
            result[nameofsource] = {}
        result[nameofsource][nameofitem] = itemtotal
    results.append(result)

finalresult = {}
for source in result:
    finalresult[source] = {}
    for item in result[source]:
        total = 0
        for i in results:
            total += i.get(source, {}).get(item, 0)
        finalresult[source][item] = total / len(results)
    total = 0
    for item in finalresult[source]:
        total += finalresult[source][item]
    for item in finalresult[source]:
        finalresult[source][item] = finalresult[source][item] / total

text = ""
for source in finalresult:
    text += source+"\n"
    for item in finalresult[source]:
        text += "    "
        text += item
        text += ": "
        text += str(finalresult[source][item]*100)
        text += "\n"
with open("output.txt", "w+") as f:
    f.write(text)