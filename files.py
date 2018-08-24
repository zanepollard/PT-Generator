import os
import shutil
import fnmatch
global siteid
global tranDate
global nDV
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

def movePumpTot():
    source = ''
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,'pump*.tot'):
            pumptot = file
            source = os.getcwd()+'\\'+pumptot