import cache
import datetime

import helper_functions as func

cache.updateDump()

itemSchema = cache.getSchema()

rares = {}

for rare in ["Fabricator (Legacy, Packaged)", "Golden Item Shredder"]:
    for item in itemSchema:
        if item["name"] == rare:
            id = item["id"]
            rares[id] = rare
            break

startDate = cache.startDate
endDate = datetime.date.today()


output = ""

rareCounts = []
for dayCount in range((endDate-startDate).days):
    rareCount = 0
    day = startDate+datetime.timedelta(dayCount)
    print("working, {} days left".format((endDate-startDate).days-dayCount))
    for entry in cache.getFromCache("log", date=day):
        if entry["item"] in rares:
            rareCount += 1
            src = entry["src"]
            if src[-5:] == " hurt":
                violent = "violently "
                src = src[:-5]
            else:
                violent = ""
            src = src[1:-1]
            dst = entry["dst"][1:-1]
            srcShip = func.getShipInfo(src, day)
            dstShip = func.getShipInfo(dst, day)
            date = str(day.day)+"/"+str(day.month)+"/"+str(day.year)
            output += ("OMG! {} {} {}sent {} {} to {} {} on {}\n".format(src, srcShip["name"], violent, entry["count"], rares[entry["item"]], dst, dstShip["name"], date))
    rareCounts.append(rareCount)

rareCount = 0
for num in rareCounts:
    rareCount += num
output += "\n Average amount of rares traded per day: {}".format(rareCount/(endDate-startDate).days)

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(output)
print("done!")