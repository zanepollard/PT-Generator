from email.message import EmailMessage
from genericpath import isdir, isfile
import os
import shutil
import re
import csv
from datetime import datetime
from datetime import timedelta
import smtplib
import pysftp
import paramiko
from sys import exit
from base64 import decodebytes



def get_lastRun_Date(root):
    os.chdir(root)
    if(os.path.exists('lastRun')):
        with open('lastRun', 'r') as lastRun:
            reader = csv.reader(lastRun)
            row1 = next(reader)
            lastRunDate = datetime(int(row1[0]), int(row1[1]), int(row1[2]))
            print(f"Software last run at {lastRunDate}")
    else:
        lastRunDate = datetime.today()
    return lastRunDate


def set_lastRun_Date(dateRun, root):
    os.chdir(root)
    with open('lastRun', 'w') as lastRun:
        writer = csv.writer(lastRun, delimiter=',')
        writer.writerow([dateRun.year, dateRun.month, dateRun.day])
    

def fileFind(folder, config_data, SOFTWARE_VERSION, pullMode, recentDate = None, pastDate = None):
    files = []
    if(SOFTWARE_VERSION == "VB6"):
        extension = f"{'^s' if config_data['processors_VB6']=='' else config_data['processors_VB6']}"

        h = []
        d = []
        v = []
        
        if(pullMode == "DAILY"):
            year = str(recentDate.year)[2:4]
            day = str(recentDate.day)
            month = str(recentDate.month)
            for file in os.listdir(folder):
                if re.match(rf'[}}]h{year}0?{month}0?{day}[.][{extension}]1c', file):
                    h.append(f"{folder}/{file}")
                if re.match(rf'[}}]d{year}0?{month}0?{day}[.][{extension}]1c', file):
                    d.append(f"{folder}/{file}")
                if re.match(rf'[}}]v{year}0?{month}0?{day}[.][{extension}]1c', file):
                    v.append(f"{folder}/{file}")
        elif(pullMode == "ALL"):
            for file in os.listdir(folder):
                if re.match(rf'[}}]h\d{{6}}[.][{extension}]1c',file):
                    h.append(f"{folder}/{file}")
                if re.match(rf'[}}]d\d{{6}}[.][{extension}]1c',file):
                    d.append(f"{folder}/{file}")   
                if re.match(rf'[}}]v\d{{6}}[.][{extension}]1c',file):
                    v.append(f"{folder}/{file}")
        elif(pullMode == "RANGE"):
            date_list = [recentDate - datetime.timedelta(days=x) for x in range(1, (recentDate-pastDate).days + 1)]
            for date in date_list:
                year = str(date.year)[2:4]
                day = str(date.day)
                month = str(date.month)
                for file in os.listdir(folder):
                    if re.match(rf'[}}]h{year}0?{month}0?{day}[.][^s]1c', file):
                        h.append(f"{folder}/{file}")
                    if re.match(rf'[}}]d{year}0?{month}0?{day}[.][^s]1c', file):
                        d.append(f"{folder}/{file}")
                    if re.match(rf'[}}]v{year}0?{month}0?{day}[.][^s]1c', file):
                        v.append(f"{folder}/{file}")
        if(len(h) == 0):
            exit()
        if(((len(h) == len(d) == len(v)) != True)):
            exit()
        return [sorted(h),sorted(d),sorted(v)]
    else:
        if(pullMode == "ALL"):
            for file in os.listdir(folder):
                if re.match(rf'TransactionTable[\d]{{6}}[.csv]', file):
                    files.append(f"{folder}\\{file}")
        elif(pullMode == "DAILY"):
            for file in os.listdir(folder):
                if re.match(rf'TransactionTable{str(recentDate.year)[2:4]}0?{str(recentDate.month)}0?{str(recentDate.day)}[.csv]', file):
                    files.append(f"{folder}\\{file}")
        elif(pullMode == "RANGE"):
            date_list = [recentDate - timedelta(days=x) for x in range(1, ((recentDate-pastDate).days + 1))]
            for date in date_list:
                for file in os.listdir(folder):
                    if re.match(rf'TransactionTable{str(date.year)[2:4]}0?{str(date.month)}0?{str(date.day)}[.csv]', file):
                        files.append(f"{folder}\\{file}")
        return sorted(files)


def fileName(inputDate, config_data):
    fileName = ""
    dateString = ""
    fileDate = inputDate

    if (config_data.get('file_name')['date']['include'] == True):
        if (config_data.get('file_name')['date']['add_day'] == False):
            inputDate = inputDate - timedelta(days=1)
        day = f"{'0'+str(fileDate.day) if (len(str(inputDate.day))<2) else str(inputDate.day)}"
        month = f"{'0'+str(fileDate.month) if (len(str(inputDate.month))<2) else str(inputDate.month)}"
        year = str(fileDate.year)[2:4]

        dateString = f"{str(year)+str(month)+str(day) if config_data.get('file_name')['date']['format']==True else str(month)+str(day)+str(year)}"

    fileName = (f"{config_data.get('file_name')['custom']['text']+'_' if config_data.get('file_name')['custom']['custom_beginning'] == True else ''}"
                f"{config_data.get('site_number')+'_' if config_data.get('file_name')['siteid'] == True else ''}"
                f"{dateString}"
                f"{config_data.get('file_name')['extension']}")
    
    return fileName

def salesOutput_ind(parseObj, config_data, root, outputFolder):
    os.chdir(outputFolder)
    for key in parseObj.transactions:
        filename = fileName(datetime(int(parseObj.transactions[key].tranDate[0:4]), int(parseObj.transactions[key].tranDate[4:6]), int(parseObj.transactions[key].tranDate[6:8])), config_data)
        with open(filename, "a",newline='') as outputFile:
            if bool(config_data['CFNcsv']):
                tranWriter = csv.writer(outputFile, delimiter=',')
                tranWriter.writerow(parseObj.transactions[key].CFNcsvPrint(config_data))
    os.chdir(root)


def salesOutput(parseObj, config_data, root, outputFolder):
    os.chdir(outputFolder)
    filename = fileName(datetime(int(parseObj.tranDate[0:4]), int(parseObj.tranDate[4:6]), int(parseObj.tranDate[6:8])), config_data)
    with open(filename, "a", newline='') as outputFile:
        if bool(config_data['VDPOutput']):
            for key in parseObj.transactions:
                outputFile.write(parseObj.transactions[key].VDPPrint(config_data))
            
        elif bool(config_data['AGTRAX']):
            for key in parseObj.transactions:
                outputFile.write(parseObj.transactions[key].AGTRAXPrint(config_data))

        elif bool(config_data['JCDoyle']):
            header = True
            if os.path.isfile(filename):
                header = False
            if header:
                outputFile.write("TRAN   TY  CUSTOMER     CARD DATE       TIME  P#  GAL    PRICE   TOTAL\n")
            for key in parseObj.transactions:
                outputFile.write(parseObj.transactions[key].JCDoylePrint(config_data))

        elif bool(config_data['ptOutput']):
            for key in parseObj.transactions:
                outputFile.write(parseObj.transactions[key].ptPrint(config_data))

        elif bool(config_data['gasboyOutput']):
            for key in parseObj.transactions:
                outputFile.write(parseObj.transactions[key].gasboyPrint(config_data))                  

        elif bool(config_data['csvOutput']):
            header = ['Transaction Date', 'Site', 'Trans #', 'Seq #', 'Auth #', 'Card #', 'Product', 'Prod ID', 
                'Pump', 'Quantity', 'PPG', 'Total','Day', 'Time', 'Card Type']

            tranWriter = csv.writer(outputFile, delimiter=',',quoting=csv.QUOTE_NONNUMERIC)
            tranWriter.writerow(header)
            for key in parseObj.transactions:
                tranWriter.writerow(parseObj.transactions[key].csvPrint(config_data))

        elif bool(config_data['merchantAg']):
            for key in parseObj.transactions:
                outputFile.write(parseObj.transactions[key].merchantAgPrint(config_data))
            
        elif bool(config_data['CFNcsv']):
            tranWriter = csv.writer(outputFile, delimiter=',')
            for key in parseObj.transactions:
                tranWriter.writerow(parseObj.transactions[key].CFNcsvPrint(config_data))
        elif bool(config_data['FuelMaster']):
            for key in parseObj.transactions:
                outputFile.write(parseObj.transactions[key].FuelMasterPrint(config_data))  
    os.chdir(root)


def backupFiles(folder):
    os.chdir(folder)
    backupFolder = f"{folder}\\backup"
    if not os.path.exists(backupFolder):
        os.makedirs(backupFolder)
    for file in os.listdir(folder):
        if os.path.isfile(file):
            shutil.copyfile(os.path.abspath(f"{folder}\\{file}"), os.path.abspath(f"{backupFolder}\\{file}"))

def log_events(logfile, message):
    with open(logfile, "a") as log_output:
        log_output.write(message)

def emailTransfer(outputFolder, mailServer, port, mailUser, mailPassword, messageSubject, messageBody, recipients):
    backupFiles(outputFolder)
    os.chdir(outputFolder)

    messages = []

    try:
        server = smtplib.SMTP(mailServer, port)
        server.ehlo()
        server.starttls()
        server.login(mailUser, mailPassword)
    except Exception:
        print("Could not connect to SMTP server. Check connection or login info.\n")

    msg = EmailMessage()
    msg['Subject'] = messageSubject
    msg['From'] = mailUser
    msg.set_content(messageBody)
    for file in os.listdir(outputFolder):
        msg.add_attachment(open(file, 'r').read(), filename=file)
    for recipient in recipients:
        msg['To'] = recipient
        messages.append(msg)
    
    for message in messages:
        try:
            server.send_message(message)   
        except Exception:
            print("Message failed to send\n")
            return
    for file in os.listdir(outputFolder):
        os.remove(file)

def transfer_SFTP(salesFile, username, password, hostname, keydata):
    key = paramiko.RSAKey(data=decodebytes(bytes(keydata, encoding="ascii")))
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.add(hostname, 'ssh-rsa', key)

    with pysftp.Connection(hostname, username=username, password=password, cnopts=cnopts) as sftp:
        try:
            sftp.put(salesFile ,preserve_mtime=True) 
            #Transfer to SFTP server. If this fails we do not delete the local file. This allows us to still make a sales file locally even if upload fails.
            #We will attempt another transfer during the next file generation.
        except IOError:
            #'Failure'
            print("IOError")
        except OSError:
            #'Failure'
            print("OSError")
        else:
            os.remove(salesFile) #and now we delete the local file since we succeeded. 
    
    
    
    