import csv
import re
import transaction
import os


class parse:
    def __init__(self) -> None:
        self.tranDate = ""
        self.transactions = {}


    def parse(self,file):
        print(f"Parsing {file}")
        oD = {}
        tD = {}
        pD = {}
        with open(file, newline='', errors="ignore") as table:
            reader = csv.reader(table, quotechar="\"")
            next(reader)
            for row in reader:
                tempDict = {}
                for entry in re.split(r'\',\'',row[15]):
                    entry = re.sub(r'\'', '', entry).split(":")
                    if(len(entry) == 2):
                        tempDict[entry[0]] = entry[1]
                    else:
                        tempDict[entry[0]] = ''
                match row[3]:
                    case "Other":
                        self.transactions[row[4]] = transaction.transaction()
                        self.transactions[row[4]].set_otherDict(tempDict)
                        oD = tempDict
                        self.transactions[row[4]].set_tranNum(row[4])
                        try:
                            self.transactions[row[4]].set_seqNum(oD['hostTransaction'])
                        except Exception:
                            #print(f"Could not find 'hostTransaction' variable for transaction number {row[4]}. Defaulting to 0.\n")
                            self.transactions[row[4]].set_seqNum("0")
                    case "Tender":
                        self.transactions[row[0]].set_tenderDict(tempDict)
                        tD = tempDict
                        try:
                            self.transactions[row[0]].set_cardType(row[6])
                        except Exception:
                            print(f"Could not find 'cardType' variable for transaction number {row[0]}\n")
                        try:
                            if 'cardNumber' not in tD:
                                if 'ID_CARD_NR' not in tD:
                                    tD['cardNumber'] = ""
                                else:
                                    tD['cardNumber'] = tD['ID_CARD_NR']
                            self.transactions[row[0]].set_card(tD['cardNumber'])
                        except Exception:
                            print(f"Could not find 'cardNumber' variable for transaction number {row[0]}\n") 
                        try:
                            if 'id_accountNumber' not in tD:
                                if 'lastFour' not in tD:
                                    tD['id_accountNumber'] = ""
                                else:
                                    tD['id_accountNumber'] = tD['lastFour']
                            self.transactions[row[0]].set_account(tD['id_accountNumber'])
                        except Exception:
                            print(f"Could not find 'id_accountNumber' variable for transaction number {row[0]}\n")
                        try:
                            self.transactions[row[0]].set_siteID(tD['siteid'])
                        except Exception:
                            print(f"Could not find 'siteid' variable for transaction number {row[0]}\n")
                    case "Product":
                        self.transactions[row[0]].set_productDict(tempDict)
                        pD = tempDict
                        self.transactions[row[0]].set_pName(row[5])
                        self.transactions[row[0]].set_pDesc(row[6])
                        self.transactions[row[0]].set_price(row[8])
                        self.transactions[row[0]].set_quantity(row[9])
                        self.transactions[row[0]].set_totalAmount(row[11])
                        self.transactions[row[0]].set_tranTime(row[2][8:12])
                        self.transactions[row[0]].set_tranDate(row[2][0:8])
                        self.tranDate = row[2][0:8]
                        self.transactions[row[0]].set_rawTranTime(row[2])
                        try:
                            if 'productid' not in pD:
                                pD['productid'] = "00"
                            self.transactions[row[0]].set_pCode(pD['productid'])
                        except Exception:
                                print(f"Could not find 'productid' variable for transaction number {row[0]}\n")
                        try:
                            if 'pumpid' not in pD:
                                pD['pumpid'] = "00"
                            self.transactions[row[0]].set_pump(pD['pumpid'])
                        except Exception:
                                print(f"Could not find 'pumpid' variable for transaction number {row[0]}\n")
        return self

