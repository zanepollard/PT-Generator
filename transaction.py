import re
import format

class transaction:

    def __init__(self):
        self.siteID = "0"
        self.seqNum = "0"
        self.tranNum = "0"
        self.totalAmount = "0.00"
        self.pCode = "0"
        self.quantity = "0.000"
        self.price = "0.00"
        self.odometer = "0"
        self.pump = "00"
        self.tranTime = "1200"
        self.tranDate = "20000101"
        self.authNum = "0"
        self.pName = "NONE"
        self.pDesc = "NONE"
        self.cardType = "UNK"
        self.vehicle = "0"
        self.vehicleID = "0"
        self.card = "0"
        self.account = "0"
        self.rawTranTime = "00000000000000000"

        self.otherDict = {}
        self.tenderDict = {}
        self.productDict = {}
    
    def set_siteID(self,sID):
        self.siteID = sID
    def set_seqNum(self, sNum):
        self.seqNum = sNum
    def set_tranNum(self, tNum):
        self.tranNum = tNum
    def set_totalAmount(self, tA):
        self.totalAmount = tA
    def set_pCode(self,pC):
        self.pCode = pC
    def set_quantity(self, q):
        self.quantity = q
    def set_price(self, p):
        self.price = p
    def set_odometer(self, o):
        self.odometer = o
    def set_pump(self, p):
        self.pump = p
    def set_tranTime(self, tT):
        self.tranTime = tT
    def set_tranDate(self, tD):
        self.tranDate = tD
    def set_authNum(self, aN):
        self.authNum = aN
    def set_pName(self, pN):
        self.pName = pN
    def set_pDesc(self, pD):
        self.pDesc = pD
    def set_cardType(self,cT):
        self.cardType = cT
    def set_vehicle(self, v):
        self.vehicle = v
    def set_vehicleID(self, vID):
        self.vehicleID = vID
    def set_card(self, c):
        self.card = c
    def set_account(self, a):
        self.account = a
    def set_rawTranTime(self, rTT):
        self.rawTranTime = rTT
    def set_otherDict(self, oD):
        self.otherDict = oD
    def set_tenderDict(self, tD):
        self.tenderDict = tD
    def set_productDict(self, pD):
        self.productDict = pD


    def VDPPrint(self, config_data):
        if(config_data.get('site_number') == ""):
            self.set_siteID(format.padAdd("left", "0", 6, self.siteID))
        else:
            self.set_siteID(format.padAdd("left", "0", 6, config_data.get('site_number')))
        self.set_tranNum(format.padAdd("left", "0", 6, self.tranNum))
        if(self.cardType == "Credit"):
            self.set_card(format.padAdd("right", "0", 30, format.padAdd("left", "0", 23, "0000")))
        else:
            self.set_card(format.padAdd("right", "0", 30, format.padAdd("left", "0", 23, self.card)))
        

        if(self.tenderDict['actionState'] == "Unapproved"):
            self.set_pCode("00")
            self.set_seqNum("0000")
            self.set_totalAmount("00000000")
            self.set_price("0000")
            self.set_quantity("00000000")
            self.set_pump("00")
        else:
            if self.pCode == "44":
                self.set_pCode("50")
            elif self.pCode == "03":
                self.set_pCode("45")
            self.set_seqNum(format.padAdd("left", "0", 4, self.seqNum))
            self.set_totalAmount(format.padAdd("left", "0", 8, format.decimalFormat(2,self.totalAmount)))
            self.set_price(format.padAdd("left", "0", 4, format.decimalFormat(3,self.price)))
            self.set_quantity(format.padAdd("left", "0", 8, format.decimalFormat(3, self.quantity)))
            self.set_pump(format.padAdd("left", "0", 2, self.pump))
        return ("0" + self.siteID + self.tranNum + self.seqNum + "0" + 
                self.totalAmount + "00" + self.pCode + self.price + self.quantity + 
                "0000000000000000" + self.pump + self.tranDate + self.tranTime + 
                "41" + "00000000000000000000000011" + self.card + 
                "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\n")
    
    def AGTRAXPrint(self, config_data):
        if(self.pCode == "01"):
            self.set_pCode("703")
        elif(self.pCode == "21"):
            self.set_pCode("702")
        elif(self.pCode == "44"):
            self.set_pCode("705")
        if config_data.get('site_number') == "":
            self.set_siteID(str(format.padAdd("left", "0", 3, self.siteID)))
        else:
            self.set_siteID(str(format.padAdd("left", "0", 3, config_data.get('site_number'))))
        self.set_account(str(format.padAdd("left", " ", 7, re.sub(r'^0*','',format.cutLength("right", 7, self.account)))))
        self.set_totalAmount(str(format.padAdd("left", "0", 10, format.decimalFormat(2, self.totalAmount))))
        self.set_card(str(format.padAdd('right', " ", 16, (format.cutLength("right", 4, self.card).strip("X")))))
        self.set_pCode(str(format.padAdd("right", " ", 16, self.pCode)))
        self.set_quantity(str(format.padAdd("left", "0", 10, format.decimalFormat(3, self.quantity))))
        self.set_price(str(format.padAdd("left", "0", 10, format.decimalFormat(4, self.price))))
        self.set_tranNum(str(format.padAdd("left", "0", 6, str(self.tranNum))))

        commentCard = self.card.strip()
        commentCard = commentCard[len(commentCard)-4:len(commentCard)]
        comment = str(format.padAdd("right", " ", 25, (self.cardType + " " + commentCard)))
        tranCode = ""

        if self.cardType == "NBS":
            tranCode = "05"
            self.set_account("   CASH")
        else:
            tranCode = "02"

        return ("00" + self.siteID + self.tranNum + self.tranDate + self.account + tranCode + self.totalAmount + "+" + "00000000+00000000+0000000000+0000000000+                       " + self.card + "000000000000000000+\n" +
                "01" + "004" + self.pCode + self.quantity + "+" + self.price + self.totalAmount + "+" + "0000000000000000+0000000000+0000000000+                         \n" +
                "02" + comment + "\n")
    
    def JCDoylePrint(self, config_data):
        self.set_pump(format.padAdd("left", "0", 2, self.pump))
        
        self.set_tranNum(str(format.padAdd("left", "0", 6, self.tranNum)))
        self.set_tranDate(" " + str(self.rawTranTime[4:6]) + "/" + str(self.rawTranTime[6:8]) + "/" + str(self.rawTranTime[0:4]))
        self.set_tranTime(" " + str(self.rawTranTime[8:10]) + ":" + str(self.rawTranTime[10:12]))
        self.set_account(" " + str(format.padAdd("right", " ", 8, re.sub(r'^0*X+','',format.cutLength("right", 7, self.account)))))
        self.set_totalAmount(" " + str(format.padAdd("left"," ",7,format.decimalPad(2,self.totalAmount))))
        self.set_card(" " + str(format.padAdd("left", " ", 8, self.card)))
        self.set_pCode(" " + str(format.padAdd("left", " ", 2, re.sub(r'product\.id = ','',str(self.pCode)))))
        self.set_quantity(" " + str(format.padAdd("left", " ", 7, str(format.decimalPad(3,self.quantity)))))
        self.set_price(" " + str(format.padAdd("left", " ", 6, str(format.decimalPad(3,self.price)))))
        tranCode = ""

        return self.tranNum + "  0 "  + self.account + self.card + self.tranDate + self.tranTime + self.pCode + self.quantity + self.price + self.totalAmount + "\n"

    def ptPrint(self, config_data):
        STATCODE = "00"
        ACT = "00"
        TRANTYPE = "00"
        OID = "0"
        FILL = "00000000"
        PART_ID = "000"
        END = ("00000000000000000000000000000"
                "00000000000000000000000000000"
                "00000000000000000000000000000"
                "00000000000000000000000000000"
                "000000000000DCF00000000000000"
                "0000000000")

        self.set_tranNum(format.padAdd("left","0",4,format.cutLength("right",4, str(self.tranNum))))
        self.set_siteID(str(re.sub(r'[a-z_\s-]','', str(self.siteID), flags=re.IGNORECASE)))
        for __ in range((6-len(self.siteID))):
            self.set_siteID('0' + self.siteID)
        self.set_seqNum(format.padAdd("left","0",4, format.cutLength("right",4,str(self.seqNum))))
        self.set_totalAmount(format.padAdd("left","0",6,format.decimalFormat(2,str(self.totalAmount))))
        self.set_price(format.padAdd("left","0",8,format.decimalFormat(7,str(self.price))))
        self.set_quantity(format.padAdd("left","0",8,format.decimalFormat(3,str(self.quantity))))
        self.set_odometer(format.padAdd("left","0",7,str(format.cutLength("right",8,str(self.odometer)))))
        self.set_pump(format.padAdd("left","0",2,format.cutLength("right",2,str(self.pump))))
        self.set_tranDate(self.tranDate[2:8])
        self.set_vehicle(format.padAdd("left","0",8,format.cutLength("right",8,str(self.vehicle))))
        self.set_card(format.padAdd("left","0",7,format.cutLength("right",7,str(self.card))))
        self.set_account(format.padAdd("left","0",6,format.cutLength("right",6,str(self.account))))
        self.set_vehicleID(format.padAdd("left","0",4,format.cutLength("right",4,str(self.vehicle))))
       
        return (self.siteID + self.seqNum + STATCODE + self.totalAmount + ACT + TRANTYPE + self.pCode + self.price + 
                self.quantity + self.odometer  + OID + self.pump + self.tranNum + self.tranDate + self.tranTime + 
                FILL + self.vehicle + self.card + PART_ID + self.account + self.vehicleID + END + "\n")
    
    def gasboyPrint(self, config_data):
        self.set_tranNum(format.padAdd("left", " ", 4, format.cutLength("right", 4, self.tranNum)))
        if(config_data['site_number'] == ""):
            self.set_siteID(re.sub(r'[a-z_\s-]','', self.siteID, flags=re.IGNORECASE))
            if(len(self.siteID) > 2):
                self.set_siteID(self.siteID[len(self.siteID)-2: len(self.siteID)])
            self.set_siteID(self.siteID + " ")
        else:
            self.set_siteID(format.padAdd("left", " ", 2, format.cutLength("right",2,str(config_data['site_number']))) + " ")
        self.set_tranNum(format.padAdd("left"," ",4,format.cutLength("right",4,self.tranNum)) + " ")
        self.set_card(format.padAdd("left"," ",6,format.cutLength("right",6,self.card)) + " ")
        self.set_account(format.padAdd("left"," ",5,format.cutLength("right",6,self.account)) + " ")
        self.set_vehicle(format.padAdd("left"," ",9,format.cutLength("right",9,self.vehicle)) + " ")
        self.set_tranDate(format.padAdd("left"," ",8,(self.tranDate[4:6][0].strip("0") + self.tranDate[4:6][1] + "/" + 
                                                      self.tranDate[6:8] + "/" +
                                                      self.tranDate[2:4])) + " ")
        self.set_tranTime(format.padAdd("left"," ",5,(self.tranTime[0:2][0].strip("0") + self.tranTime[0:2][1] + ":" +
                                                      self.tranTime[2:4])) + " ")
        self.set_pump(format.padAdd("left","0",2,self.pump) + " ")
        self.set_pCode(format.padAdd("left","0",2,self.pCode) + " ")
        self.set_quantity(format.padAdd("left"," ",9,format.decimalPad(3,self.quantity)) + " ")
        self.set_price(format.padAdd("left"," ",5,format.decimalPad(3,self.price)) + " ")
        self.set_totalAmount(format.padAdd("left"," ",9,format.decimalPad(2,self.totalAmount)) + " ")
        self.set_odometer(format.padAdd("left"," ",6,format.cutLength("right",6,self.odometer)) + " ")

        if(config_data['Dawson'] == True):
            carwash =""
            if self.card[len(self.card)-4:len(self.card)] == self.account[len(self.card)-4:len(self.card)]:
                driver = "000000 "
            else:
                driver = self.card
            for x in ("07 ","08 ","09 "):
                if self.pCode == x:
                    carwash = "CARWASH "
            return(self.siteID + self.tranNum + driver + self.account + "000 " + self.vehicle + self.tranDate +self.tranTime + self.pump + self.pCode + 
                   self.quantity + self.price + self.totalAmount + self.odometer + carwash + "\n")
        else:
            return(self.siteID + self.tranNum + self.card + self.account + "000 " + self.vehicle + self.tranDate +self.tranTime + self.pump + self.pCode + 
                   self.quantity + self.price + self.totalAmount + self.odometer + "\n")

    def csvPrint(self, config_data):
        tranDateTime = self.tranDate[4:6] + "-" + self.tranDate[6:8] + "-" + self.tranDate[0:4] + " " + self.tranTime[0:2] + ":" + self.tranTime[2:4]
        return [tranDateTime, self.siteID, self.tranNum, self.seqNum, self.authNum, self.account, self.pName, self.pCode, self.pump, self.quantity, 
                self.price, self.totalAmount, self.tranDate, self.tranTime, self.cardType]
            

    def CFNcsvPrint(self, config_data):
        if(len(self.pName) > 20):
            self.set_pName(self.pName[0:20])
        if(len(str(self.seqNum))>4):
            self.set_seqNum(self.seqNum[len(self.seqNum)-4:len(self.seqNum)])
        if(len(str(self.odometer))>7):
            self.set_odometer(self.odometer[len(self.odometer)-7:len(self.odometer)])
        if(len(str(self.tranNum))>4):
            self.set_tranNum(self.tranNum[len(self.tranNum)-4:len(self.tranNum)])

        if(config_data['Downs']):
            self.set_card("000" + self.card[len(self.card)-4:len(self.card)])
            p19 = self.card + "000" + "000000" + "0000"
            if(len(self.siteID.split(' - ')) == 2):
                self.set_siteID(re.sub(r'[a-z_\s-]','', self.siteID.split(' - ')[1], flags=re.IGNORECASE))
            else:
                self.set_siteID(re.sub(r'[a-z_\s-]','', self.siteID, flags=re.IGNORECASE))
            tranType = "N"  
        elif(config_data['Atlas']):
            self.set_cardType("PV")
            self.set_siteID(config_data.get('site_number'))
            self.set_card(format.padAdd("left","0",6, self.siteID) + self.card[6:len(self.card)])
            p19 = self.card + "196" + "001454" + "0000"
            #p19 = "5550123" + "321" + "001234" + "0000"         
            tranType = "P"

        return [self.siteID, self.seqNum, "0", self.totalAmount, "0", self.pCode, "FUEL", self.pName,self.price,self.quantity,self.odometer,self.pump,self.tranNum,self.tranDate[2:8],self.tranTime,
                    0,9,'',p19,'','','','','','','','','','','','','','','','','','','','','','',tranType,self.cardType,0,self.price,0,0,'','','','','','','','','']

    def merchantAgPrint(self, config_data):
        catCode = "                    "
        cusCode = "                    "
        blank1 = "                                                     "
        blank2 = "                                                    "
        
        if(config_data['site_number'] == ""):
            self.set_siteID(re.sub(r'[a-z_\s-]','', self.siteID, flags=re.IGNORECASE))
        else:
            self.set_siteID(config_data['site_number'])
        
        self.set_siteID(format.padAdd("left","0",8,self.siteID))
        self.set_totalAmount(format.padAdd("left","0",9,re.sub(r'[.]','', format.decimalPad(3,self.totalAmount), flags=re.IGNORECASE)))
        self.set_pCode(format.padAdd("right"," ",20,format.padAdd("left","0",3,self.pCode)))
        self.set_quantity(format.padAdd("left","0",9,re.sub(r'[.]','', format.decimalPad(3,self.quantity), flags=re.IGNORECASE)))
        self.set_price(format.padAdd("left","0",9,re.sub(r'[.]','', format.decimalPad(3,self.price), flags=re.IGNORECASE)))
        self.set_pump(format.padAdd("left","0",2,self.pump))
        self.set_tranNum(format.padAdd("left","0",9,self.tranNum))
        self.set_tranDate(self.tranDate[6:8] + self.tranDate[4:6] + self.tranDate[0:4])
        self.set_vehicle(format.padAdd("left","0",9,self.vehicle))
        self.set_card(format.padAdd("left","0",9,self.card))
        self.set_account(format.padAdd("left"," ",9,self.account))
        self.set_vehicleID(format.padAdd("left","0",9,self.vehicleID))
        self.set_pName(format.padAdd("right"," ",26,self.pName))
        self.set_cardType(format.mAgCardName(self.cardType))

        driver = self.card
        if self.account == self.card:
                driver = "000000000"
        return (self.tranNum + self.tranDate + self.tranTime + self.account + self.pCode + catCode + self.pName +
                self.quantity + self.odometer + self.vehicle + self.price + self.totalAmount + self.totalAmount + cusCode +
                self.siteID + self.pump + driver + blank1 + self.cardType + self.account + self.totalAmount + blank2 + "\n")\
    
    def FuelMasterPrint(self, config_data):
        if(config_data['site_number'] == ""):
            self.set_siteID(re.sub(r'[a-z_\s-]','', self.siteID, flags=re.IGNORECASE))
        else:
            self.set_siteID(config_data['site_number'])
        self.set_siteID(format.padAdd("left","0",4,format.cutLength("right",4,self.siteID)))
        self.set_tranDate(self.tranDate[4:6] + self.tranDate[6:8] + self.tranDate[2:4])
        self.set_account(format.padAdd("left","0",5,format.cutLength("right",5,self.account)))
        self.set_card(format.padAdd("left","0",4,format.cutLength("right",4,self.card)))
        self.set_odometer(format.padAdd("left"," ",6,format.cutLength("right",6,self.odometer)))
        if len(self.pCode) == 2:
            self.set_pCode(re.sub(r'0','',self.pCode[0]) + self.pCode[1])
        self.set_pCode(format.padAdd("left"," ",2,self.pCode))
        self.set_pump(format.padAdd("left"," ",2,self.pump))
        self.set_quantity(format.padAdd("left","0",9,format.decimalPad(2, self.quantity)))
        self.set_price(format.padAdd("left","0",7,format.decimalPad(4,self.price)))
        self.set_totalAmount(format.padAdd("left","0",11,format.decimalPad(2,self.totalAmount)))

        return ("00" + self.siteID + self.tranDate + self.tranTime + "0000" + self.account + "0000" +
               self.card + self.odometer + "     " + self.pCode + self.pump + self.quantity + self.price + 
               self.totalAmount + "\n")

    def HuntBreshersPrint(self, config_data):
        if(config_data['site_number'] == ""):
            self.set_siteID(re.sub(r'[a-z_\s-]','', self.siteID, flags=re.IGNORECASE))
        else:
            self.set_siteID(config_data['site_number'])
        #self.set_siteID()


