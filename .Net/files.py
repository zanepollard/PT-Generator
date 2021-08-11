import datetime
import os
import shutil
#import yaml
import re
import csv

tdy = datetime.datetime.today()

def fileFind(folder, pullMode):
    dateRun = datetime.datetime.today()
    files = []

    if(pullMode == "ALL"):
        year = str(dateRun.year)[2:4]
        month = str(dateRun.month)
        day = str(dateRun.day)
        for file in os.listdir(folder):
            if re.match(rf'TransactionTable[\d]{{6}}[.csv]', file):
                files.append(file)
    if(pullMode == "DAILY"):
        prevDate = dateRun - datetime.timedelta(days=1)
        year = str(prevDate.year)[2:4]
        month = str(prevDate.month)
        day = str(prevDate.day)
        for file in os.listdir(folder):
            if re.match(rf'TransactionTable{year}0?{month}0?{day}[.csv]', file):
                files.append(file)

    return files

def salesOutput(set, config_data, root):
    output = os.path.abspath(config_data.get('output_folder'))
    filename = ""

    dateRun = datetime.datetime.today()
    day = str(dateRun.day)
    month = str(dateRun.month)
    year = str(dateRun.year)[2:4]

    if(len(day)<2):
        day = "0" + day
    if(len(month)<2):
        month = "0" + month


    os.chdir(root)
    os.chdir(output)

    if bool(config_data['VDPOutput']):
        filename = f"pt{month}{day}{year}.txt"
        f = open(filename, "a")
        for key in set:
            f.write(set[key].VDPPrint())
        
    elif bool(config_data['AGTRAX']):
        filename = "AGTRAX.DDF"
        f = open(filename, "a")
        for key in set:
            f.write(set[key].AGTRAXPrint())