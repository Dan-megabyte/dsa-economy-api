import datetime
import matplotlib.pyplot as plt
import numpy as np

import cache
from helper_functions import dateRange

cache.updateDump("prod", ["summary"])

item_name = "Explosives"

schema = cache.getSchema("prod", False)

item_id = None

for item in schema:
    if item["name"]==item_name:
        item_id = item["id"]
        break

if item_id == None:
    raise ValueError

x = []
y = []

for day, _ in dateRange():
    for entry in cache.getFromCache("summary", "prod", day)["items_new"]:
        if entry["item"] == item_id:
            x.append(day)
            y.append(entry["grabbed"])
            break

#x = range(0, len(y))

plt.plot(x, y)
plt.show()