import json

import cache
import helper_functions as helperfunc

with open("item_values.json") as f:
    values = json.load(f)
schema = cache.getSchema()
item_values = {}
for name in values:
    for item in schema:
        if item["name"] == name:
            item_values[str(item["id"])] = values[name]
            break
if len(item_values) != len(values):
    raise LookupError ("Couldn't find all keys! Please review to make sure no keys are missing.")
del schema, values, item, name
print(item_values)

ships = {}

for day, dayCount in helperfunc.dateRange():
    print("Getting Ships, {} days left".format(dayCount))
    for ship in cache.getFromCache("ships", date=day):
        ships[ship["hex_code"]] = {
            "name": ship["name"],
            "items": ship["items"]
        }


print("calculating values for {} ships".format(len(ships)))
for hex in ships:
    items = ships[hex]["items"]
    value = 0
    for id in items:
        value += items[id] * item_values.get(id, 0)
    ships[hex]["value"] = value

print("Sorting...")
sorted =sorted(ships, key=lambda x: ships[x]["value"], reverse=True)

print("Outputting")
output = "Ship Stats:\n"
for hex in sorted[:500]:
    ship = ships[hex]
    output += "#{}: {} {} got {} points\n".format(sorted.index(hex)+1, hex, ship["name"], ship["value"])

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(output)