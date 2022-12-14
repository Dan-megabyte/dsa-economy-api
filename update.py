import gzip
import requests
import datetime
import json
import os

startdate = datetime.date(2022, 11, 23)
enddate = datetime.date.today()
date = startdate

if not os.path.exists("files/"):
    os.mkdir("files")

requests.get("").text
if os.path.exists("files/item_schema.json"):