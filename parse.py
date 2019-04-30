import pt
import os
import csv
import fmt
import re
import files


class parse:
    def __init__(self):
        self.siteid = []
        self.tranDate = ""
        self.nDV = ""
        self.pList = []
        self.transactions = {}

    #Parses header sales file
    def hParse(self, folder, hFile, gasboy):
        firstRun = True
        raw_id = ""
        rowdata = []
        os.chdir(folder)
        with open(hFile, newline='') as csvfile: 
            reader = csv.reader(csvfile, quotechar="\"")
            #Goes through each row in current header file
            for row in reader:
                rowdata = row
                if not gasboy:
                    if rowdata[3] not in self.transactions:
                        #Default values for standard PT file, needed to ensure every line outputs properly
                        #This is needed because the VB6 code sometimes has variables missing from the sales files.
                        # Missing variables will break back office PT import, better to have filler zeros than a file that can't be imported, or has missing transactions. 
                        self.transactions[rowdata[3]] = {'seqnum': "0000",'totAmt': "000000", 'pCode': "00", 'quantity': "00000000", 
                                                    'odometer': "0000000", 'pump': "00",'tranNum': "0000",'tranTime': "0000",
                                                    'id_vehicle': "00000000", 'id_card': "0000000",'id_acct': "000000", 'vehicle': "0000", 'price': "00000000"} 
                else:
                    if rowdata[3] not in self.transactions:
                        #Default gasboy variable values. Same reasoon as above.
                        self.transactions[rowdata[3]] = {'seqnum': "0000",'totAmt': "000000", 'pCode': "00", 'quantity': "00000000", 
                                                    'odometer': "       ", 'pump': "00 ",'tranNum': "0000",'tranTime': "0000",
                                                    'id_vehicle': "          ", 'id_card': "       ",'id_acct': "      ", 'vehicle': "          ", 'price': "00000000"}
                self.transactions[rowdata[3]]['tranNum'] = fmt.tNumFMT(rowdata[3])
                #This statement is here for processes that only have to be done once per file set. Pulls the siteid and date, processing them 
                #Based on if it is the standard PT output or the gasboy output
                if firstRun:
                    raw_id = re.sub(r'[a-z_\s-]','', rowdata[0], flags=re.IGNORECASE)
                    #length check for gasboy output
                    if len(raw_id)>2 and gasboy:
                        raw_id = raw_id[len(raw_id)-2:len(raw_id)]
                    firstRun = False
                    self.nDV = rowdata[1]
                    if not gasboy:
                        self.tranDate = fmt.dFormat(rowdata[1])
                    else:
                        dTemp = rowdata[1]
                        dTemp = dTemp.split("-") 
                        if dTemp[0][0] == "0":
                            dTemp[0] = " " + dTemp[0][1]
                        dTemp[2] = dTemp[2][2:4]
                        self.tranDate = dTemp[0] + "/" +  dTemp[1] + "/" + dTemp[2] + " "
                    siteid = raw_id
                    if not gasboy:
                        for __ in range((6 - len(raw_id))):
                            siteid = '0' + siteid
                    else:
                        siteid = siteid + " "
                    self.siteid = siteid       

    #Parses data sales file
    def dParse(self, folder, dFile, gasboy): 
        os.chdir(folder)
        #Sets variables in dictionary based on the key value of the transaction number. (dRow[3])
        #Depending on the output style the variables will be formatted differently
        with open(dFile, newline='') as csvfile:
            dreader = csv.reader(csvfile, quotechar="\"")
            if not gasboy:
                for dRow in dreader:
                    self.transactions[dRow[3]]['price'] = fmt.pFormat(dRow[16],gasboy)
                    self.transactions[dRow[3]]['quantity'] = fmt.decimalCheck(dRow[10], True) #True = Quantity
                    self.transactions[dRow[3]]['totAmt'] = fmt.decimalCheck(dRow[48], False)
                    self.transactions[dRow[3]]['pCode'] = dRow[11]
                    self.transactions[dRow[3]]['tranTime'] = fmt.tFormat(dRow[2],gasboy)
            else:
                for dRow in dreader:
                    self.transactions[dRow[3]]['price'] = fmt.pFormat(dRow[16], gasboy)
                    self.transactions[dRow[3]]['quantity'] = fmt.gBoyFormat(dRow[10], 5, 3)
                    self.transactions[dRow[3]]['totAmt'] = fmt.gBoyFormat(dRow[48], 6,2)
                    self.transactions[dRow[3]]['pCode'] = dRow[11] + " "
                    self.transactions[dRow[3]]['tranTime'] = fmt.tFormat(dRow[2],gasboy)

    # parses }v8*.d1c file once and places variables into the dictionary using the transaction number as the key                 
    def vParse(self, folder, vFile, gasboy):
        os.chdir(folder)
        with open(vFile, newline='') as csvfile:
            vreader = csv.reader(csvfile, quotechar="\"") 
            if not gasboy:
                for vrow in vreader:
                    if vrow[8].lower() == "SEQUENCE#".lower():
                        self.transactions[vrow[3]]['seqnum'] = fmt.format(vrow[9],4,gasboy)
                    if vrow[8].lower() == "ODOMETER".lower():
                        self.transactions[vrow[3]]['odometer'] = fmt.format(vrow[9],7,gasboy)
                    if vrow[8].lower() == "PUMP".lower():
                        self.transactions[vrow[3]]['pump'] = fmt.format(vrow[9],2,gasboy)
                    if vrow[8].lower() == "VEHICLE".lower() or vrow[8].lower() == "ID_VEHICLE" or vrow[8].lower() == "ID_VEHCARD".lower():
                        self.transactions[vrow[3]]['vehicle'] = fmt.format(vrow[9],8,gasboy)
                    if vrow[8].lower() == "ID_CARD".lower():
                        self.transactions[vrow[3]]['id_card'] = fmt.format(vrow[9],7,gasboy)
                    if vrow[8].lower() == "ID_ACCT".lower():
                        self.transactions[vrow[3]]['id_acct'] = fmt.format(vrow[9],6,gasboy)
                    if vrow[8].lower() == "ID_VEHCARD".lower() or vrow[8].lower() == "ID_VEHICLE" or vrow[8].lower() == "VEHICLE".lower():
                        self.transactions[vrow[3]]['id_vehicle'] = fmt.format(vrow[9],4,gasboy)
            else:
                for vrow in vreader:
                    if vrow[8].lower() == "SEQUENCE#".lower():
                        self.transactions[vrow[3]]['seqnum'] = fmt.format(vrow[9],4,gasboy)
                    if vrow[8].lower() == "ODOMETER".lower():
                        self.transactions[vrow[3]]['odometer'] = fmt.format(vrow[9],6,gasboy)
                    if vrow[8].lower() == "PUMP".lower():
                        self.transactions[vrow[3]]['pump'] = fmt.format(vrow[9],2,gasboy)
                    if vrow[8].lower() == "VEHICLE".lower() or vrow[8].lower() == "ID_VEHICLE" or vrow[8].lower() == "ID_VEHCARD".lower():
                        self.transactions[vrow[3]]['vehicle'] = fmt.format(vrow[9],9,gasboy)
                    if vrow[8].lower() == "ID_CARD".lower():
                        self.transactions[vrow[3]]['id_card'] = fmt.format(vrow[9],6,gasboy)
                    if vrow[8].lower() == "ID_ACCT".lower():
                        self.transactions[vrow[3]]['id_acct'] = fmt.format(vrow[9],5,gasboy)
                    if vrow[8].lower() == "ID_VEHCARD".lower() or vrow[8].lower() == "ID_VEHICLE" or vrow[8].lower() == "VEHICLE".lower():
                        self.transactions[vrow[3]]['id_vehicle'] = fmt.format(vrow[9],9,gasboy)

    def parse(self, input_folder, f, config_data):
        os.chdir(input_folder)
        gasboy = config_data.get('gasboyOutput')

        if config_data.get('multiDayPT') == False: 
            self.hParse(input_folder, f[0], gasboy)
            self.dParse(input_folder, f[1], gasboy)
            self.vParse(input_folder, f[2], gasboy) 
        else:
            for i in range(len(f[0])):
                #f in this case is a list of filesets as opposed to just a singular fileset
                self.hParse(input_folder, f[0][i], gasboy)
                self.dParse(input_folder, f[1][i], gasboy)
                self.vParse(input_folder, f[2][i], gasboy)

        #creates PT line objects for each transaction 
        for i in self.transactions:
                temp = pt.ptLine(self.siteid,self.transactions[i]['seqnum'],self.transactions[i]['totAmt'],self.transactions[i]['pCode'],self.transactions[i]['price'],self.transactions[i]['quantity'],self.transactions[i]['odometer'],
                                self.transactions[i]['pump'],self.transactions[i]['tranNum'],self.tranDate,self.transactions[i]['tranTime'],self.transactions[i]['vehicle'],
                                self.transactions[i]['id_card'],self.transactions[i]['id_acct'],self.transactions[i]['id_vehicle']) 
                self.pList.append(temp)
        
        return self
            
