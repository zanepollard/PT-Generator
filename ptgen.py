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



gasboy = bool(config_data['gasboyOutput'])
csvOutput = bool(config_data['csvOutput'])
input_folders = list(config_data['input_folders'])
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
    if fCount>=3:
        f = files.fileFind(folder)
        if config_data.get('multiDayPT') == False:  
            for x in range(len(f[0])):
                temp = None
                temp = parse.parse()
                pt.append(temp.parse(folder, [f[0][x],f[1][x],f[2][x]], config_data))
        else:
            temp = parse.parse()
            pt.append(temp.parse(folder, f, config_data))

        lTemp = None
        for q in pt:
            os.chdir(cwd)
            if not gasboy and not csvOutput:
                files.makePT(q, config_data,cwd)
            lTemp = q
        if gasboy:
            files.makePT(lTemp, config_data,cwd)
        if csvOutput:
            files.makeCSV(q, config_data, cwd)
        os.chdir(cwd)
    else:
        eName = i + "\\{0}.log".format(datetime.date(datetime.now()))
        log = open(eName, 'a+')
        log.write("Not enough files in " + i + " to make a pt file")