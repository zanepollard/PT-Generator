import os
import shutil
import fnmatch
import yaml
import parse
import fmt

def fileIO(pList):
    
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
    pumptotN = os.getcwd() + '\\' + pumptot
    shutil.move(source, pumptotN)
    f= open("pt{0}.dat".format(ptFileName),"w+")
    #Outputs the data line by line to the .dat file
    for i in range(runCount):
        f.write(check(siteid,6,"SiteId") + check(seqnum[i],4,"seqNum") + STATCODE + check(totAmt[i],6,"TotAMT") + 
        ACT + TRANTYPE + check(pCode[i],2,"pCode") + PRICE + check(quantity[i],8,"quantity") + 
        check(odometer[i],7,"odometer") + OID + check(pump[i],2,"pump#") + check(tranNum[i],4,"trans #") + check(tranDate,6,"trandate") + 
        check(tranTime[i],4,"Trantime") + FILL + check(id_vehicle[i],8,"vehicle id") + check(id_card[i],7,"id_card") + 
        PART_ID + check(id_acct[i],6,"id_acct") + check(vehicle[i],4,"vehicle") + END + "\n")
    f.close()
    ptFile= ''
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,'pt*.dat'):
            filename = file
            ptFile = os.getcwd()+'\\'+filename
    os.chdir("..") 
    os.chdir("..")
    cwd = os.getcwd()
    dest = os.getcwd() + '\\{0}\\{1}\\d1c files\\'.format(siteid,tranDate)
    h = "\\}}h{0}.d1c".format(tranDate)
    d = "\\}}d{0}.d1c".format(tranDate)
    v = "\\}}v{0}.d1c".format(tranDate)
    shutil.move(cwd + h, dest + h)
    shutil.move(cwd + d, dest + d)
    shutil.move(cwd + v, dest + v)

def makePT(pObj, input, config_data):
    filename = ''
    output = config_data.get('output_folder')
    
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
    
    os.chdir(output)
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


def movePumpTot(input):
    source = ''
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,'pump*.tot'):
            pumptot = file
            source = os.getcwd()+'\\'+pumptot

def backupSales(input):
    pass

def yaml_loader(filepath):
    with open(filepath, "r") as file_descriptor:
        data = yaml.load(file_descriptor)
    return data