import NETparse
import files
import VBparse
import yaml
import files
import os
import sys
import getopt
from datetime import datetime, timedelta
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.box import Box, MINIMAL_DOUBLE_HEAD

console = Console(color_system=None, style=None)
arguments = len(sys.argv) - 1
full_cmd_arguments = sys.argv
short_options = "h"
long_options = "headless"
argument_list=full_cmd_arguments[1:]

try:
    arguments,values = getopt.getopt(argument_list, short_options,long_options)
except getopt.error as err:
    print(str(err))
    sys.exit(2)

headless = True


def main():
    root = os.getcwd()
    dateRun = datetime.today()
    lastRunDate = files.get_lastRun_Date(root)
    log_file = f"{root}\\log.txt"

    with open(os.path.abspath(f"{root}\\config.yaml"))  as cfg:
        config_data = yaml.load(cfg, Loader=yaml.FullLoader)

    input_folders = list(config_data['input_folders'])
    output_folder = config_data.get('output_folder')
    pullMode = config_data.get('pullMode')
    SOFTWARE_VERSION = config_data.get('SOFTWARE_VERSION')

    match SOFTWARE_VERSION:
        case ("VB6"|".NET"):
            print(f"Software Version: {SOFTWARE_VERSION}")
            match headless:
                case True:
                    fileList = pullFiles(config_data,pullMode,input_folders,SOFTWARE_VERSION,dateRun,lastRunDate,log_file)
                    if fileList is not None:
                        generateSales(config_data,
                                SOFTWARE_VERSION,
                                fileList,
                                root,
                                output_folder,
                                log_file)
                case False:
                    pass
            transfer(config_data, output_folder)
            files.set_lastRun_Date(dateRun, root)  
        case _:
            print(f"Please check config. Software version set to {SOFTWARE_VERSION}, should be either '.NET' or 'VB6'")
            files.log_events(log_file,f"{dateRun}:  ERROR: incorrect software version configuration\n")
            exit(1)


def userControl():
    while True:
        table = Table(show_header=True,header_style=None, box=MINIMAL_DOUBLE_HEAD,show_lines=True, show_edge=True)
        table.add_column("#")
        table.add_column("Choice", justify="center")
        table.add_row("1", "Export specific date to sales file")
        table.add_row("2", "Export a range of dates to sales file")
        table.add_row("3", "Export all data to sales file")

        console.print(table)
        selection = Prompt.ask("Enter your selection", choices=["1","2","3"],show_choices=None, console=console)
        break


def pullFiles(config_data, pullMode, input_Folders, SOFTWARE_VERSION, dateRun, lastRunDate, log_file, userRange=None):
    fileList = []
    for folderPath in input_Folders:
        input_folder = os.path.abspath(folderPath)
        match pullMode:
            case "ALL":
                fileList = fileList + files.fileFind(input_folder,config_data,SOFTWARE_VERSION,pullMode)
            case "DAILY":
                timeDelta = (dateRun-(lastRunDate)).days
                if((timeDelta <= 1)):
                    fileList = fileList + files.fileFind(input_folder,config_data,SOFTWARE_VERSION,pullMode,(dateRun-timedelta(days=1)))
                elif(timeDelta > 1):
                    #Case when program hasn't been run in a while. Looking for any files during that time.
                    fileList = fileList + files.fileFind(input_folder,config_data,SOFTWARE_VERSION,"RANGE",(dateRun-timedelta(days=1)),lastRunDate)
            case "RANGE":
                #implement later alongside command line interface.
                pass
            case _:
                console.print(f"ERROR: Check pullMode setting in config. Must be set to 'ALL', 'DAILY', or 'RANGE'. Currently set to '{pullMode}'\n")
                files.log_events(log_file,f"{dateRun}:  ERROR: Check pullMode setting in config. Must be set to 'ALL', 'DAILY', or 'RANGE'. Currently set to '{pullMode}'\n")
                exit(1)
    if(len(fileList) == 0):
        console.print(f"ERROR: Not enough files found matching date parameters in '{input_folder}'\n")
        files.log_events(log_file,f"{dateRun}:  ERROR: Not enough files found matching date parameters in '{input_folder}'\n")
        return None
    else:
        return fileList
    

def generateSales(config_data, SOFTWARE_VERSION, fileList, root, output_folder, log_file):
    match SOFTWARE_VERSION:
        case "VB6":
            parseObj = VBparse.parse()
            for x in range(len(fileList[0])):
                parseObj.parse([fileList[0][x],fileList[1][x],fileList[2][x]])
        case ".NET":
            parseObj = NETparse.parse()
            for file in fileList:
                parseObj.parse(file)

    if(config_data.get('individual_files')):
        files.salesOutput_individual(parseObj, config_data, root, output_folder, log_file)
    else:
        files.salesOutput(parseObj, config_data, root, output_folder, log_file)


def transfer(config_data, output_folder):
    if(config_data.get('USE_EMAIL')):
        files.backupFiles(output_folder)
        files.transfer_email(output_folder,
                             config_data.get('EMAIL_Settings')['mailServer'],
                             int(config_data.get('EMAIL_Settings')['mailPort']),
                             config_data.get('EMAIL_Settings')['mailUser'],
                             config_data.get('EMAIL_Settings')['mailPassword'],
                             config_data.get('EMAIL_Settings')['messageSubject'],
                             config_data.get('EMAIL_Settings')['messageBody'],
                             config_data.get('EMAIL_Settings')['to'])            

    if(config_data.get('USE_SFTP')):
        files.backupFiles(output_folder)
        files.transfer_SFTP(output_folder,
                            config_data.get('SFTP_Settings')['Username'],
                            config_data.get('SFTP_Settings')['Password'],
                            config_data.get('SFTP_Settings')['HostName'],
                            config_data.get('SFTP_Settings')['KeyData'])


if __name__ == "__main__":
    main()