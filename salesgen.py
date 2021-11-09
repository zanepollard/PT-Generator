import shutil
import NETparse
import files
import VBparse
import yaml
import files
import os
from datetime import datetime, timedelta

def main():
    root = os.getcwd()
    dateRun = datetime.today()
    lastRunDate = files.get_lastRun_Date(root)

    with open(os.path.abspath(root + "\\config.yaml"))  as cfg:
        config_data = yaml.load(cfg, Loader=yaml.FullLoader)

    fileList = []
    input_folders = list(config_data['input_folders'])
    output_folder = config_data.get('output_folder')
    pullMode = config_data.get('pullMode')
    SOFTWARE_VERSION = config_data.get('SOFTWARE_VERSION')


    for folderPath in input_folders:
        currentFolder = os.path.abspath(folderPath)
        if(pullMode == "ALL"):
            fileList = files.fileFind(currentFolder, SOFTWARE_VERSION, pullMode)
        elif(pullMode == "DAILY"):
            timeDelta = (dateRun - (lastRunDate)).days
            if((timeDelta <= 1)):
                fileList = files.fileFind(currentFolder, SOFTWARE_VERSION, pullMode, (dateRun - timedelta(days=1)))
            elif(timeDelta > 1):
                #Case when program hasn't been run in a while. Looking for any files during that time.
                fileList = files.fileFind(currentFolder, SOFTWARE_VERSION, "RANGE", (dateRun - timedelta(days=1)), lastRunDate)
        elif(pullMode == "RANGE"):
            #implement later alongside command line interface.
            pass
        os.chdir(root)
        if(len(fileList) == 0):
            print("No files found to parse matching date parameters. Exiting...")
            exit()
        if(SOFTWARE_VERSION == "VB6"):
            parseObj = VBparse.parse()
            for x in range(len(fileList[0])):
                parseObj.parse(currentFolder, [fileList[0][x],fileList[1][x],fileList[2][x]], config_data)
        elif(SOFTWARE_VERSION == ".NET"):
            parseObj = NETparse.parse()
            for file in fileList:
                parseObj.parse(currentFolder, file, config_data)

        files.salesOutput(parseObj, config_data, root, output_folder)
        files.set_lastRun_Date(dateRun, root)

        if(config_data.get('USE_EMAIL')):
            os.chdir(output_folder)
            backupFolder = os.path.abspath(output_folder + "/backup")
            if not (os.path.isdir(backupFolder)):
                os.mkdir(backupFolder)
            for file in os.listdir(output_folder):
                shutil.copyfile(os.path.abspath(output_folder + "/" + file), os.path.abspath(backupFolder + "/" + file))
            

        if(config_data.get('USE_SFTP')):
            pass


if __name__ == "__main__":
    main()