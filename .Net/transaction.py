import format
import re

class transaction:

    def __init__(self):
        self.parentID = "00000"
        self.otherDict = {}
        self.tenderDict = {}
        self.productDict = {}
        self.processor = "UNKNOWN"

        self.unitPrice = "0.000"
        self.volume = "000.000"
        self.totalAmt = "000.00"
        self.UOM = "N/A"
        self.pName = "N/A"
        self.pDesc = "N/A"

        self.rawTranTime = "00000000000000000"


    def parentIDSet(self, pID):
        self.parentID = pID
    def otherDictSet(self, dict):
        self.otherDict = dict
    def tenderDictSet(self, dict):
        self.tenderDict = dict
    def productDictSet(self, dict):
        self.productDict = dict

    def unitPriceSet(self, uP):
        self.unitPrice = uP
    def volumeSet(self, v):
        self.volume = v
    def totalAmtSet(self, tAmt):
        self.totalAmt = tAmt
    def uOMSet(self, uOm):
        self.UOM = uOm
    def pNameSet(self, pN):
        self.pName = pN
    def pDescSet(self, pD):
        self.pDesc = pD
    def processorSet(self, p):
        self.processor = p
    def rawTranTimeSet(self, t):
        self.rawTranTime = t

    def parentIDGet(self):
        return self.parentID
    def getOtherDict(self):
        return self.otherDict
    def getTenderDict(self):
        return self.tenderDict
    def getProductDict(self):
        return self.productDict


    def VDPPrint(self):
        if(self.tenderDict['actionState'] == "Unapproved"):
            pID = "00"
            siteID = "000090"
            tranNum = format.padAdd("left", "0", 6, self.parentID)
            idTran = "0000"
            totPrice = "00000000"
            uPrice = "0000"
            quantity = "00000000"
            pumpid = "00"
            date = self.rawTranTime[0:8]
            time = self.rawTranTime[8:12]
            if(self.processor == "Credit"):
                cardNumber = format.padAdd("right", "0", 30, format.padAdd("left", "0", 23, "0000"))
            else:
                cardNumber = format.padAdd("right", "0", 30, format.padAdd("left", "0", 23, self.tenderDict['cardNumber']))
        else:
            pID = self.productDict['productid']
            if pID == "44":
                pID = "50"
            elif pID == "03":
                pID = "45"
            siteID = "000090"
            tranNum = format.padAdd("left", "0", 6, self.parentID)
            idTran = format.padAdd("left", "0", 4, self.otherDict['hostTransaction'])
            totPrice = format.padAdd("left", "0", 8, format.decimalFormat(2,self.totalAmt))
            uPrice = format.padAdd("left", "0", 4, format.decimalFormat(3,self.unitPrice))
            quantity = format.padAdd("left", "0", 8, format.decimalFormat(3, self.volume))
            if 'pumpid' not in self.productDict:
                pumpid = "00"
            else:
                pumpid = format.padAdd("left", "0", 2, self.productDict['pumpid'])
            date = self.rawTranTime[0:8]
            time = self.rawTranTime[8:12]
            if(self.processor == "Credit"):
                cardNumber = format.padAdd("right", "0", 30, format.padAdd("left", "0", 23, "0000"))
            else:
                cardNumber = format.padAdd("right", "0", 30, format.padAdd("left", "0", 23, self.tenderDict['cardNumber']))

        return ("0" + siteID + tranNum +idTran + "0" + totPrice + "00" + pID + uPrice + quantity + "0000000000000000" +
                pumpid + date + time + "41" + "00000000000000000000000011" + cardNumber + "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\n")
    
    def AGTRAXPrint(self):
        if 'id_accountNumber' not in self.tenderDict:
            if 'lastFour' not in self.tenderDict:
                self.tenderDict['id_accountNumber'] = ""
            else:
                self.tenderDict['id_accountNumber'] = self.tenderDict['lastFour']
        if 'cardNumber' not in self.tenderDict:
            if 'ID_CARD_NR' not in self.tenderDict:
                self.tenderDict['cardNumber'] = ""
            else:
                self.tenderDict['cardNumber'] = self.tenderDict['ID_CARD_NR']

        if(self.productDict['productid'] == "01"):
            self.productDict['productid'] = "703"
        elif(self.productDict['productid'] == "21"):
            self.productDict['productid'] = "702"
        elif(self.productDict['productid'] == "44"):
            self.productDict['productid'] = "705"

        orderBranch = str(format.padAdd("left", "0", 3, self.tenderDict['siteid']))
        invoiceNumber = str(format.padAdd("left", "0", 6, self.parentID))
        invoiceDate = str(self.rawTranTime[0:8])
        customerNumber = str(format.padAdd("left", " ", 7, re.sub(r'^0*','',format.cutLength("right", 7, self.tenderDict['id_accountNumber']))))
        tAmt = str(format.padAdd("left", "0", 10, format.decimalFormat(2, self.totalAmt)))
        cardNumber = str(format.padAdd('right', " ", 16, (format.cutLength("right", 4, self.tenderDict['cardNumber']).strip("X"))))
        iProductNumber = str(format.padAdd("right", " ", 16, self.productDict['productid']))
        iQuantity = str(format.padAdd("left", "0", 10, format.decimalFormat(3, self.volume)))
        iPrice = str(format.padAdd("left", "0", 10, format.decimalFormat(4, self.unitPrice)))
        commentCard = cardNumber.strip()
        commentCard = commentCard[len(commentCard)-4:len(commentCard)]
        comment = str(format.padAdd("right", " ", 25, (self.processor + " " + commentCard)))
        tranCode = ""


        if self.processor == "NBS":
            tranCode = "05"
            customerNumber = "   CASH"
        else:
            tranCode = "02"

        return ("00" + "004" + invoiceNumber + invoiceDate + customerNumber + tranCode + tAmt + "+" + "00000000+00000000+0000000000+0000000000+                       " + cardNumber + "000000000000000000+\n" +
                "01" + "004" + iProductNumber + iQuantity + "+" + iPrice + tAmt + "+" + "0000000000000000+0000000000+0000000000+                         \n" +
                "02" + comment + "\n")
