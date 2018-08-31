import os
import shutil
import fnmatch
import yaml
import parse
import fmt

#generates the file name in standard set in config file, outputs to file
def makePT(pObj, input, config_data,root):
    
    output = os.path.abspath(config_data.get('output_folder'))
    opFolder = os.path.abspath(ptFilePath(output, config_data, pObj))
    if (config_data.get('backup_sales') == True):
        backupSales(opFolder, config_data, pObj)
    
    os.chdir(root)
    os.chdir(opFolder)

    if (config_data.get('multiDayPT') == False):
        filename = fileName(pObj,config_data, root)

        f= open(filename, "w+")
        #Outputs the data line by line to the .dat file
        for i in range(len(pObj.pList)):
            
            f.write(pObj.pList[i].siteid + pObj.pList[i].seqnum + pObj.pList[i].STATCODE + pObj.pList[i].totAmt +
                    pObj.pList[i].ACT + pObj.pList[i].TRANTYPE + pObj.pList[i].pCode + pObj.pList[i].price + 
                    pObj.pList[i].quantity + pObj.pList[i].odometer + pObj.pList[i].OID + pObj.pList[i].pump +
                    pObj.pList[i].tranNum + pObj.pList[i].tranDate + pObj.pList[i].tranTime + pObj.pList[i].FILL +
                    pObj.pList[i].vehicle + pObj.pList[i].id_card + pObj.pList[i].PART_ID + pObj.pList[i].id_acct +
                    pObj.pList[i].id_vehicle + pObj.pList[i].END + "\n")
            '''
            f.write(pObj.pList[i].siteid + " " + pObj.pList[i].seqnum + " " + pObj.pList[i].STATCODE + " " + pObj.pList[i].totAmt + " " +
                    pObj.pList[i].ACT + " " + pObj.pList[i].TRANTYPE + " " + pObj.pList[i].pCode + " " + pObj.pList[i].price + " " + 
                    pObj.pList[i].quantity + " " + pObj.pList[i].odometer + " " + pObj.pList[i].OID + " " + pObj.pList[i].pump + " " +
                    pObj.pList[i].tranNum + " " + pObj.pList[i].tranDate + " " + pObj.pList[i].tranTime + " " + pObj.pList[i].FILL + " " +
                    pObj.pList[i].vehicle + " " + pObj.pList[i].id_card + " " + pObj.pList[i].PART_ID + " " + pObj.pList[i].id_acct + " " +
                    pObj.pList[i].id_vehicle + " " + pObj.pList[i].END + "\n")
            '''
        f.close()
    else:
        print("why")
        end = len(pObj) - 1
        filename = fileName(pObj[end], config_data, root)
        for i in pObj:
            f= open(filename, "w+")
            #Outputs the data line by line to the .dat file
            for j in pObj:
                for k in j.pList:
                    f.write(k.siteid + k.seqnum + k.STATCODE + k.totAmt +
                            k.ACT + k.TRANTYPE + k.pCode + k.PRICE + 
                            k.quantity + k.odometer + k.OID + k.pump +
                            k.tranNum + k.tranDate + k.tranTime + k.FILL +
                            k.id_vehicle + k.id_card + k.PART_ID + k.id_acct +
                            k.vehicle + k.END + "\n")

def fileName(pObj,config_data, root):
    filename = ''
    os.chdir(root)
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
    return filename + config_data.get('file_name')['extension']

#Generates path PT file will be generated to according to options seet in config
def ptFilePath(output, config, pObj):
    ptLoc = output
    if(config.get('multiDayPT') == False):
        if(config.get('output_options')['site_folder'] == True):
            ptLoc = ptLoc + "\\" + pObj.pList[0].siteid
        if(config.get('output_options')['date_folder'] == True):
            ptLoc = ptLoc + "\\" + pObj.pList[0].tranDate
        if not os.path.exists(ptLoc):
            os.makedirs(ptLoc)
        if (config.get('pump_total') == True):
            movePumpTot(ptLoc, config, output)
    else:
        end = len(pObj) - 1
        for __ in pObj:
            if(config.get('output_options')['site_folder'] == True):
                ptLoc = ptLoc + "\\" + pObj[end].pList[0].siteid
            if(config.get('output_options')['date_folder'] == True):
                ptLoc = ptLoc + "\\" + pObj[end].pList[0].tranDate
            if not os.path.exists(ptLoc):
                os.makedirs(ptLoc)
            if (config.get('pump_total') == True):
                movePumpTot(ptLoc, config, output)
    return ptLoc

#moves pump total file if specified by YAML
def movePumpTot(iput, config, output):
    #cwd = os.getcwd()
    os.chdir(output)
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,'pump*.tot'):
            pumptot = file
            shutil.move(output + "\\" + pumptot, iput + "\\"+ pumptot)

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
    bkFold = os.path.abspath(bkFold + "\\d1c files")
    if not os.path.exists(bkFold):
        os.makedirs(bkFold)
    shutil.move(cwd + h, bkFold + h)
    shutil.move(cwd + d, bkFold + d)
    shutil.move(cwd + v, bkFold + v)

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
        print("some sales files missing!")
        exit()
    return [h,d,v]


#Loads YAML config file
def yaml_loader(filepath):
    with open(filepath, "r") as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

