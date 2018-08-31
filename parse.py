import pt
import os
import fnmatch
import csv
import fmt
import re
import files


class parse:
    def __init__(self):
        self.siteid = []
        self.seqnum = []
        self.totAmt = []
        self.pCode = []
        self.quantity = []
        self.odometer = []
        self.pump = []
        self.tranNum = []
        self.tranDate = []
        self.tranTime = []
        self.id_vehicle = []
        self.id_card = []
        self.id_acct = []
        self.vehicle = []
        self.runCount = 0
        self.nDV = ""
        self.pList = []

    def hParse(self, folder):
        firstRun = True
        raw_id = ""
        rowdata = []
        filename = None
        #Pulls filename from directory where the script lives
        for file in os.listdir(folder):
            if fnmatch.fnmatch(file,'}h*.d1c'):
                filename = file
        if filename == None:
            print("No '}h*.d1c' file found! ")
            os.system('pause')
            exit()
        os.chdir(folder)
        with open(filename, newline='') as csvfile: 
            reader = csv.reader(csvfile, quotechar="\"")
            for row in reader:
                rowdata = row
                self.tranNum.append(rowdata[3][1:8])
                if firstRun: #Pulls all the single use variables into memory from the csv
                    raw_id = rowdata[0]
                    raw_id = re.sub(r'[a-z_\s-]','', raw_id, flags=re.IGNORECASE)
                    firstRun = False
                    self.nDV = rowdata[1]
                    self.tranDate = fmt.dFormat(rowdata[1])
                    siteid = raw_id
                    for __ in range((6 - len(raw_id))):
                        siteid = '0' + siteid
                    self.siteid = siteid
                self.dParse(folder)
                self.vParse(folder)
                self.runCount += 1                  

    #parses variables from the data file
    def dParse(self, folder):
        DFile = None
        for file in os.listdir(folder):
            if fnmatch.fnmatch(file,'}}d{0}.d1c'.format(self.tranDate)):
                DFile = file
        if DFile == None:
            print("No '}d*.d1c' file found!")
            os.system('pause')
            exit()    
        with open(DFile, newline='') as csvfile: #opening the data file csv
            dreader = csv.reader(csvfile, quotechar="\"")
            dPattern = "[0-9]" + self.tranNum[self.runCount] #!TODO
            for drow in dreader:
                if re.search(dPattern, drow[3]):
                    self.quantity.append(fmt.decimalCheck(drow[10], True)) #True = Quantity
                    self.totAmt.append(fmt.decimalCheck(drow[48], False))
                    self.pCode.append(drow[11])
                    self.tranTime.append(fmt.tFormat(drow[2]))
                    
    #parses the variables file
    def vParse(self, folder):
        for file in os.listdir(folder):
            if fnmatch.fnmatch(file,'}}v{0}.d1c'.format(self.tranDate)):
                VFile = file    
        with open(VFile, newline='') as csvfile: #opening the variable csv file
            vreader = csv.reader(csvfile, quotechar="\"") 
            vPattern = "[0-9]" + self.tranNum[self.runCount] 
            for vrow in vreader:
                if re.search(vPattern, vrow[3]):
                    if vrow[8].lower() == "SEQUENCE#".lower():
                        self.seqnum.append(fmt.format(vrow[9],4))
                    if vrow[8].lower() == "ODOMETER".lower():
                        self.odometer.append(fmt.format(vrow[9],7))
                    if vrow[8].lower() == "PUMP".lower():
                        self.pump.append(fmt.format(vrow[9],2))
                    if vrow[8].lower() == "ID_VEHICLE".lower() or vrow[8].lower() == "ID_VEHCARD".lower():
                        self.id_vehicle.append(fmt.format(vrow[9],8))
                    if vrow[8].lower() == "ID_CARD".lower():
                        self.id_card.append(fmt.format(vrow[9],7))
                    if vrow[8].lower() == "ID_ACCT".lower():
                        self.id_acct.append(fmt.format(vrow[9],6))
                    if vrow[8].lower() == "VEHICLE".lower() or vrow[8].lower() == "ID_VEHCARD".lower():
                        self.vehicle.append(fmt.format(vrow[9],4))

                    #checks for null values in the variables 
                    if len(self.odometer) < self.runCount:
                        self.odometer.append("0000000")
                    if len(self.seqnum) < self.runCount:
                        self.seqnum.append("0000")
                    if len(self.pump) < self.runCount:
                        self.pump.append("00")
                    if len(self.id_vehicle) < self.runCount:
                        self.id_vehicle.append("00000000")
                    if len(self.id_card) < self.runCount:
                        self.id_card.append("0000000")
                    if len(self.id_acct) < self.runCount:
                        self.id_acct.append("000000")
                    if len(self.vehicle) < self.runCount:
                        self.vehicle.append("0000")

    def parse(self, folder):
        self.hParse(folder)
        
        for i in range(self.runCount):
            
            temp = pt.ptLine(self.siteid,self.seqnum[i],self.totAmt[i],self.pCode[i],self.quantity[i],self.odometer[i],
                            self.pump[i],self.tranNum[i],self.tranDate,self.tranTime[i],self.id_vehicle[i],
                            self.id_card[i],self.id_acct[i],self.vehicle[i])
            self.pList.append(temp)
        return self
        
    def fillWZero(self, v, length):
        temp = ""
        
        for __ in range(length):
            temp = temp + "0"
        for __ in range(run):
            v.append(temp)
            

