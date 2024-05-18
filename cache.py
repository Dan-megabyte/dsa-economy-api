import os
import gzip
import requests
import datetime
import json
import time
import threading

prefix = "https://pub.drednot.io/"
mid = "/econ/"
startDate = datetime.date(2022, 11, 23)
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
    dumpTypes:set={"summary", "log", "ships"}, 
    startdate:datetime.date=startDate, 
    enddate:datetime.date=datetime.date.today()) -> None:
    saveLinkToFile(
        prefix + instance + mid + "item_schema.json",
        os.path.join(cachedir, instance, "item_schema.json"))
    threads = []
    for dumpType in dumpTypes:
        date = startdate
        date -= datetime.timedelta(days=1)
        print("Verifying data {} for {}".format(dumpType, instance))
        while date < enddate:
            date += datetime.timedelta(days=1)
            datestr = str(date.year)+"_"+str(date.month)+"_"+str(date.day)
            filepath = os.path.join(cachedir,instance,dumpType,datestr+".json")
            if not os.path.exists(filepath):
                print("Getting data {} for {} : {} days left".format(dumpType, instance, (enddate-date).days))
                while threading.activeCount() > 10:
                    time.sleep(0.5)
                threads.append(threading.Thread(target=saveLinkToFile,args=(
                    prefix+instance+mid+datestr+"/"+dumpType+dumpTypeExtensions[dumpType],
                    filepath)))
                threads[-1].start()
    for thread in threads:
        thread.join()
                    
def getFromCache(dumpType:str, instance:str="prod", date:datetime.date=datetime.date.today()):
    datestr = str(date.year)+"_"+str(date.month)+"_"+str(date.day)
    filepath = os.path.join(cachedir, instance, dumpType, datestr+".json")
    if not os.path.exists(filepath):
        updateDump(instance, {dumpType}, date, date)
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)

def getSchema(instance:str="prod", overwrite:bool=True) -> list:
    filepath = os.path.join(cachedir, instance, "item_schema.json")
    if not os.path.exists(filepath):
        saveLinkToFile(
            prefix + instance + mid + "item_schema.json",
            filepath)
    lastmodified = datetime.datetime.fromtimestamp(os.path.getmtime("cache.py"))
    if lastmodified < datetime.datetime.now() - datetime.timedelta(days=1):
        saveLinkToFile(
            prefix + instance + mid + "item_schema.json",
            filepath)
    with open(filepath, encoding="utf-8") as f:
        schema = json.load(f)
    if overwrite:
        with open("depreciated_items.json", encoding="utf-8") as f:
            overrides = json.load(f)
        for override in overrides:
            schema.append(override)
    return schema

if __name__ == "__main__":
    updateDump()
    updateDump("test")
    print(getSchema())
