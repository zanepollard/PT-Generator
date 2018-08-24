import pt
import os
import fnmatch
import csv
import fmt
import re
import files

runCount = 0
nDV = ""
v = pt
siteid = ""
seqnum = []
totAmt = []
pCode = []
quantity = []
odometer = []
pump = []
tranNum =[]
tranDate = []
tranTime = []
id_vehicle = []
id_card = []
id_acct = []
vehicle = []
pList =[]

def hParse():
    global runCount
    global siteid
    global tranDate
    global nDV
    firstRun = True
    raw_id = ""
    rowdata = []
    filename = None
    #Pulls filename from directory where the script lives
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,'}h*.d1c'):
            filename = file
    if filename == None:
        print("No '}h*.d1c' file found! ")
        os.system('pause')
        exit()
    with open(filename, newline='') as csvfile: 
        reader = csv.reader(csvfile, quotechar="\"")
        for row in reader:
            rowdata = row
            tranNum.append(rowdata[3][1:8])
            if firstRun: #Pulls all the single use variables into memory from the csv
                raw_id = rowdata[0]
                raw_id = re.sub(r'[a-z_\s-]','', raw_id, flags=re.IGNORECASE)
                firstRun = False
                nDV = rowdata[1]
                tranDate = fmt.dFormat(rowdata[1])
                siteid = raw_id
                for __ in range((6 - len(raw_id))):
                    siteid = '0' + siteid
            dParse()
            vParse()                         
            runCount += 1
    #files.fileIO()

#parses variables from the data file
def dParse():
    DFile = None
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,'}d*.d1c'):
            DFile = file
    if DFile == None:
        print("No '}d*.d1c' file found!")
        os.system('pause')
        exit()    
    with open(DFile, newline='') as csvfile: #opening the data file csv
        dreader = csv.reader(csvfile, quotechar="\"")
        dPattern = "[0-9]" + tranNum[runCount] #!TODO
        for drow in dreader:
            if re.search(dPattern, drow[3]):
                quantity.append(fmt.decimalCheck(drow[10], True)) #True = Quantity
                totAmt.append(fmt.decimalCheck(drow[48], False))
                pCode.append(drow[11])
                tranTime.append(fmt.tFormat(drow[2]))
                
#parses the variables file
def vParse():
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,'}v*.d1c'):
            VFile = file    
    with open(VFile, newline='') as csvfile: #opening the variable csv file
        vreader = csv.reader(csvfile, quotechar="\"") 
        for vrow in vreader:
            if tranNum[runCount] == vrow[3][1:5]:
                if vrow[8] == "SEQUENCE#":
                    seqnum.append(fmt.format(vrow[9],4))
                elif vrow[8] == "ODOMETER":
                    odometer.append(fmt.format(vrow[9],7))
                elif vrow[8] == "pump":
                    pump.append(fmt.format(vrow[9],2))
                elif vrow[8] == "ID_VEHICLE":
                    id_vehicle.append(fmt.format(vrow[9],8))
                elif vrow[8] == "ID_CARD":
                    id_card.append(fmt.format(vrow[9],7))
                elif vrow[8] == "ID_ACCT":
                    id_acct.append(fmt.format(vrow[9],6))
                elif vrow[8] == "VEHICLE":
                    vehicle.append(fmt.format(vrow[9],4))

                #checks for null values in the variables 
                if len(odometer) < runCount:
                    odometer.append("0000000")
                elif len(seqnum) < runCount:
                    seqnum.append("0000")
                elif len(pump) < runCount:
                    pump.append("00")
                elif len(id_vehicle) < runCount:
                    id_vehicle.append("00000000")
                elif len(id_card) < runCount:
                    id_card.append("0000000")
                elif len(id_acct) < runCount:
                    id_acct.append("000000")
                elif len(vehicle) < runCount:
                    vehicle.append("0000")

def parse():
    hParse()
    
    for i in range(runCount):
        
        temp = pt.ptLine(siteid,seqnum[i],totAmt[i],pCode[i],quantity[i],odometer[i],
                        pump[i],tranNum[i],tranDate,tranTime[i],id_vehicle[i],
                        id_card[i],id_acct[i],vehicle[i])
        pList.append(temp)
    