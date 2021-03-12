import pt
import os
import csv
import fmt
import re
import files
import yaml

class parse:
    def __init__(self):
        self.siteid = ""
        self.tranDate = ""
        self.nDV = ""
        self.pList = []
        self.transactions = {}
        config_data = None
        with open('config.yaml') as cfg:
            config_data = yaml.load(cfg, Loader=yaml.FullLoader)
        self.ptOutput = bool(config_data['ptOutput'])
        self.gasboy = bool(config_data['gasboyOutput'])
        self.csvOutput = bool(config_data['csvOutput'])
        self.merchantAg = bool(config_data['merchantAg'])

    #Parses header sales file
    def hParse(self, folder, hFile):
        firstRun = True
        raw_id = ""
        rowdata = []
        os.chdir(folder)
        with open(hFile, newline='', errors="ignore") as csvfile: 
            reader = csv.reader(csvfile, quotechar="\"")
            if self.ptOutput:
                for row in reader:
                    rowdata = row
                    if rowdata[3] not in self.transactions:
                        #Default values for standard PT file, needed to ensure every line outputs properly
                        #This is needed because the VB6 code sometimes has variables missing from the sales files.
                        # Missing variables will break back office PT import, better to have filler zeros than a file that can't be imported, or has missing transactions. 
                        self.transactions[rowdata[3]] = {'seqnum': "0000",'totAmt': "0.00", 'pCode': "00", 'quantity': "0.0", 
                                                    'odometer': "0", 'pump': "0",'tranNum': "00000",'tranTime': "00:00:00", 'tranDate': "01-01-2000",
                                                    'id_vehicle': "0", 'id_card': "0",'id_acct': "0", 'vehicle': "0", 'price': "0.000",
                                                    'authNum': '', 'pName': '', 'id_card_type': ''}
                        self.transactions[rowdata[3]]['tranNum'] = fmt.tNumFMT(rowdata[3])
                        if firstRun:
                            firstRun = False
                            raw_id = re.sub(r'[a-z_\s-]','', rowdata[0], flags=re.IGNORECASE)
                            siteid = raw_id
                            for __ in range((6 - len(raw_id))):
                                siteid = '0' + siteid
                            self.siteid = siteid
                            self.nDV = rowdata[1]

            elif self.gasboy:
                for row in reader:
                    rowdata = row
                    if rowdata[3] not in self.transactions:
                        #Default gasboy variable values. Same reasoon as above.
                        self.transactions[rowdata[3]] = {'seqnum': "0000",'totAmt': "0.0", 'pCode': "00", 'quantity': "0.0", 
                                                    'odometer': "000000", 'pump': "0",'tranNum': "00000",'tranTime': "00:00:00", 'tranDate': '01-01-2000',
                                                    'id_vehicle': "          ", 'id_card': "000000",'id_acct': "00000", 'vehicle': "          ", 'price': "0.000",
                                                    'authNum': '', 'pName': '', 'id_card_type': ''}
                    self.transactions[rowdata[3]]['tranNum'] = fmt.tNumFMT(rowdata[3])
                    if firstRun:
                        firstRun = False
                        raw_id = re.sub(r'[a-z_\s-]','', rowdata[0], flags=re.IGNORECASE)
                        if len(raw_id)>2:
                            raw_id = raw_id[len(raw_id)-2:len(raw_id)]
                        siteid = raw_id
                        siteid = siteid + " "
                        dTemp = rowdata[1]
                        dTemp = dTemp.split("-") 
                        if dTemp[0][0] == "0":
                            dTemp[0] = " " + dTemp[0][1]
                        dTemp[2] = dTemp[2][2:4]
                        self.tranDate = dTemp[0] + "/" +  dTemp[1] + "/" + dTemp[2] + " "
                        self.siteid = siteid
                        self.nDV = rowdata[1]

            elif self.csvOutput:
                for row in reader:
                    rowdata = row
                    if rowdata[3] not in self.transactions:
                        self.transactions[rowdata[3]] = {'seqnum': 0,'totAmt': 0, 'pCode': "N/A", 'quantity': 0, 'odometer': 0, 'pump': 0,'tranNum': 0,'tranTime': "N/A", 'tranDate': "N/A",
                                                    'id_vehicle': 0, 'id_card': "",'id_acct': "", 'vehicle': "N/A", 'price': 0, 'authNum': 0, 'pName': "N/A", 'id_card_type': "N/A"}
                        self.transactions[rowdata[3]]['tranNum'] = rowdata[3]
                        if firstRun:
                            firstRun = False
                            raw_id = re.sub(r'[a-z_\s-]','', rowdata[0], flags=re.IGNORECASE)
                            siteid = raw_id
                            siteid = rowdata[0]
                            self.transactions[rowdata[3]]['tranDate'] = rowdata[1]
                            self.siteid = siteid
                            self.nDV = rowdata[1]

            elif self.merchantAg:
                for row in reader:
                    rowdata = row
                    if rowdata[3] not in self.transactions:
                        self.transactions[rowdata[3]] = {'seqnum': "0000",'totAmt': "000000000", 'pCode': "00", 'quantity': "000000000", 'description': "                          ",
                                                    'odometer': "000000000", 'pump': "00",'tranNum': "000000000",'tranTime': "0000", 'tranDate': "00000000",
                                                    'id_vehicle': "00000000", 'id_card': "000000000",'id_acct': "000000000", 'vehicle': "000000000", 'price': "00000000",
                                                    'pName': '                          ', 'id_card_type': 'UNK  ', 'authNum': ''}
                        self.transactions[rowdata[3]]['tranNum'] = fmt.mAgPadding(9,rowdata[3],True,"0")
                        if firstRun:
                            firstRun = False
                            raw_id = re.sub(r'[a-z_\s-]','', rowdata[0], flags=re.IGNORECASE)
                            siteid = raw_id
                            for __ in range(8-len(raw_id)):
                                siteid = '0' + siteid
                            self.siteid = siteid
                            self.nDV = rowdata[1]
                
    

    #Parses data sales file
    def dParse(self, folder, dFile): 
        os.chdir(folder)
        with open(dFile, newline='', errors="ignore") as csvfile:
            dreader = csv.reader(csvfile, quotechar="\"")
            for dRow in dreader:
                if dRow[9] == "P":
                    self.transactions[dRow[3]]['price'] = dRow[16]
                    self.transactions[dRow[3]]['quantity'] = dRow[10]
                    self.transactions[dRow[3]]['tranTime'] = dRow[2][0:5]
                    self.transactions[dRow[3]]['tranDate'] = dRow[1]
                    self.transactions[dRow[3]]['pCode'] = dRow[11]
                    self.transactions[dRow[3]]['totAmt'] = dRow[48]
                    self.transactions[dRow[3]]['pName'] = dRow[14]
                    


    def vParse(self, folder, vFile):
        os.chdir(folder)
        with open(vFile, newline='', errors="ignore") as csvfile:
            vreader = csv.reader(csvfile, quotechar="\"")
            for vrow in vreader:
                if vrow[8].lower() == "SEQUENCE#".lower():
                    self.transactions[vrow[3]]['seqnum'] = vrow[9]
                elif vrow[8].lower() == "ODOMETER".lower():
                    self.transactions[vrow[3]]['odometer'] = vrow[9]
                elif vrow[8].lower() == "PUMP".lower():
                    self.transactions[vrow[3]]['pump'] = vrow[9]
                elif vrow[8].lower() == "VEHICLE".lower() or vrow[8].lower() == "ID_VEHICLE" or vrow[8].lower() == "ID_VEHCARD".lower():
                    self.transactions[vrow[3]]['vehicle'] = vrow[9]
                elif (vrow[8].lower() == "ID_CARD".lower()) or (vrow[8].lower() == "ID_CRD_NR".lower()):
                    self.transactions[vrow[3]]['id_card'] = vrow[9]
                elif vrow[8].lower() == "ID_ACCT".lower() or vrow[8].lower() == "ID_MASKED".lower():
                    self.transactions[vrow[3]]['id_acct'] = vrow[9]
                elif vrow[8].lower() == "ID_VEHCARD".lower() or vrow[8].lower() == "ID_VEHICLE" or vrow[8].lower() == "VEHICLE".lower():
                    self.transactions[vrow[3]]['id_vehicle'] = vrow[9]
                elif vrow[8].lower() == "R_CODE".lower() or vrow[8].lower() == "R_APPROVAL".lower():
                    self.transactions[vrow[3]]['authNum'] = vrow[9]
                elif vrow[8].lower() == "ID_PREFIX".lower():
                    self.transactions[vrow[3]]['id_card_type'] = vrow[9]


    def parse(self, input_folder, f, config_data):
        os.chdir(input_folder)

        if config_data.get('multiDayPT') == False: 
            self.hParse(input_folder, f[0])
            self.dParse(input_folder, f[1])
            self.vParse(input_folder, f[2]) 
        else:
            for i in range(len(f[0])):
                #f in this case is a list of filesets as opposed to just a singular fileset
                self.hParse(input_folder, f[0][i])
                self.dParse(input_folder, f[1][i])
                self.vParse(input_folder, f[2][i])

        #creates PT line objects for each transaction 
        for i in self.transactions:
            if self.ptOutput:
                temp = pt.ptLine(self.siteid,fmt.format(self.transactions[i]['seqnum'], 4, False),fmt.decimalCheck(self.transactions[i]['totAmt'], False),self.transactions[i]['pCode'],fmt.pFormat(self.transactions[i]['price'], False),fmt.decimalCheck(self.transactions[i]['quantity'], False),fmt.format(self.transactions[i]['odometer'], 7, False),
                                    fmt.format(self.transactions[i]['pump'], 2, False),self.transactions[i]['tranNum'],fmt.dFormat(self.transactions[i]['tranDate']),fmt.tFormat(self.transactions[i]['tranTime'], False),fmt.format(self.transactions[i]['vehicle'], 8, False),
                                    fmt.format(self.transactions[i]['id_card'],7, False), fmt.format(self.transactions[i]['id_acct'], 6, False), fmt.format(self.transactions[i]['id_vehicle'], 4, False),0,0,0)
                self.pList.append(temp)

            elif self.gasboy:
                temp = pt.ptLine(self.siteid,fmt.format(self.transactions[i]['seqnum'], 4, True),fmt.gBoyFormat(self.transactions[i]['totAmt'],6,2),self.transactions[i]['pCode'],fmt.pFormat(self.transactions[i]['price'], True),fmt.gBoyFormat(self.transactions[i]['quantity'],5,3),fmt.format(self.transactions[i]['odometer'], 6, True),
                                    fmt.format(self.transactions[i]['pump'], 2, True),self.transactions[i]['tranNum'],fmt.dGasboyFormat(self.transactions[i]['tranDate']),fmt.tFormat(self.transactions[i]['tranTime'], True),fmt.format(self.transactions[i]['vehicle'], 9, True),
                                    fmt.format(self.transactions[i]['id_card'],6,True), fmt.format(self.transactions[i]['id_acct'], 5, True), fmt.format(self.transactions[i]['id_vehicle'], 9, True),0,0,0)
                self.pList.append(temp)

            elif self.csvOutput:
                if(int(i) != 0):
                    temp = pt.ptLine(self.siteid,self.transactions[i]['seqnum'],self.transactions[i]['totAmt'],self.transactions[i]['pCode'],self.transactions[i]['price'],self.transactions[i]['quantity'],self.transactions[i]['odometer'],
                                self.transactions[i]['pump'],self.transactions[i]['tranNum'],self.transactions[i]['tranDate'],self.transactions[i]['tranTime'],self.transactions[i]['vehicle'],
                                self.transactions[i]['id_card'],self.transactions[i]['id_acct'],self.transactions[i]['id_vehicle'],self.transactions[i]['authNum'], self.transactions[i]['pName'], self.transactions[i]['id_card_type']) 
                    self.pList.append(temp)

            elif self.merchantAg:
                temp = pt.ptLine(fmt.mAgPadding(8,self.siteid, True, "0"), 0, fmt.mAgPadding(9,self.transactions[i]['totAmt'], True, "0"),
                                 fmt.mAgPadding(20, fmt.mAgPadding(3,self.transactions[i]['pCode'], True, "0"), False, " "), fmt.mAgPadding(9, self.transactions[i]['price'], True, "0"),
                                 fmt.mAgPadding(9, fmt.mAgDecimalLength(self.transactions[i]['quantity'],3), True, "0"), fmt.mAgPadding(9, self.transactions[i]['odometer'], True, "0"),
                                 fmt.mAgPadding(2, self.transactions[i]['pump'], True, "0"), fmt.mAgPadding(9, self.transactions[i]['tranNum'], True, "0"),
                                 fmt.mAgDateTimeFormat(self.transactions[i]['tranDate']),fmt.mAgDateTimeFormat(self.transactions[i]['tranTime']),
                                 fmt.mAgPadding(9, self.transactions[i]['vehicle'], True, "0"), fmt.mAgPadding(9, self.transactions[i]['id_card'], True, "0"),
                                 fmt.mAgPadding(9, self.transactions[i]['id_acct'], True, " "), fmt.mAgPadding(9, self.transactions[i]['id_vehicle'], True, "0"), 0,
                                 fmt.mAgPadding(26, self.transactions[i]['pName'], False, " "), fmt.mAgCardName(self.transactions[i]['id_card_type']))
                self.pList.append(temp)

        self.pList = sorted(self.pList,key=lambda ptOBJ: ptOBJ.tranDate + ptOBJ.tranTime)
        return self
            
