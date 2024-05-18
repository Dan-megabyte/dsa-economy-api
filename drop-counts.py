import datetime

import cache

date = datetime.date(2023, 7, 28) #cache.startDate
endDate = datetime.date.today()

items = cache.getSchema()

itemDict = {}
for item in items:
    itemDict[item["id"]] = item["name"]
del items, item

results = []

date -= datetime.timedelta(days=1)
while date < endDate:
    print((endDate-date).days)
    date += datetime.timedelta(days=1)

    summary = cache.getFromCache("summary", "prod", date)

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
