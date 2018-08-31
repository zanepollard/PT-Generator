class ptLine:

    #Initializes a line object
    def __init__(self,siteid,seqnum,totAmt,
                pCode, price,quantity,odometer,pump,
                tranNum,tranDate,tranTime,vehicle,
                id_card,id_acct,id_vehicle):
        self.siteid = siteid
        self.seqnum = seqnum
        self.STATCODE = "00"
        self.totAmt = totAmt
        self.ACT = "00"
        self.TRANTYPE = "00"
        self.pCode = pCode
        self.price = price
        self.quantity = quantity
        self.odometer = odometer
        self.OID = "0"
        self.pump = pump
        self.tranNum = tranNum
        self.tranDate = tranDate
        self.tranTime = tranTime
        self.FILL = "00000000"
        self.id_vehicle = id_vehicle
        self.id_card = id_card
        self.PART_ID = "000"
        self.id_acct = id_acct
        self.vehicle = vehicle
        self.END = ("00000000000000000000000000000"
                    "00000000000000000000000000000"
                    "00000000000000000000000000000"
                    "00000000000000000000000000000"
                    "000000000000DCF00000000000000"
                    "0000000000")
    
        
    
