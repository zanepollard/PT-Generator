import parse 
import files
import os
import yaml
from pathlib import Path
from datetime import datetime


startTime = datetime.now()
config_data = None
with open('config.yaml') as cfg:
    config_data = yaml.load(cfg, Loader=yaml.FullLoader)


input_folders = list(config_data['input_folders'])
pullMode = config_data.get('pullMode')
cwd = os.getcwd()
pt = []
temp = parse.parse()

for i in input_folders:
    fCount = 0
    folder = os.path.abspath(i)
    for file in os.listdir(Path(i)):
        if len(file)>4:
            if file[len(file)-4:len(file)] != ".log":
                fCount += 1
    if((fCount%3)==0):
        f = files.fileFind(folder, pullMode)
        if config_data.get('multiDayPT') == False:  
            for x in range(len(f[0])):
                temp = None
                temp = parse.parse()
                pt.append(temp.parse(folder, [f[0][x],f[1][x],f[2][x]], config_data))
        else:
            temp = parse.parse()
            pt.append(temp.parse(folder, f, config_data))

        for q in pt:
            os.chdir(cwd)
            files.salesOutput(q, config_data,cwd)
        os.chdir(cwd)
    else:
        eName = i + "\\{0}.log".format(datetime.date(datetime.now()))
        log = open(eName, 'a+')
        log.write("Not enough files in " + i + " to make a pt file")