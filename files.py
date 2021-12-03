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
            date_list = [recentDate - timedelta(days=x) for x in range(0, (recentDate-pastDate).days + 1)]
            for date in date_list:
                year = str(date.year)[2:4]
                day = str(date.day)
                month = str(date.month)
                for file in os.listdir(folder):
                    if re.match(rf'[}}]h{year}0?{month}0?{day}[.][{extension}]1c', file):
                        h.append(f"{folder}/{file}")
                    if re.match(rf'[}}]d{year}0?{month}0?{day}[.][{extension}]1c', file):
                        d.append(f"{folder}/{file}")
                    if re.match(rf'[}}]v{year}0?{month}0?{day}[.][{extension}]1c', file):
                        v.append(f"{folder}/{file}")
        if (len(h) == len(d) == len(v)): 
            return [sorted(h),sorted(d),sorted(v)]
        else:
            return []
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
            date_list = [recentDate - timedelta(days=x) for x in range(0, ((recentDate-pastDate).days + 1))]
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


def salesOutput_individual(parseObj, config_data, root, outputFolder, log_file):
    os.chdir(outputFolder)
    fileObjDict = {}
    sorted_transactions = sorted(parseObj.transactions.values(), key=lambda x: (x.tranDate,x.tranTime))
    for transaction in sorted_transactions:
        transactionDate = transaction.tranDate
        if transactionDate not in fileObjDict:
            file_name = fileName(datetime(int(transactionDate[0:4]), 
                                          int(transactionDate[4:6]), 
                                          int(transactionDate[6:8])), 
                                          config_data)
            fileObjDict[transactionDate] = open(file_name, "a",newline='')
        writeFile(transaction,fileObjDict[transactionDate],config_data)

    for key in fileObjDict:
        fileObjDict[key].close()

    os.chdir(root)


def salesOutput(parseObj, config_data, root, outputFolder, log_file):
    os.chdir(outputFolder)
    sorted_transactions = sorted(parseObj.transactions.values(), key=lambda x: (x.tranDate,x.tranTime))
    filename = fileName(datetime(int(parseObj.tranDate[0:4]), 
                                 int(parseObj.tranDate[4:6]), 
                                 int(parseObj.tranDate[6:8])), 
                                 config_data)
    with open(filename, "a", newline='') as outputFile:
        for transaction in sorted_transactions:
            outputFile = writeFile(transaction, outputFile, config_data) 
    os.chdir(root)


def writeFile(transaction, file_object, config_data):
    if bool(config_data['VDPOutput']):
        file_object.write(transaction.VDPPrint(config_data))
        
    elif bool(config_data['AGTRAX']):
        file_object.write(transaction.AGTRAXPrint(config_data))

    elif bool(config_data['JCDoyle']):
        header = "TRAN   TY  CUSTOMER     CARD DATE       TIME  P#  GAL    PRICE   TOTAL\n"
        if os.stat(file_object.fileno()).st_size == 0:
            file_object.write(header)
        file_object.write(transaction.JCDoylePrint(config_data))

    elif bool(config_data['ptOutput']):
        file_object.write(transaction.ptPrint(config_data))

    elif bool(config_data['gasboyOutput']):
        file_object.write(transaction.gasboyPrint(config_data))                  

    elif bool(config_data['csvOutput']):
        header = ['Transaction Date', 'Site', 'Trans #', 'Seq #', 'Auth #', 'Card #', 'Product', 'Prod ID', 
            'Pump', 'Quantity', 'PPG', 'Total','Day', 'Time', 'Card Type']

        tranWriter = csv.writer(file_object, delimiter=',',quoting=csv.QUOTE_NONNUMERIC)
        if file_object.tell() == 0:
            tranWriter.writerow(header)
        tranWriter.writerow(transaction.csvPrint(config_data))

    elif bool(config_data['merchantAg']):
        file_object.write(transaction.merchantAgPrint(config_data))
        
    elif bool(config_data['CFNcsv']):
        tranWriter = csv.writer(file_object, delimiter=',')
        file_object.write(transaction.CFNcsvPrint(config_data))

    elif bool(config_data['FuelMaster']):
        file_object.write(transaction.FuelMasterPrint(config_data)) 
    
    return file_object


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

def transfer_email(outputFolder, mailServer, port, mailUser, mailPassword, messageSubject, messageBody, recipients):
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

    for recipient in recipients:
        msg = EmailMessage()
        msg['To'] = recipient
        msg['Subject'] = messageSubject
        msg['From'] = mailUser
        msg.set_content(messageBody)
        for file in os.listdir(outputFolder):
            if os.path.isfile(file):
                msg.add_attachment(open(file, 'r').read(), filename=file)
        messages.append(msg)
    
    for message in messages:
        try:
            server.send_message(message)   
        except Exception:
            print(f"Message to {message['To']} failed to send\n")
            
    for file in os.listdir(outputFolder):
        if os.path.isfile(file):
            os.remove(file)

def transfer_SFTP(output_folder, username, password, hostname, keydata):
    key = paramiko.RSAKey(data=decodebytes(bytes(keydata, encoding="ascii")))
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.add(hostname, 'ssh-rsa', key)

    with pysftp.Connection(hostname, username=username, password=password, cnopts=cnopts) as sftp:
        for file in os.listdir(output_folder):
            if os.path.isfile(file):
                try:
                    sftp.put(file ,preserve_mtime=True) 
                    #Transfer to SFTP server. If this fails we do not delete the local file. This allows us to still make a sales file locally even if upload fails.
                    #We will attempt another transfer during the next file generation.
                except IOError:
                    #'Failure'
                    print("IOError")
                except OSError:
                    #'Failure'
                    print("OSError")
                else:
                    os.remove(file) #and now we delete the local file since we succeeded. 
    
    
    
    