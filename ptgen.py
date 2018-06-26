import csv
import re
import fnmatch
import os

siteid = "" #6 chars from header file ***DONE***
seqnum = "" #4 chars from variable file; named "SEQUENCE#"
STATCODE = "00" #"00"
totAmt = "" #6 chars from header file; formatted like 0000.00 minus the decimal eg 002730 = 0027.30
ACT = "00"
TRANTYPE ="00"
pCode = "" #2 char product code ***DONE***
price = "10000000" #8 char price 0.0000000 ***DONE***
quantity = "" #8 chars from d log, index 10 ***DONE***
odometer = "" #7 chars in variables file
OID = "0" #odometer implied decimal
pump = "" #2 char from variables file
tranNum = "" #4 char from variable file ***DONE***
tranDate = "" #6 chars YYMMDD
tranTime = "" #4 char HHNN (military time)
fill = "00000000"
id_vehicle = "" #8 char from variable file name is id_vehicle
id_card = "" #7 char from variable file
part_id ="000"
id_acct = "" #6 chars from variable file of the same name
vehicle = "" #4 chars, same as id_vehicle but without leading zeros
end = "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000DCF000000000000000000000000"

#Formats date in the proper PT file format
def dFormat(date):
    fDate = date[8:10] + date[0:2] + date[3:5]
    return fDate

def decimalSplit(number, x):
    if x:
        temp = number.split('.')
        for i in range(5-len(temp[0])):
            temp[0]= "0"+temp[0]
        for i in range(3-len(temp[1])):
            temp[1]= temp[1]+"0"
        quantity=temp[0]+temp[1]
        print(quantity)
    else:
        pass

def decimalCheck(number):
    decimalfind = re.compile(r"\d+\.\d+")
    if decimalfind.match(number):
        decimalSplit(number, True)
    else:
        decimalSplit(number, False)

def ptGen():
    firstRun = True
    raw_id = ""
    rowdata = []
    #Pulls filename from directory where the script lives
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,'}h*.d1c'):
            filename = file
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, quotechar="\"")
        
        for row in reader:
            rowdata = row
            tranNum = rowdata[3][1:8]
            #print(tranNum)
            if firstRun:
                raw_id = rowdata[0]
                raw_id = re.sub(r'[a-z_\s-]','', raw_id, flags=re.IGNORECASE)
                firstRun = False
                tranDate = dFormat(rowdata[1])
                for x in range((6-len(raw_id))):
                    raw_id = '0' + raw_id
                siteid = raw_id
            for file in os.listdir('.'):
                if fnmatch.fnmatch(file,'}d*.d1c'):
                    DFile = file
            with open(DFile, newline='') as csvfile:
                dreader = csv.reader(csvfile, quotechar="\"")
                dPattern = "[0-9]" + tranNum
                for drow in dreader:
                    ddata = drow
                    if re.search(dPattern, drow[3]):
                        decimalCheck(drow[10]) #True = Quantity

                        #quantity = drow[10]
                        #pCode = drow[11]
                        #totAmt = drow[48]
            #print(pCode)
        #print(tranDate)
    print(siteid)
ptGen()