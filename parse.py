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
        self.hLen = 0

    def hParse(self, folder, f):
        firstRun = True
        raw_id = ""
        rowdata = []
        os.chdir(folder)
        with open(f[0], newline='') as csvfile: 
            reader = csv.reader(csvfile, quotechar="\"")
            for row in reader:
                rowdata = row
                self.tranNum[self.runCount] = rowdata[3][1:8]
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
                self.dParse(folder,f[1])
                self.vParse(folder,f[2])
                self.runCount += 1              

    #parses variables from the data file
    def dParse(self, folder, dFile): 
        os.chdir(folder)
        with open(dFile, newline='') as csvfile: #opening the data file csv
            dreader = csv.reader(csvfile, quotechar="\"")
            dPattern = "[0-9]" + self.tranNum[self.runCount] #!TODO
            for drow in dreader:
                if re.search(dPattern, drow[3]):
                    self.quantity[self.runCount] = fmt.decimalCheck(drow[10], True) #True = Quantity
                    self.totAmt[self.runCount] = fmt.decimalCheck(drow[48], False)
                    self.pCode[self.runCount] = drow[11]
                    self.tranTime[self.runCount] = fmt.tFormat(drow[2])
                    
    #parses the variables file
    def vParse(self, folder, vFile):
        os.chdir(folder)
        with open(vFile, newline='') as csvfile: #opening the variable csv file
            vreader = csv.reader(csvfile, quotechar="\"") 
            vPattern = "[0-9]" + self.tranNum[self.runCount] 
            for vrow in vreader:
                if re.search(vPattern, vrow[3]):
                    if vrow[8].lower() == "SEQUENCE#".lower():
                        self.seqnum[self.runCount] = fmt.format(vrow[9],4)
                    if vrow[8].lower() == "ODOMETER".lower():
                        self.odometer[self.runCount] = fmt.format(vrow[9],7)
                    if vrow[8].lower() == "PUMP".lower():
                        self.pump[self.runCount] = fmt.format(vrow[9],2)
                    if vrow[8].lower() == "ID_VEHCARD".lower():
                        self.id_vehicle[self.runCount] = fmt.format(vrow[9],8)
                    if vrow[8].lower() == "ID_CARD".lower():
                        self.id_card[self.runCount] = fmt.format(vrow[9],7)
                    if vrow[8].lower() == "ID_ACCT".lower():
                        self.id_acct[self.runCount] = fmt.format(vrow[9],6)
                    if vrow[8].lower() == "VEHICLE".lower() or vrow[8].lower() == "ID_VEHCARD".lower():
                        self.vehicle[self.runCount] = fmt.format(vrow[9],4)

                    #checks for null values in the variables 
                    if len(self.odometer) < self.runCount:
                        self.odometer[self.runCount] = "0000000"
                    if len(self.seqnum) < self.runCount:
                        self.seqnum[self.runCount] = "0000"
                    if len(self.pump) < self.runCount:
                        self.pump[self.runCount] = "00"
                    if len(self.id_vehicle) < self.runCount:
                        self.id_vehicle[self.runCount] = "00000000"
                    if len(self.id_card) < self.runCount:
                        self.id_card[self.runCount] = "0000000"
                    if len(self.id_acct) < self.runCount:
                        self.id_acct[self.runCount] = "000000"
                    if len(self.vehicle) < self.runCount:
                        self.vehicle[self.runCount] = "0000"
                
                

    def parse(self,folder, f):
        os.chdir(folder)
        self.seqnum = self.fillWZero(f, 4)
        self.totAmt = self.fillWZero(f, 6)
        self.pCode = self.fillWZero(f, 2)
        self.quantity = self.fillWZero(f, 8)
        self.odometer = self.fillWZero(f, 7)
        self.pump = self.fillWZero(f, 2)
        self.tranNum = self.fillWZero(f,4)
        self.tranTime = self.fillWZero(f,4)
        self.id_vehicle = self.fillWZero(f,8)
        self.id_card = self.fillWZero(f, 7)
        self.id_acct = self.fillWZero(f, 6)
        self.vehicle = self.fillWZero(f, 4)
        self.hParse(folder, f)
        for i in range(self.runCount): 
            temp = pt.ptLine(self.siteid,self.seqnum[i],self.totAmt[i],self.pCode[i],self.quantity[i],self.odometer[i],
                            self.pump[i],self.tranNum[i],self.tranDate,self.tranTime[i],self.id_vehicle[i],
                            self.id_card[i],self.id_acct[i],self.vehicle[i])
            self.pList.append(temp)
        return self
        
    def fillWZero(self, f, length):
        temp = ""
        v = []
        if(self.hLen == 0):
            with open(f[0], newline='') as csvfile: 
                reader = csv.reader(csvfile, quotechar="\"")
                for __ in reader:
                    self.hLen += 1
        for __ in range(length):
            temp = temp + "0"
        for __ in range(self.hLen):
            v.append(temp)
        return v
            

