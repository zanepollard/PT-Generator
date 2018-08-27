import os
import shutil
import fnmatch
import yaml
import parse
import fmt

#generates the file name in standard set in config file, outputs to file
def makePT(pObj, input, config_data):
    filename = ''
    output = config_data.get('output_folder')
    opFolder = ptFilePath(output, config_data, pObj)
    if (config_data.get('backup_sales') == True):
        backupSales(opFolder, config_data, pObj)
    if (config_data.get('file_name')['custom']['custom_beginning'] == True):
        filename = filename + config_data.get('file_name')['custom']['text']
    if (config_data.get('siteid') == True):
        filename = filename + pObj.pList[0].siteid
    #include date
    if (config_data.get('file_name')['date']['include'] == True):
        #True = yymmdd False = mmddyy
        if (config_data.get('file_name')['date']['format'] == True):
            filename = filename + pObj.nDV[8:10] + pObj.nDV[0:2] + pObj.nDV[3:5] 
        else:
            if (config_data.get('file_name')['date']['add_day'] == True):
                filename = filename + fmt.nextDay(pObj.nDV)
            else:
                filename = filename  + pObj.nDV[0:2]+ pObj.nDV[3:5]+ pObj.nDV[8:10] 
    filename = filename + config_data.get('file_name')['extension']
    
    os.chdir(opFolder)
    f= open(filename, "w+")
    #Outputs the data line by line to the .dat file
    for i in range(len(pObj.pList)):
        f.write(pObj.pList[i].siteid + pObj.pList[i].seqnum + pObj.pList[i].STATCODE + pObj.pList[i].totAmt +
                pObj.pList[i].ACT + pObj.pList[i].TRANTYPE + pObj.pList[i].pCode + pObj.pList[i].PRICE + 
                pObj.pList[i].quantity + pObj.pList[i].odometer + pObj.pList[i].OID + pObj.pList[i].pump +
                pObj.pList[i].tranNum + pObj.pList[i].tranDate + pObj.pList[i].tranTime + pObj.pList[i].FILL +
                pObj.pList[i].id_vehicle + pObj.pList[i].id_card + pObj.pList[i].PART_ID + pObj.pList[i].id_acct +
                pObj.pList[i].vehicle + pObj.pList[i].END + "\n")
    f.close()

#Generates path PT file will be generated to according to options seet in config
def ptFilePath(output, config, pObj):
    ptLoc = output
    if(config.get('output_options')['site_folder'] == True):
        ptLoc = ptLoc + "\\" + pObj.pList[0].siteid
    if(config.get('output_options')['date_folder'] == True):
        ptLoc = ptLoc + "\\" + pObj.pList[0].tranDate
    if not os.path.exists(ptLoc):
        os.makedirs(ptLoc)
    if (config.get('pump_total') == True):
        movePumpTot(ptLoc)
    return ptLoc

#moves pump total file if specified by YAML
def movePumpTot(iput):
    cwd = os.getcwd()
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,'pump*.tot'):
            pumptot = file
    shutil.move(cwd + "\\" + pumptot, iput + "\\"+ pumptot)

#Backs up d1c files to folder specified by YAML config
def backupSales(iput,config, pObj):
    cwd = os.getcwd()
    h = "\\}}h{0}.d1c".format(pObj.pList[0].tranDate)
    d = "\\}}d{0}.d1c".format(pObj.pList[0].tranDate)
    v = "\\}}v{0}.d1c".format(pObj.pList[0].tranDate)
    if(config.get('backup_options')['backup_location']['output_override'] == False):
        bkFold = iput
    else:
        bkFold = config.get('backup_options')['backup_loaction']['backup_folder']
        if(config.get('backup_options')['site_folder'] == True):
            bkFold = bkFold + pObj.pList[0].siteid
        if(config.get('backup_options')['data_folder'] == True):
            bkFold = bkFold + pObj.pList[0].tranDate
    bkFold = bkFold + "\\d1c files"
    if not os.path.exists(bkFold):
        os.makedirs(bkFold)
    shutil.move(cwd + h, bkFold + h)
    shutil.move(cwd + d, bkFold + d)
    shutil.move(cwd + v, bkFold + v)

#Loads YAML config file
def yaml_loader(filepath):
    with open(filepath, "r") as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

