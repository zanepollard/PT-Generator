import os
import shutil
import fnmatch
import yaml
import parse 
import fmt
import re
import csv
import datetime
import pysftp
import paramiko
from sys import exit
from base64 import decodebytes
from pathlib import Path

def salesOutput(pObj, config_data, root):
    ptOutput = bool(config_data['ptOutput'])
    gasboy = bool(config_data['gasboyOutput'])
    csvOutput = bool(config_data['csvOutput'])
    merchantAg = bool(config_data['merchantAg'])
    CFNcsv = bool(config_data['CFNcsv'])

    output = os.path.abspath(config_data.get('output_folder'))
    opFolder = os.path.abspath(ptFilePath(output, config_data, pObj))

    if (config_data.get('backup_sales') == True):
        backupSales(opFolder, config_data, pObj)

    filename = fileName(pObj, config_data, root)

    os.chdir(root)
    os.chdir(opFolder)

    
    if ptOutput:
        f = open(filename, "w+")
        for i in range(len(pObj.pList)):
            f.write(pObj.pList[i].ptPrint())
        f.close()

    elif gasboy:
        f = open(filename, "w+")
        for i in range(len(pObj.pList)):
            f.write(pObj.pList[i].gasboyPrint())
        f.close()

    elif csvOutput:
        header = ['Transaction Date', 'Site', 'Trans #', 'Seq #', 'Auth #', 'Card #', 'Product', 'Prod ID', 
              'Pump', 'Quantity', 'PPG', 'Total','Day', 'Time', 'Card Type']

        os.chdir(root)
        os.chdir(opFolder)

        with open(filename,'w', newline='') as csvfile:
            tranWriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_NONNUMERIC)
            tranWriter.writerow(header)
            for i in range(len(pObj.pList)):
                tranWriter.writerow(pObj.pList[i].csvPrint())
        csvfile.close()

    elif merchantAg:
        f = open(filename, "w+")
        for i in range(len(pObj.pList)):
            f.write(pObj.pList[i].merchantAgPrint())
        f.close()

    elif CFNcsv:
        os.chdir(root)
        os.chdir(opFolder)

        with open(filename,'w', newline='') as csvfile:
            tranWriter = csv.writer(csvfile, delimiter=',')
            for i in range(len(pObj.pList)):
                tranWriter.writerow(pObj.pList[i].CFNcsvPrint())
        csvfile.close()



    sftpFolder = root + '\\sftpQueue'
    if(config_data.get('USE_SFTP') == True):
        if not os.path.exists(sftpFolder):
            os.makedirs(sftpFolder)
        shutil.copyfile((opFolder + '\\' + filename), (sftpFolder + '\\' + filename))

#Sets file name based on config.yaml options
def fileName(pObj,config_data, root):
    filename = ''
    os.chdir(root)
    if (config_data.get('file_name')['custom']['custom_beginning'] == True):
        filename = filename + config_data.get('file_name')['custom']['text']
    if (config_data.get('file_name')['siteid'] == True):
        if( pObj.pList != []):
            filename = filename + pObj.pList[0].siteid + "_"
    #include date
    if (config_data.get('file_name')['date']['include'] == True):
        #True = yymmdd False = mmddyy
        if (config_data.get('file_name')['date']['format'] == True):
            filename = filename + pObj.nDV[8:10] + pObj.nDV[0:2] + pObj.nDV[3:5] 
        else:
            if (config_data.get('file_name')['date']['add_day'] == True):
                filename = filename + fmt.nextDay(pObj.nDV)
            else:
                print(config_data.get('file_name')['date']['fullyear'])
                if(config_data.get('file_name')['date']['fullyear'] == True):
                    filename = filename + pObj.nDV[0:2]+ pObj.nDV[3:5]+ pObj.nDV[6:10]
                else:
                    filename = filename + pObj.nDV[0:2]+ pObj.nDV[3:5]+ pObj.nDV[8:10]
    return filename + config_data.get('file_name')['extension']

#Generates path PT file will be generated to according to options seet in config
def ptFilePath(output, config_data, pObj):
    ptLoc = output
    if(config_data.get('output_options')['site_folder'] == True):
        for __ in pObj.pList:
            if( pObj.pList != []):
                ptLoc = ptLoc + "\\" + pObj.pList[0].siteid
                break
    if(config_data.get('output_options')['date_folder'] == True):
        if( pObj.pList != []):
            ptLoc = ptLoc + "\\" + pObj.pList[0].tranDate
    if not os.path.exists(ptLoc):
        os.makedirs(ptLoc)
    if (config_data.get('pump_total') == True):
        movePumpTot(ptLoc, config_data, pObj)
    return ptLoc

#moves pump total file if specified by YAML
def movePumpTot(ptLoc, config_data, pObj):
    #cwd = os.getcwd()
    start = os.path.abspath(config_data.get('input_folders')[0])
    os.chdir(start)
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,"pump{0}.tot".format(pObj.nDV[0:2]+ pObj.nDV[3:5])):
            
            pumptot = file
            shutil.move(start + "\\" + pumptot, ptLoc + "\\"+ pumptot)

#Backs up d1c files to folder specified by YAML config
def backupSales(opFolder,config_data, pObj):
    cwd = os.getcwd()
    fileLists = [[],[],[]]

    for file in os.listdir(cwd):
        if re.match(r'[}]h\d{6}[.].1c',file):
            fileLists[0].append(file)
        if re.match(r'[}]d\d{6}[.].1c',file):
            fileLists[1].append(file)   
        if re.match(r'[}]v\d{6}[.].1c',file):
            fileLists[2].append(file)

    if(config_data.get('backup_options')['backup_location']['output_override'] == False):
        bkFold = opFolder
    else:
        bkFold = config_data.get('backup_options')['backup_loaction']['backup_folder']
        if(config_data.get('backup_options')['site_folder'] == True):
            bkFold = bkFold + pObj.pList[0].siteid
        if(config_data.get('backup_options')['data_folder'] == True):
            bkFold = bkFold + pObj.pList[0].tranDate
    bkFold = os.path.abspath(bkFold + "\\d1c files")
    if not os.path.exists(bkFold):
        os.makedirs(bkFold)

    for fList in fileLists:
        for item in fList:
            shutil.move(cwd + item, bkFold + item)



#Checks folder for sales files and sorts the list
def fileFind(folder, pullMode):
    h = []
    d = []
    v = []
    dateRun = datetime.datetime.today()
    year = str(dateRun.year)[2:4]

    if(pullMode == "MONTHLY"):
        month = fmt.datePadder(dateRun.month)
        
        for file in os.listdir(folder):
            if re.match(rf'[}}]h{year}{month}\d{{2}}[.][^s]1c', file):
                h.append(file)
            if re.match(rf'[}}]d{year}{month}\d{{2}}[.][^s]1c', file):
                d.append(file)
            if re.match(rf'[}}]v{year}{month}\d{{2}}[.][^s]1c', file):
                v.append(file)
    elif(pullMode == "DAILY"):
        prevDate = dateRun - datetime.timedelta(days=1)
        day = fmt.datePadder(prevDate.day)
        month = fmt.datePadder(prevDate.month)
        for file in os.listdir(folder):
            if re.match(rf'[}}]h{year}{month}{day}[.][^s]1c', file):
                h.append(file)
            if re.match(rf'[}}]d{year}{month}{day}[.][^s]1c', file):
                d.append(file)
            if re.match(rf'[}}]v{year}{month}{day}[.][^s]1c', file):
                v.append(file)
    elif(pullMode == "ALL"):
        print("ALL")
        for file in os.listdir(folder):
            if re.match(r'[}]h\d{6}[.][^s]1c',file):
                h.append(file)
            if re.match(r'[}]d\d{6}[.][^s]1c',file):
                d.append(file)   
            if re.match(r'[}]v\d{6}[.][^s]1c',file):
                v.append(file)
    h.sort()        
    d.sort()        
    v.sort()
    if(len(h) == 0):
        exit()
    if(((len(h) == len(d) == len(v)) != True)):
        exit()
    return [h,d,v]


#Loads YAML config file
def yaml_loader(filepath):
    with open(filepath, "r") as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

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