import NETparse
import files
import VBparse
import yaml
import files
import os
import sys
import getopt
import re
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
if "-h" in argument_list:
    headless = True
else:
    headless = False


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
                    fileList = pullFiles(config_data,pullMode,input_folders,SOFTWARE_VERSION,log_file,dateRun,lastRunDate)      
                    files.set_lastRun_Date(dateRun, root)
                case False:
                    fileList = userControl(config_data,input_folders,SOFTWARE_VERSION,log_file)
            if fileList is not None: 
                generateSales(config_data,
                        SOFTWARE_VERSION,  
                        fileList,
                        root,
                        output_folder,
                        log_file)
                if headless:
                    transfer(config_data,output_folder,log_file,dateRun)
                else:
                    Prompt.ask(f"Files output to {output_folder}. Press ENTER to continue...", console=console)
            else:
                if headless:
                    Prompt.ask(f"Exiting. Press ENTER to continue...", console=console)
            
        case _:
            print(f"Please check config. Software version set to {SOFTWARE_VERSION}, should be either '.NET' or 'VB6'")
            files.log_events(log_file,f"{dateRun}:  ERROR: incorrect software version configuration\n")
            exit(1)
    

    

def userControl(config_data,input_Folders,SOFTWARE_VERSION,log_file):
    while True:
        table = Table(show_header=True,header_style=None, box=MINIMAL_DOUBLE_HEAD,show_lines=True, show_edge=True)
        table.add_column("#")
        table.add_column("Choice", justify="center")
        table.add_row("1", "Export specific date to sales file")
        table.add_row("2", "Export a range of dates to sales file")
        table.add_row("3", "Export all data to sales file")
        table.add_row("4", "Exit")

        console.print(table)

        match Prompt.ask("Enter your selection", choices=["1","2","3","4"],show_choices=None, console=console):
            case "1":
                input_date = Prompt.ask("Please enter the date in MM-DD-YYYY format (EX: 01-01-2001)", console=console)
                if re.match(r"(0[1-9]|1[012])[- \/.](0[1-9]|[12][0-9]|3[01])[- \/.]\d{4}",input_date):
                    try:
                        date = datetime(int(input_date[6:10]),int(input_date[0:2]),int(input_date[3:5]))
                    except ValueError:
                        console.print(f"\nUser entered value of {input_date} is not a real date. Date must be in MM-DD-YYYY format.\n")
                        Prompt.ask("Press ENTER to continue...", console=console)
                    else:
                        return pullFiles(config_data,"RANGE",input_Folders,SOFTWARE_VERSION,log_file,date,date)
                else:
                    console.print(f"\nUser entered value of {input_date} invalid. Date must be in MM-DD-YYYY format\n")
                    Prompt.ask("Press ENTER to continue...", console=console)
            case "2":
                try:
                    start_input_date = Prompt.ask("Please enter the start date in MM-DD-YYYY format (EX: 01-01-2001)", console=console)
                    if re.match(r"(0[1-9]|1[012])[- \/.](0[1-9]|[12][0-9]|3[01])[- \/.]\d{4}",start_input_date):
                        try:
                            start_date = datetime(int(start_input_date[6:10]),int(start_input_date[0:2]),int(start_input_date[3:5]))
                        except ValueError:
                            console.print(f"\nUser entered value of {start_input_date} is not a real date. Date must be in MM-DD-YYYY format.\n")
                            Prompt.ask("Press ENTER to continue...", console=console)
                    else:
                        console.print(f"\nUser entered value of {start_input_date} invalid. Date must be in MM-DD-YYYY format\n")
                        Prompt.ask("Press ENTER to continue...", console=console)
                    end_input_date = Prompt.ask("Please enter the end date in MM-DD-YYYY format (EX: 01-01-2001)", console=console)
                    if re.match(r"(0[1-9]|1[012])[- \/.](0[1-9]|[12][0-9]|3[01])[- \/.]\d{4}",end_input_date):
                        try:
                            end_date = datetime(int(end_input_date[6:10]),int(end_input_date[0:2]),int(end_input_date[3:5]))
                        except ValueError:
                            console.print(f"\nUser entered value of {end_input_date} is not a real date. Date must be in MM-DD-YYYY format.\n")
                            Prompt.ask("Press ENTER to continue...", console=console)
                    else:
                        console.print(f"\nUser entered value of {end_input_date} invalid. Date must be in MM-DD-YYYY format\n")
                        Prompt.ask("Press ENTER to continue...", console=console)
                except Exception:
                    print("An error Occurred")
                else:
                    #Technically either way is a range of dates. No point in forcing purely a start and end date
                    if(end_date-start_date).days > 0:
                        return pullFiles(config_data,"RANGE",input_Folders,SOFTWARE_VERSION,log_file,end_date,start_date)
                    else:
                        return pullFiles(config_data,"RANGE",input_Folders,SOFTWARE_VERSION,log_file,start_date,end_date)
            case "3":
                return pullFiles(config_data,"ALL",input_Folders,SOFTWARE_VERSION,log_file)
            case "4":
                Prompt.ask("Exiting... Press ENTER to continue...", console=console)
                break


def pullFiles(config_data, pullMode, input_Folders, SOFTWARE_VERSION,log_file, recentDate=None, pastDate=None):
    fileList = []
    for folderPath in input_Folders:
        input_folder = os.path.abspath(folderPath)
        match pullMode:
            case "ALL":
                fileList = fileList + files.fileFind(input_folder,config_data,SOFTWARE_VERSION,pullMode)
            case "DAILY":
                timeDelta = (recentDate-(pastDate)).days
                if((timeDelta <= 1)):
                    fileList = fileList + files.fileFind(input_folder,config_data,SOFTWARE_VERSION,pullMode,(recentDate-timedelta(days=1)))
                else:
                    #Case when program hasn't been run in a while. Looking for any files during that time.
                    
                    fileList = fileList + files.fileFind(input_folder,config_data,SOFTWARE_VERSION,"RANGE",(recentDate-timedelta(days=1)),pastDate)
            case "RANGE":
                fileList = fileList + files.fileFind(input_folder,config_data,SOFTWARE_VERSION,"RANGE",recentDate,pastDate)
            case _:
                console.print(f"ERROR: Check pullMode setting in config. Must be set to 'ALL', 'DAILY', or 'RANGE'. Currently set to '{pullMode}'\n")
                files.log_events(log_file,f"{recentDate}:  ERROR: Check pullMode setting in config. Must be set to 'ALL', 'DAILY', or 'RANGE'. Currently set to '{pullMode}'\n")
                exit(1)
    if(len(fileList) == 0):
        console.print(f"ERROR: Not enough files found matching date parameters in '{input_folder}'\n")
        files.log_events(log_file,f"{recentDate}:  ERROR: Not enough files found matching date parameters in '{input_folder}'\n")
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


def transfer(config_data, output_folder,log_file,dateRun):
    if(config_data.get('USE_EMAIL')):
        print(config_data['EMAIL_Settings'])
        for key in config_data['EMAIL_Settings']:
            if config_data['EMAIL_Settings'][key] == None:
                files.log_events(log_file,f"{dateRun}:  ERROR: Please verify Email configuration. Required settings are missing.\n")
                break
        files.backupFiles(output_folder)
        try:
            files.transfer_email(output_folder,
                                config_data.get('EMAIL_Settings')['mailServer'],
                                int(config_data.get('EMAIL_Settings')['mailPort']),
                                config_data.get('EMAIL_Settings')['mailUser'],
                                config_data.get('EMAIL_Settings')['mailPassword'],
                                config_data.get('EMAIL_Settings')['messageSubject'],
                                config_data.get('EMAIL_Settings')['messageBody'],
                                config_data.get('EMAIL_Settings')['to'])
        except Exception:
            files.log_events(log_file,f"{dateRun}:  ERROR: Email transfer failed. Please verify configuration.\n")                        

    if(config_data.get('USE_SFTP')):
        for key in config_data['SFTP_Settings']:
            if config_data['SFTP_Settings'][key] == None:
                files.log_events(log_file,f"{dateRun}:  ERROR: Please verify SFTP configuration. Required settings are missing.\n")
                break
        files.backupFiles(output_folder)
        try:
            files.transfer_SFTP(output_folder,
                                config_data.get('SFTP_Settings')['Username'],
                                config_data.get('SFTP_Settings')['Password'],
                                config_data.get('SFTP_Settings')['HostName'],
                                config_data.get('SFTP_Settings')['KeyData'])
        except Exception:
            files.log_events(log_file,f"{dateRun}:  ERROR: SFTP transfer failed. Please verify configuration.\n")   


if __name__ == "__main__":
    main()