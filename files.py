import os
import shutil
import fnmatch
import yaml
import parse
import fmt
from datetime import datetime
from pathlib import Path

#generates the file name in standard set in config file, outputs to file
def makePT(pObj, config_data,root):
    output = os.path.abspath(config_data.get('output_folder'))
    gasboy = config_data.get('gasboyOutput')
    opFolder = os.path.abspath(ptFilePath(output, config_data, pObj))
    if (config_data.get('backup_sales') == True):
        backupSales(opFolder, config_data, pObj)

    filename = fileName(pObj,config_data, root)
    os.chdir(root)
    os.chdir(opFolder)
    if not gasboy:
        f = open(filename, "w+")
    else:
        f = open(filename, "a+")
    if not gasboy:
        for i in range(len(pObj.pList)):   
            f.write(pObj.pList[i].siteid + pObj.pList[i].seqnum + pObj.pList[i].STATCODE + pObj.pList[i].totAmt +
                    pObj.pList[i].ACT + pObj.pList[i].TRANTYPE + pObj.pList[i].pCode + pObj.pList[i].price + 
                    pObj.pList[i].quantity + pObj.pList[i].odometer + pObj.pList[i].OID + pObj.pList[i].pump +
                    pObj.pList[i].tranNum + pObj.pList[i].tranDate + pObj.pList[i].tranTime + pObj.pList[i].FILL +
                    pObj.pList[i].vehicle + pObj.pList[i].id_card + pObj.pList[i].PART_ID + pObj.pList[i].id_acct +
                    pObj.pList[i].id_vehicle + pObj.pList[i].END + "\n")
    else:
        for i in range(len(pObj.pList)):
            carwash =""
            for x in ("07 ","08 ","09 "):
                if pObj.pList[i].pCode == x:
                    carwash = "CARWASH "
            f.write(pObj.pList[i].siteid + pObj.pList[i].seqnum + pObj.pList[i].id_card + 
                    pObj.pList[i].id_acct + "000 " + pObj.pList[i].vehicle + pObj.pList[i].tranDate +
                    pObj.pList[i].tranTime + pObj.pList[i].pump + pObj.pList[i].pCode +
                    pObj.pList[i].quantity + pObj.pList[i].price + pObj.pList[i].totAmt +
                    pObj.pList[i].odometer + carwash+"\n")
    print("end of one file")
    f.close()

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
    h = "\\}}h{0}.d1c".format(pObj.pList[0].tranDate)
    d = "\\}}d{0}.d1c".format(pObj.pList[0].tranDate)
    v = "\\}}v{0}.d1c".format(pObj.pList[0].tranDate)
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
    shutil.move(cwd + h, bkFold + h)
    shutil.move(cwd + d, bkFold + d)
    shutil.move(cwd + v, bkFold + v)

#Checks folder for sales files and sorts the list
def fileFind(folder):
    h = []
    d = []
    v = []
    for file in os.listdir(folder):
        if fnmatch.fnmatch(file,'}h*.d1c'):
            h.append(file)
        if fnmatch.fnmatch(file,'}d*.d1c'):
            d.append(file)   
        if fnmatch.fnmatch(file,'}v*.d1c'):
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

