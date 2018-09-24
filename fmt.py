import re
import datetime

def tFormat(time,gasboy):
    nTime = time[0:5]
    if not gasboy:
        return (nTime[0:2] + nTime[3:5])
    else:
        temp = nTime.split(":")
        if temp[0][0] == "0":
            temp[0] = " " + temp[0][1]
        return temp[0] + ":" + temp[1] + " "


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

def decimalCheck(number, x):
    decimalfind = re.compile(r"\d+\.\d+")
    if decimalfind.match(number):
        return decimalSplit(number, x, True)
    else:
        return decimalSplit(number, x, False)

#Ensures the value that was put into it has the proper amount of zeros
def format(oD, num, gasboy):
    temp = oD
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

def tNumFMT(tran):
    if len(tran) > 4:
        return tran[(len(tran)-4):(len(tran))]
    else:
        temp = tran
        for __ in range(4 - len(tran)):
            temp = "0" + temp
        return temp

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
    
