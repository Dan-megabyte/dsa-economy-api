import cache
import datetime

import helper_functions as func

cache.updateDump()
itemSchema = cache.getSchema()

itemDict = {}
for item in itemSchema:
    itemDict[item["id"]] = item["name"]


startDate = cache.startDate
endDate = cache.startDate + datetime.timedelta(days=1)



ship_names = {"void":"the void"}
fights = {}

for dayCount in range((endDate-startDate).days):
    day = startDate+datetime.timedelta(dayCount)
    try:
        print("working, {} days left".format((endDate-startDate).days-dayCount))
        for entry in cache.getFromCache("log", date=day):
            if entry["src"][-5:] == " hurt":
                #print(entry)
                hurt = entry["src"][1:-6]
                if not hurt in fights:
                    fights[hurt] = {}
                    if not hurt in ship_names:
                        ship_names[hurt] = func.getShipInfo(hurt, day)["name"]
                if entry["dst"] == "killed":
                    dst = "void"
                else:
                    dst = entry["dst"][1:-1]
                    if not dst in ship_names:
                        ship_names[dst] = func.getShipInfo(dst, day)["name"]
                if not dst in fights[hurt]:
                    fights[hurt][dst] = {}
                if entry["item"] in itemDict:
                    itemId = entry["item"]
                    itemCount = entry["count"]
                else:
                    print(itemDict)
                    raise ValueError ("Item Id {} does not exist in item schema".format(entry["item"]))
                if not itemId in fights[hurt][dst]:
                    fights[hurt][dst][itemId] = 0
                fights[hurt][dst][itemId] += itemCount
                
    except Exception as err:
        print("An error occured:")
        print(err)
        print("On day:")
        print(day)
        print("Continuing...")

print("cleaning up")
invalid = []
for victim in fights:
    if list(fights[victim].keys()) == ["void"]:
        invalid.append(victim)
for victim in invalid:
    del fights[victim]
del invalid

output = ""

for victim in fights:
    if not victim in ship_names:
        print("Haven't found victim's name: {}".format(victim))
    victim_name = ship_names.get(victim, victim)
    output += "{} Lost:\n".format(victim_name)
    for victor in fights[victim]:
        if not victor in ship_names:
            print("Haven't found victor's name: {}".format(victor))
        victor_name = ship_names.get(victor, victor)
        output += "   To {}\n".format(victor_name)
        for item in fights[victim][victor]:
            item_name = itemDict[item]
            count = fights[victim][victor][item]
            output += "      {}: {}\n".format(item_name, count)

#output += "\n Average amount of rares traded per day: {}"

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(output)
print("done!")
