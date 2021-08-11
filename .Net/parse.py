import csv
import re
import transaction
import os


class parse:
    def __init__(self) -> None:
        self.rowcount = 0
        self.tranList = []
        self.tranDict = {}




    def parse(self, folder, filePath):
        os.chdir(folder)
        
        with open(filePath, newline='', errors="ignore") as table:
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
                if(row[3] == "Other"):
                    self.tranDict[row[4]] = transaction.transaction()
                    self.tranDict[row[4]].otherDictSet(tempDict)
                    self.tranDict[row[4]].parentIDSet(row[4])
                if(row[3] == "Tender"):
                    self.tranDict[row[0]].tenderDictSet(tempDict)
                    self.tranDict[row[0]].processorSet(row[6])
                if(row[3] == "Product"):
                    self.tranDict[row[0]].productDictSet(tempDict)
                    self.tranDict[row[0]].pNameSet(row[5])
                    self.tranDict[row[0]].pDescSet(row[6])
                    self.tranDict[row[0]].unitPriceSet(row[8])
                    self.tranDict[row[0]].volumeSet(row[9])
                    self.tranDict[row[0]].uOMSet(row[10])
                    self.tranDict[row[0]].totalAmtSet(row[11])
                    self.tranDict[row[0]].rawTranTimeSet(row[2])
                self.rowcount += 1
        return self.tranDict

