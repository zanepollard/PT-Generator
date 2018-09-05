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
        self.tranDate = []
        self.nDV = ""
        self.pList = []
        self.transactions = {}

    def hParse(self, folder, f):
        firstRun = True
        raw_id = ""
        rowdata = []
        os.chdir(folder)
        with open(f, newline='') as csvfile: 
            reader = csv.reader(csvfile, quotechar="\"")
            for row in reader:
                rowdata = row

                #self.rawTran[self.runCount] = rowdata[3]
                if rowdata[3] not in self.transactions:
                    self.transactions[rowdata[3]] = {'seqnum': "0000",'totAmt': "000000", 
                                                'pCode': "00", 'quantity': "00000000", 
                                                'odometer': "0000000", 'pump': "00",
                                                'tranNum': "0000",'tranTime': "0000",
                                                'id_vehicle': "00000000", 'id_card': "0000000",
                                                'id_acct': "000000", 'vehicle': "0000",
                                                'price': "00000000"} 
                self.transactions[rowdata[3]]['tranNum'] = fmt.tNumFMT(rowdata[3])
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

    #parses variables from the data file
    def dParse(self, folder, dFile): 
        os.chdir(folder)
        with open(dFile, newline='') as csvfile: #opening the data file csv
            dreader = csv.reader(csvfile, quotechar="\"")
            #dPattern = "[0-9]*" + self.rawTran[self.runCount] #!TODO
            for drow in dreader:
                    self.transactions[drow[3]]['price'] = fmt.pFormat(drow[16])
                    self.transactions[drow[3]]['quantity'] = fmt.decimalCheck(drow[10], True) #True = Quantity
                    self.transactions[drow[3]]['totAmt'] = fmt.decimalCheck(drow[48], False)
                    self.transactions[drow[3]]['pCode'] = drow[11]
                    self.transactions[drow[3]]['tranTime'] = fmt.tFormat(drow[2])
                    
    #parses the variables file
    def vParse(self, folder, vFile):
        os.chdir(folder)
        with open(vFile, newline='') as csvfile: #opening the variable csv file
            vreader = csv.reader(csvfile, quotechar="\"") 
            #vPattern = "[0-9]*" + self.rawTran[self.runCount] 
            for vrow in vreader:
                if vrow[8].lower() == "SEQUENCE#".lower():
                    self.transactions[vrow[3]]['seqnum'] = fmt.format(vrow[9],4)
                if vrow[8].lower() == "ODOMETER".lower():
                    self.transactions[vrow[3]]['odometer'] = fmt.format(vrow[9],7)
                if vrow[8].lower() == "PUMP".lower():
                    self.transactions[vrow[3]]['pump'] = fmt.format(vrow[9],2)
                if vrow[8].lower() == "VEHICLE".lower() or vrow[8].lower() == "ID_VEHICLE" or vrow[8].lower() == "ID_VEHCARD".lower():
                   self.transactions[vrow[3]]['vehicle'] = fmt.format(vrow[9],8)
                if vrow[8].lower() == "ID_CARD".lower():
                    self.transactions[vrow[3]]['id_card'] = fmt.format(vrow[9],7)
                if vrow[8].lower() == "ID_ACCT".lower():
                    self.transactions[vrow[3]]['id_acct'] = fmt.format(vrow[9],6)
                if vrow[8].lower() == "ID_VEHCARD".lower() or vrow[8].lower() == "ID_VEHICLE" or vrow[8].lower() == "VEHICLE".lower():
                    self.transactions[vrow[3]]['id_vehicle'] = fmt.format(vrow[9],4)

    def parse(self,folder, f):
        os.chdir(folder)

        self.hParse(folder, f[0])
        self.dParse(folder, f[1])
        self.vParse(folder, f[2])
        
        for i in self.transactions:
            temp = pt.ptLine(self.siteid,self.transactions[i]['seqnum'],self.transactions[i]['totAmt'],self.transactions[i]['pCode'],self.transactions[i]['price'],self.transactions[i]['quantity'],self.transactions[i]['odometer'],
                            self.transactions[i]['pump'],self.transactions[i]['tranNum'],self.tranDate,self.transactions[i]['tranTime'],self.transactions[i]['vehicle'],
                            self.transactions[i]['id_card'],self.transactions[i]['id_acct'],self.transactions[i]['id_vehicle']) 
            self.pList.append(temp)
        return self
        '''
        for i in range(self.runCount): 
            temp = pt.ptLine(self.siteid,self.seqnum[i],self.totAmt[i],self.pCode[i],self.price[i],self.quantity[i],self.odometer[i],
                            self.pump[i],self.tranNum[i],self.tranDate,self.tranTime[i],self.id_vehicle[i],
                            self.id_card[i],self.id_acct[i],self.vehicle[i]) 
            self.pList.append(temp)
        return self
        '''
            
