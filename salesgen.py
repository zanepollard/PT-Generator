import shutil

from rich.padding import Padding
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
from rich.style import Style

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


def main():
    root = os.getcwd()
    dateRun = datetime.today()
    lastRunDate = files.get_lastRun_Date(root)

    with open(os.path.abspath(f"{root}\\config.yaml"))  as cfg:
        config_data = yaml.load(cfg, Loader=yaml.FullLoader)

    fileList = []
    input_folders = list(config_data['input_folders'])
    output_folder = config_data.get('output_folder')
    pullMode = config_data.get('pullMode')
    SOFTWARE_VERSION = config_data.get('SOFTWARE_VERSION')




    for folderPath in input_folders:
        currentFolder = os.path.abspath(folderPath)
        if(pullMode == "ALL"):
            fileList = files.fileFind(currentFolder,config_data,SOFTWARE_VERSION,pullMode)
        elif(pullMode == "DAILY"):
            timeDelta = (dateRun-(lastRunDate)).days
            if((timeDelta <= 1)):
                fileList = files.fileFind(currentFolder,config_data,SOFTWARE_VERSION,pullMode,(dateRun-timedelta(days=1)))
            elif(timeDelta > 1):
                #Case when program hasn't been run in a while. Looking for any files during that time.
                fileList = files.fileFind(currentFolder,config_data,SOFTWARE_VERSION,"RANGE",(dateRun-timedelta(days=1)),lastRunDate)
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
        #files.salesOutput_ind(parseObj, config_data, root, output_folder)
        files.salesOutput(parseObj, config_data, root, output_folder)
        files.set_lastRun_Date(dateRun, root)

        if(config_data.get('USE_EMAIL')):
            files.backupFiles(output_folder)
            #TODO!             

        if(config_data.get('USE_SFTP')):
            files.backupFiles(output_folder)
            #TODO!


def userControl():
    while True:
        table = Table(show_header=True,header_style=None, box=MINIMAL_DOUBLE_HEAD,show_lines=True, show_edge=True)
        table.add_column("#")
        table.add_column("Choice", justify="center")
        table.add_row("1", "Export specific date to sales file")
        table.add_row("2", "Export a range of dates to sales file")

        console.print(table)
        selection = Prompt.ask("Enter your selection", choices=["1","2"],show_choices=None, console=console)
        break


if __name__ == "__main__":
    main()