import os
import shutil
import fnmatch
import yaml
import parse 
import fmt
import re
import csv
from datetime import datetime
from pathlib import Path

def salesOutput(pObj, config_data, root):
    ptOutput = bool(config_data['ptOutput'])
    gasboy = bool(config_data['gasboyOutput'])
    csvOutput = bool(config_data['csvOutput'])
    merchantAg = bool(config_data['merchantAg'])

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

    elif gasboy:
        f = open(filename, "w+")
        for i in range(len(pObj.pList)):
            f.write(pObj.pList[i].gasboyPrint())

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

#Sets file name based on config.yaml options
def fileName(pObj,config_data, root):
    filename = ''
    os.chdir(root)
    if (config_data.get('file_name')['custom']['custom_beginning'] == True):
        filename = filename + config_data.get('file_name')['custom']['text']
    if (config_data.get('file_name')['siteid'] == True):
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
                filename = filename + pObj.nDV[0:2]+ pObj.nDV[3:5]+ pObj.nDV[8:10]
    return filename + config_data.get('file_name')['extension']

#Generates path PT file will be generated to according to options seet in config
def ptFilePath(output, config_data, pObj):
    ptLoc = output
    if(config_data.get('output_options')['site_folder'] == True):
        ptLoc = ptLoc + "\\" + pObj.pList[0].siteid
    if(config_data.get('output_options')['date_folder'] == True):
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
def fileFind(folder):
    h = []
    d = []
    v = []
    for file in os.listdir(folder):
        if re.match(r'[}]h\d{6}[.].1c',file):
            h.append(file)
        if re.match(r'[}]d\d{6}[.].1c',file):
            d.append(file)   
        if re.match(r'[}]v\d{6}[.].1c',file):
            v.append(file)
    h.sort()        
    d.sort()        
    v.sort()
    if((len(h) == len(d) == len(v)) != True):
        eName = folder + "\\{0}.log".format(datetime.date(datetime.now()))
        log = open(eName, 'a+')
        log.write("Not enough files in " + folder + " to make a pt file. check to see if all h,d, and v files are in the folder")
        exit()
    return [h,d,v]


#Loads YAML config file
def yaml_loader(filepath):
    with open(filepath, "r") as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

