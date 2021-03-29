import parse 
import files
import os
import yaml
import shutil
from pathlib import Path
from datetime import datetime


startTime = datetime.now()
config_data = None
with open('config.yaml') as cfg:
    config_data = yaml.load(cfg, Loader=yaml.FullLoader)

fileList = []
input_folders = list(config_data['input_folders'])
pullMode = config_data.get('pullMode')
cwd = os.getcwd()
root = os.getcwd()
pt = []
temp = parse.parse()

for folderPath in input_folders:
    fCount = 0
    folder = os.path.abspath(folderPath)
    f = files.fileFind(folder, pullMode)
    fileList.append(f)
    if config_data.get('multiDayPT') == False:  
        for x in range(len(f[0])):
            temp = None
            temp = parse.parse()
            pt.append(temp.parse(folder, [f[0][x],f[1][x],f[2][x]], config_data))
    else:
        os.chdir(root)
        temp = parse.parse()
        pt.append(temp.parse(folder, f, config_data))

    for q in pt:
        os.chdir(cwd)
        files.salesOutput(q, config_data,cwd)
    os.chdir(cwd)


if(config_data.get('USE_SFTP') == True):
    os.chdir(root)
    SFTPusername = config_data.get('SFTP_Settings')['Username']
    SFTPpassword = config_data.get('SFTP_Settings')['Password']
    SFTPhostname = config_data.get('SFTP_Settings')['HostName']
    KeyData = config_data.get('SFTP_Settings')['KeyData']
    if not os.path.exists(root + '\\sftpQueue'):
        os.makedirs(root + '\\sftpQueue')
    os.chdir('sftpQueue')
    for salesFile in os.listdir(".\\"):
        print("Transferring " + salesFile + " to SFTP server")
        files.transfer_SFTP(salesFile, SFTPusername, SFTPpassword, SFTPhostname, KeyData)
