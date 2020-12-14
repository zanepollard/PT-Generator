class ptLine:

    #Initializes a line object
    def __init__(self,siteid,seqnum,totAmt,
                pCode, price,quantity,odometer,pump,
                tranNum,tranDate,tranTime,vehicle,
                id_card,id_acct,id_vehicle, authNum, 
                pName,cardType):
        self.siteid = siteid
        self.seqnum = seqnum
        self.totAmt = totAmt
        self.pCode = pCode
        self.price = price
        self.quantity = quantity
        self.odometer = odometer
        self.pump = pump
        self.tranNum = tranNum
        self.tranDate = tranDate
        self.tranTime = tranTime
        self.id_vehicle = id_vehicle
        self.id_card = id_card
        self.id_acct = id_acct
        self.vehicle = vehicle
        self.pName = pName
        self.authNum = authNum
        self.cardType = cardType

    def ptPrint(self):
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
        return (self.siteid + self.seqnum + STATCODE + self.totAmt + ACT + TRANTYPE + self.pCode + self.price + 
                self.quantity + self.odometer + OID + self.pump + self.tranNum + self.tranDate + self.tranTime + 
                FILL + self.vehicle + self.id_card + PART_ID + self.id_acct + self.id_vehicle + END + "\n")
    
    def gasboyPrint(self):
        carwash =""
        if self.id_card[len(self.id_card)-4:len(self.id_card)] == self.id_acct[len(self.id_card)-4:len(self.id_card)]:
                driver = "000000 "
        else:
                driver = self.id_card
        for x in ("07 ","08 ","09 "):
                if self.pCode == x:
                        carwash = "CARWASH "
        return(self.siteid + self.seqnum + driver + 
                self.id_acct + "000 " + self.vehicle + self.tranDate +
                self.tranTime + self.pump + self.pCode + " " +
                self.quantity + self.price + self.totAmt +
                self.odometer + carwash+"\n")

    def csvPrint(self):
        tranDateTime = self.tranDate + " " + self.tranTime
        return [tranDateTime, self.siteid, self.tranNum, self.seqnum, self.authNum, self.id_acct,
                self.pName, self.pCode, self.pump, self.quantity, self.price, self.totAmt,
                self.tranDate, self.tranTime, self.cardType]

    def merchantAgPrint(self):
        catCode = "                    "
        cusCode = "                    "
        blank1 = "                                                     "
        blank2 = "                                                    "
        driver = self.id_card
        if self.id_acct == self.id_card:
                driver = "000000000"
        return (self.tranNum + self.tranDate + self.tranTime + self.id_acct + self.pCode + catCode + self.pName +
                self.quantity + self.odometer + self.vehicle + self.price + self.totAmt + self.totAmt + cusCode +
                self.siteid + self.pump + driver + blank1 + self.cardType + self.id_acct + self.totAmt + blank2 + "\n")

        
    
