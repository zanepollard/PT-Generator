import re
import datetime

#Formats time in sales files
def tFormat(time,gasboy):
    if not gasboy:
        return time
    else:
        if time[0] == "0":
            time[0] = " "
        return str(time[0:2] + ":" + time[2:4] + " ")

#Formats date object to pt output
def dFormat(date):
    return str(date[2:8])

def dGasboyFormat(date):
    if(len(date)==8):
        return date[4:6] + "/" + date[6:8] + "/" + date[2:4]
    else:
        return "01/01/01"

#Pulls date from sales file, converts it to a date object, and adds a day to the date object 
#(Only used at Anaheim Truck Depot sites, only used for the file name)
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
    return (month + day + str(date.year)[2:4])

#splits numbers based on the decimals and pads them with zeros depending on the variable itself
def decimalSplit(number, x, y): #y is decimal true/false
    if x: #quantity value check
        if y: #check if it has a decimal or not
            temp = number.split('.')
            for __ in range(5 - len(temp[0])):
                temp[0] = "0" + temp[0]
            for __ in range(3-len(temp[1])):
                temp[1] = temp[1] + "0"
            return(temp[0] + temp[1])
        else:
            temp = number
            for __ in range(5-len(temp)):
                temp = "0"+temp
            return(temp + "000")
    else:
        if y:
            temp = number.split('.')
            for __ in range(4 - len(temp[0])):
                temp[0] = "0" + temp[0]
            if len(temp[1]) > 2:
                temp[1] = temp[1][0:2]
                for __ in range(2 - len(temp[1])):
                    temp[1] = temp[1]+"0"
            else:
                for __ in range(2 - len(temp[1])):
                    temp[1] = temp[1] + "0"
            return(temp[0] + temp[1])
        else:
            temp = number
            for __ in range(4 - len(number)):
                temp = "0" + temp
            return(temp + "00")

#Checks the number for a decimal value. Some numbers in the data sales file won't have decimal points and need to 
#be handled differently
def decimalCheck(number, x):
    decimalfind = re.compile(r"\d+\.\d+")
    if decimalfind.match(number):
        return decimalSplit(number, x, True)
    else:
        return decimalSplit(number, x, False)

#Ensures the value that was put into it has the proper amount of zeros
def format(oD, num, gasboy):
    temp = str(oD)
    if len(temp)>num:
        temp = temp[len(oD) - num:len(oD)] 
    for __ in range(num - len(oD)):
        if not gasboy:
            temp = "0" + temp
        else:
            temp = " " + temp
    if gasboy:
        temp = temp + " "
    return temp

#Sets the transaction number to a char length of 4.
#If the transaction number is larger than 4, it will cut the leading numbers
#If it is shorter, it will add leading zeros
def tNumFMT(tran):
    if len(tran) > 4:
        return tran[(len(tran)-4):(len(tran))]
    else:
        temp = tran
        for __ in range(4 - len(tran)):
            temp = "0" + temp
        return temp

#Formats the price per gallon value
#If it is not a gasboy format, it will remove the decimal and add zeros until it reaches 8 chars
#If it is the gasboy format, it will ensure the length of the value is 5, making the decimal values longer or shorter depending on the value before the decimal ex 10.00, 1.000
def pFormat(price, gasboy):
    if not gasboy:
        temp = price.replace(".", "")
        for __ in range(8 - len(temp)):
            temp = temp + "0"
        return temp    
    else:
        pRe = re.compile(r'\d*\.\d*')
        if pRe.match(price):
            pr = price.split('.')
            for _ in range(4 - len(pr[0])-len(pr[1])):
                pr[1] += "0"
            return pr[0] + "." + pr[1] + " "
        else:
            z = ""
            for __ in range(4-len(price)):
                z = z + "0"
            return price + "." + z + " "

#Alternate to decimalcheck for gasboy output
def gBoyFormat(v, l1, l2):
    temp = v.split(".")
    for _ in range(l1 - len(temp[0])):
        temp[0] = " " + temp[0]
    if(len(temp) == 2):
        for _ in range(l2 - len(temp[1])):
            temp[1] = temp[1] + "0"        
    else:
        temp.append("0")
        for _ in range(l2-1):
            temp[1] = temp[1] + "0"
    return temp[0] + "." + temp[1] + " "


#MERCHANT AG FORMATTING

# l is section length, bE is beginning or end bool (T/F), padChar is character to pad with
def mAgPadding(l, i, bE, padChar):
    i = re.sub(r'[.]','', i, flags=re.IGNORECASE)
    padding = ""
    if(len(i) <= l):
        for __ in range(l-len(i)):
            padding = padding + padChar
        if bE:
            return(padding + i)
        else:
            return(i + padding)
    else:
        if bE:
            limit = len(i)
            return(i[(limit-l):(limit)])
        else:
            return(i[0:l])

def mAgDateTimeFormat(i):
    i = re.sub(r'[-:]','', i, flags=re.IGNORECASE)
    return i
    

def mAgCardName(name):
    if(name == "VS"):
        return "VISA "
    elif(name == "MC"):
        return "MCRD "
    elif(name == "DS"):
        return "DISC "
    elif(name == "AX"):
        return "AEXP "
    elif(name == "VF"):
        return "VOYG "
    else:
        return "UNKNO"

def mAgDecimalLength(i, l):
    n = i.split(".")
    if(len(n) == 1):
        return n[0] + ".000"
    else:
        for __ in range(l - len(n[1])):
            n[1] = n[1] + "0"
        return n[0] + "." + n[1]

def datePadder(i):
    temp = str(i)
    if(len(temp) < 2):
        return "0" + temp
    else:
        return temp

def padAdd(lR, fill, length, input):
    output = str(input)
    padding = ""
    
    for __ in range(length - len(str(input))):
        padding = fill + padding
    if lR == "left":
        output = padding + output
    elif lR == "right":
        output = output + padding 
    return str(output)


def cutLength(lR, length, input):
    output = str(input)
    if length < len(input):
        if lR == "left":
            output = output[0:length]
        else:
            output = output[(len(output)-length):(len(output))]
    return str(output)


def decimalFormat(sigFig, input):
    output = input.split(".")
    temp = ""
    if len(output) == 1:
        for __ in range(sigFig):
            temp = temp + "0"
        output.append(temp)
    output[1] = padAdd("right", "0", sigFig, str(output[1]))
    return (str(output[0]) + str(output[1]))

def decimalPad(sigFig, input):
    output = input.split(".")
    temp = ""
    if len(output) == 1:
        for __ in range(sigFig):
            temp = temp + "0"
        output.append(temp)
    else:
        if (len(output[1])>sigFig):
            output[1] = output[1][0:sigFig]
    return str(output[0]) + "." + padAdd("right", "0", sigFig, str(output[1]))