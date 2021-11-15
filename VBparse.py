import transaction
import os
import csv

class parse:


    def __init__(self):
        self.tranDate = ""
        self.transactions = {}


    #Parses header sales file
    def hParse(self, folder, hFile):
        os.chdir(folder)
        with open(hFile, newline='', errors="ignore") as csvfile: 
            reader = csv.reader(csvfile, quotechar="\"")
            for row in reader:
                if row[3] not in self.transactions:
                    self.transactions[row[3]] = transaction.transaction()
                    self.transactions[row[3]].set_tranNum(str(row[3]))
                    self.transactions[row[3]].set_siteID(str(row[0]))
    

    #Parses data sales file
    def dParse(self, folder, dFile): 
        os.chdir(folder)
        with open(dFile, newline='', errors="ignore") as csvfile:
            dreader = csv.reader(csvfile, quotechar="\"")
            for dRow in dreader:
                if dRow[9] == "P":
                    self.transactions[dRow[3]].set_price(str(dRow[16]))
                    self.transactions[dRow[3]].set_quantity(str(dRow[10]))
                    self.transactions[dRow[3]].set_tranTime(str(dRow[2][0:2] + dRow[2][3:5]))
                    self.transactions[dRow[3]].set_tranDate(str(dRow[1][6:10] + dRow[1][0:2] + dRow[1][3:5]))
                    self.tranDate = str(dRow[1][6:10] + dRow[1][0:2] + dRow[1][3:5])
                    self.transactions[dRow[3]].set_pCode(str(dRow[11]))
                    self.transactions[dRow[3]].set_totalAmount(str(dRow[48]))
                    self.transactions[dRow[3]].set_pName(str(dRow[14]))
                    

    #Parses variables sales file
    def vParse(self, folder, vFile):
        os.chdir(folder)
        with open(vFile, newline='', errors="ignore") as csvfile:
            #nullReader = csv.reader(x.replace('\0', '') for x in csvfile)
            #vreader = csv.reader(csvfile, quotechar="\"")
            vreader = csv.reader((x.replace('\0', '') for x in csvfile), quotechar="\"")
            for vrow in vreader:
                if vrow[8].lower() == "SEQUENCE#".lower():
                    self.transactions[vrow[3]].set_seqNum(str(vrow[9]))
                elif vrow[8].lower() == "ODOMETER".lower():
                    self.transactions[vrow[3]].set_odometer(str(vrow[9]))
                elif vrow[8].lower() == "PUMP".lower():
                    self.transactions[vrow[3]].set_pump(str(vrow[9]))
                elif vrow[8].lower() == "VEHICLE".lower() or vrow[8].lower() == "ID_VEHICLE" or vrow[8].lower() == "ID_VEHCARD".lower():
                    self.transactions[vrow[3]].set_vehicle(str(vrow[9]))
                elif (vrow[8].lower() == "ID_CARD".lower()) or (vrow[8].lower() == "ID_CRD_NR".lower()):
                    self.transactions[vrow[3]].set_card(str(vrow[9]))
                elif vrow[8].lower() == "ID_ACCT".lower() or vrow[8].lower() == "ID_MASKED".lower():
                    self.transactions[vrow[3]].set_account(str(vrow[9]))
                elif vrow[8].lower() == "ID_VEHCARD".lower() or vrow[8].lower() == "ID_VEHICLE" or vrow[8].lower() == "VEHICLE".lower():
                    self.transactions[vrow[3]].set_vehicleID(str(vrow[9]))
                elif vrow[8].lower() == "R_CODE".lower() or vrow[8].lower() == "R_APPROVAL".lower():
                    self.transactions[vrow[3]].set_authNum(str(vrow[9]))
                elif vrow[8].lower() == "ID_PREFIX".lower():
                    self.transactions[vrow[3]].set_cardType(str(vrow[9]))


    def parse(self, input_folder, fileList, config_data):
        os.chdir(input_folder)
        print(f"Parsing {fileList[0]}, {fileList[1]}, {fileList[2]}")
        self.hParse(input_folder, fileList[0])
        self.dParse(input_folder, fileList[1])
        self.vParse(input_folder, fileList[2])

        return self
            