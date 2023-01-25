import gzip
import requests
import datetime
import json
import os

prefix = "https://pub.drednot.io/"
mid = "/econ/"
cachedir = "cache"

dumpTypeExtensions = {
    "summary":".json",
    "log":".json.gz",
    "ships":".json.gz",
}

def mkdir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

mkdir(cachedir)

mkdir(cachedir + "/prod")
mkdir(cachedir + "/test")

mkdir(cachedir + "/prod/summary")
mkdir(cachedir + "/prod/log")
mkdir(cachedir + "/prod/ships")

mkdir(cachedir + "/test/summary")
mkdir(cachedir + "/test/log")
mkdir(cachedir + "/test/ships")

def saveLinkToFile(link, filepath):
    text = requests.get(link).text
    if link[-3:] == ".gz":
        text = gzip.decompress(requests.get(link).content)
    elif link[-5:] == ".json":
        text = requests.get(link).text
    text = json.loads(text)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(text, f, separators=(',', ':'), indent=None)
def updateDump(
    instance:str="prod",
    dumpTypes:list=["summary", "log", "ships"], 
    startdate:datetime.date=datetime.date(2022, 11, 23), 
    enddate:datetime.date=datetime.date.today()) -> None:
    saveLinkToFile(
        prefix + instance + mid + "item_schema.json",
        os.path.join(cachedir, instance, "item_schema.json"))
    for dumpType in dumpTypes:
        date = startdate
        date -= datetime.timedelta(days=1)
        while date < enddate:
            print("Getting data {} for {} : {} days left".format(dumpType, instance, (enddate-date).days))
            date += datetime.timedelta(days=1)
            datestr = str(date.year)+"_"+str(date.month)+"_"+str(date.day)
            filepath = os.path.join(cachedir,instance,dumpType,datestr+".json")
            if not os.path.exists(filepath):
                saveLinkToFile(
                    prefix+instance+mid+datestr+"/"+dumpType+dumpTypeExtensions[dumpType],
                    filepath)
"""
def getFromCache(dumpType:str, instance:str="prod", date:datetime.date=datetime.datetime.now().date):
    datestr = str(date.year)+"_"+str(date.month)+"_"+str(date.day)
    filepath = os.path.join(cachedir, instance, dumpType, datestr+".json")
    if not os.path.exists(filepath):
        updateDump(instance, [dumpType], date, date)
"""

if __name__ == "__main__":
    updateDump()
    updateDump("test")