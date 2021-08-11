import parse
import yaml
import files
import os
from datetime import datetime

pOBJ = parse.parse()
cwd = os.getcwd()
root = os.getcwd()
config_data = None
with open(os.path.abspath(root + "\\config.yaml"))  as cfg:
    config_data = yaml.load(cfg, Loader=yaml.FullLoader)
    print(config_data)

fileList = []
input_folders = list(config_data['input_folders'])
pullMode = config_data.get('pullMode')

tranSets = []
temp = parse.parse()

for folderPath in input_folders:
    folder = os.path.abspath(folderPath)
    

    for file in files.fileFind(folder, pullMode):
        pOBJ = None
        pOBJ = parse.parse()
        tranSets.append(pOBJ.parse(folder, file))
    
    for set in tranSets:
        os.chdir(cwd)
        files.salesOutput(set, config_data, cwd)