import csv
import re
import fnmatch
import os
import datetime
import shutil
import win32com.client
from win32com.client import Dispatch, constants

siteid = ""
seqnum = []
STATCODE = "00"
totAmt = [] 
ACT = "00"
TRANTYPE ="00"
pCode = [] 
price = "10000000"
quantity = []
odometer = []
OID = "0"
pump = [] 
tranNum = []
tranDate = []
tranTime = []
fill = "00000000"
id_vehicle = []
id_card = []
part_id ="000"
id_acct = []
vehicle = []
end = "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000DCF000000000000000000000000"
fileDate = ""
runCount = 0
nDV = ""

#Formats date in the proper PT file format
def tFormat(time):
    return (time[0:2]+time[3:5])

def dFormat(date):
    fDate = date[8:10] + date[0:2] + date[3:5]
    return fDate

def nextDay(d):
    date = datetime.date(int(d[6:10]),int(d[0:2]),int(d[3:5]))
    date += datetime.timedelta(days=1)
    day = ""
    month = ""
    if len(str(date.day)) < 2:
        day = "0" + str(date.day)
    else:
        day = str(date.day)
    if len(str(date.month)) < 2:
        month = "0" + str(date.month)
    else:
        month = str(date.month)
    return (str(date.year)[2:4] + month + day)

def decimalSplit(number, x, y): #y is decimal true/false
    if x: #quantity value check
        if y: #check if it has a decimal or not
            temp = number.split('.')
            for __ in range(5-len(temp[0])):
                temp[0]= "0"+temp[0]
            for __ in range(3-len(temp[1])):
                temp[1]= temp[1]+"0"
            quantity.append(temp[0]+temp[1])
        else:
            temp = number
            for __ in range(5-len(temp)):
                temp = "0"+temp
            quantity.append(temp + "000")
    else:
        if y:
            temp = number.split('.')
            for __ in range(4-len(temp[0])):
                temp[0]= "0"+temp[0]
            if len(temp[1])>2:
                temp[1]= temp[1][0:2]
                for __ in range(2-len(temp[1])):
                    temp[1]= temp[1]+"0"
            else:
                for __ in range(2-len(temp[1])):
                    temp[1]= temp[1]+"0"
            totAmt.append(temp[0]+temp[1])
        else:
            temp = number
            for __ in range(4-len(number)):
                temp = "0"+temp
            totAmt.append(temp+"00")

def decimalCheck(number, x):
    decimalfind = re.compile(r"\d+\.\d+")
    if decimalfind.match(number):
        decimalSplit(number, x, True)
    else:
        decimalSplit(number, x, False)

#Ensures the value that was put into it has the proper amount of zeros
def format(oD, num):
    temp = oD
    for __ in range(num-len(oD)):
        temp = "0"+temp
    return temp

#pulls today's date in the format requred of the naming covention
def cday():
    now = datetime.datetime.now()
    day=""
    month=""
    if len(str(now.month))<2:
        month = "0" + str(now.month)
    else:
        month = str(now.month)
    if len(str(now.day))<2:
        day = "0" + str(now.month)
    else:
        day = str(now.day)
    return month + day + str(now.year)[2:4]

def hParse():
    global runCount
    global siteid
    global tranDate
    global nDV
    firstRun = True
    raw_id = ""
    rowdata = []
    filename = None
    #Pulls filename from directory where the script lives
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,'}h*.d1c'):
            filename = file
    if filename == None:
        print("No '}h*.d1c' file found! ")
        os.system('pause')
        exit()
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, quotechar="\"")
        for row in reader:
            rowdata = row
            tranNum.append(rowdata[3][1:8])
            if firstRun: #Pulls all the single use variables into memory from the csv
                raw_id = rowdata[0]
                raw_id = re.sub(r'[a-z_\s-]','', raw_id, flags=re.IGNORECASE)
                firstRun = False
                nDV = rowdata[1]
                tranDate = dFormat(rowdata[1])
                siteid = raw_id
                for __ in range((6-len(raw_id))):
                    siteid = '0' + siteid
            dParse()
            vParse()                         
            runCount+=1
    fileIO()
    #email(raw_id, "1","2")

#parses variables from the data file
def dParse():
    DFile = None
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,'}d*.d1c'):
            DFile = file
    if DFile == None:
        print("No '}d*.d1c' file found!")
        os.system('pause')
        exit()    
    with open(DFile, newline='') as csvfile: #opening the data file csv
        dreader = csv.reader(csvfile, quotechar="\"")
        dPattern = "[0-9]" + tranNum[runCount] #!TODO
        for drow in dreader:
            if re.search(dPattern, drow[3]):
                decimalCheck(drow[10], True) #True = Quantity
                decimalCheck(drow[48], False)
                pCode.append(drow[11])
                tranTime.append(tFormat(drow[2]))
                
#parses the variables file
def vParse():
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,'}v*.d1c'):
            VFile = file    
    with open(VFile, newline='') as csvfile: #opening the variable csv file
        vreader = csv.reader(csvfile, quotechar="\"") 
        for vrow in vreader:
            if tranNum[runCount] == vrow[3][1:5]:
                if vrow[8] == "SEQUENCE#":
                    seqnum.append(vrow[9])
                elif vrow[8] == "ODOMETER":
                    odometer.append(format(vrow[9],7))
                elif vrow[8] == "pump":
                    pump.append(format(vrow[9],2))
                elif vrow[8] == "ID_VEHICLE":
                    id_vehicle.append(format(vrow[9],8))
                elif vrow[8] == "ID_CARD":
                    id_card.append(format(vrow[9],7))
                elif vrow[8] == "ID_ACCT":
                    id_acct.append(format(vrow[9],6))
                elif vrow[8] == "VEHICLE":
                    vehicle.append(format(vrow[9],4))

                #checks for null values in the variables 
                if len(odometer) < runCount:
                    odometer.append("0000000")
                elif len(seqnum)< runCount:
                    seqnum.append("0000")
                elif len(pump)< runCount:
                    pump.append("00")
                elif len(id_vehicle)< runCount:
                    id_vehicle.append("00000000")
                elif len(id_card)< runCount:
                    id_card.append("0000000")
                elif len(id_acct)< runCount:
                    id_acct.append("000000")
                elif len(vehicle)< runCount:
                    vehicle.append("0000")

def email(siteid, att1, att2):
    now = datetime.datetime.now()
    date = str(now.month) + '/' + str(tranDate[4:6]) + '/' + str(now.year)
    const=win32com.client.constants
    olMailItem = 0x0
    obj = win32com.client.Dispatch("Outlook.Application")
    newMail = obj.CreateItem(olMailItem)
    newMail.Subject = "{0} - PT File {1}".format(siteid, date)
    newMail.BodyFormat = 1 # olFormatHTML https://msdn.microsoft.com/en-us/library/office/aa219371(v=office.11).aspx
    newMail.HTMLBody = "<HTML><BODY>This time it works and the date is properly formatted</BODY></HTML>"
    newMail.To = "test@test.com"
    newMail.Attachments.Add(Source=att1)
    newMail.Attachments.Add(Source=att2)
    newMail.display()
    newMail.Send()

def fileIO():
    global siteid
    global tranDate
    global nDV
    source = ''
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,'pump*.tot'):
            pumptot = file
            source = os.getcwd()+'\\'+pumptot
    #creates directories for the sites, pt file dates, and d1c file backups
    if not os.path.exists("{0}".format(siteid)):
        os.makedirs("{0}".format(siteid))
    os.chdir("{0}".format(siteid))
    if not os.path.exists("{0}".format(tranDate)):
        os.makedirs("{0}".format(tranDate))
    os.chdir("{0}".format(tranDate))
    if not os.path.exists("d1c files"):
        os.makedirs("d1c files")
    ptFileName = nextDay(nDV)
    pumptotN = os.getcwd()+'\\'+pumptot
    shutil.move(source, pumptotN)
    f= open("pt{0}.dat".format(ptFileName),"w+")
    #Outputs the data line by line to the .dat file
    for i in range(runCount):
        f.write(siteid+seqnum[i]+STATCODE+totAmt[i]+ACT+TRANTYPE+pCode[i]+price+quantity[i]+odometer[i]+OID+pump[i]+tranNum[i]+tranDate+tranTime[i]+fill+id_vehicle[i]+id_card[i]+part_id+id_acct[i]+vehicle[i]+end+"\n")
    f.close()
    ptFile= ''
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,'pt*.dat'):
            filename = file
            ptFile = os.getcwd()+'\\'+filename
    os.chdir("..") 
    os.chdir("..")
    l = True
    while l:
        uI = input("would you like to email these files? (y/n): ")
        if uI =='y':
            print("sending email...")
            email(siteid, ptFile, pumptotN)
            l = False
        elif uI == "n":
            print("not sending email...")
            l = False
        else:
            print("please enter either y or n")
    cwd = os.getcwd()
    dest = os.getcwd() + '\\{0}\\{1}\\d1c files\\'.format(siteid,tranDate)
    h = "\\}}h{0}.d1c".format(tranDate)
    d = "\\}}d{0}.d1c".format(tranDate)
    v = "\\}}v{0}.d1c".format(tranDate)
    shutil.move(cwd + h, dest + h)
    shutil.move(cwd + d, dest + d)
    shutil.move(cwd + v, dest + v)

hParse()
