import gzip
import requests
import datetime
import json
import os

prefix = "https://pub.drednot.io/"
mid = "/econ/"

dumpTypeExtensions = {
    "summary":".json",
    ""
}

def mkdir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

mkdir("files")

mkdir("files/prod")
mkdir("files/test")

mkdir("files/prod/summary")
mkdir("files/prod/log")
mkdir("files/prod/ships")

mkdir("files/test/summary")
mkdir("files/test/log")
mkdir("files/test/ships")

def saveLinkToFile(link, filepath):
    text = requests.get(link).text
    with open(filepath, "w") as f:
        f.write(text)

def updateDump(
    instance:str="prod",
    dumpTypes:list=["summary", "log", "ships"], 
    startdate:datetime.date=datetime.date(2022, 11, 23), 
    enddate:datetime.date=datetime.date.today()):
    saveLinkToFile(
        prefix + instance + mid + "item_schema.json",
        os.path.join("files", instance, "item_schema.json"))
    for dumpType in dumpTypes:
        date = startdate
        date -= datetime.timedelta(days=1)
        while date < enddate:
            print("Getting data: {} days left".format(enddate-date).days)
            date += datetime.timedelta(days=1)
            datestr = str(date.year)+"_"+str(date.month)+"_"+str(date.day)
            filepath = os.path.join("files",instance,dumpType,datestr+".json")
            if not os.path.exists(filepath):
                saveLinkToFile(
                    prefix+instance+mid+datestr+"/"+dumpType+dumpTypeExtensions[dumpType]
                )