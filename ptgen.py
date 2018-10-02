import parse 
import files
import os
from datetime import datetime
startTime = datetime.now()
config = "config.yaml"
config_data = files.yaml_loader(config)


gasboy = config_data.get('gasboyOutput')
input_folders = config_data.get('input_folders')
cwd = os.getcwd()
pt = []
temp = parse.parse()
#temp.vTwo() 

for i in input_folders:
    print(i)
    fCount = 0
    folder = os.path.abspath(i)
    print(os.listdir(i))
    for file in os.listdir(i):
        if len(file)>4:
            if file[len(file)-4:len(file)] != ".log":
                fCount += 1
    if fCount>=3:
        f = files.fileFind(folder)
        print(f)
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
            if not gasboy:
                files.makePT(q, config_data,cwd)
            lTemp = q
        if gasboy:
            files.makePT(lTemp, config_data,cwd)
        os.chdir(cwd)
    else:
        eName = i + "\\{0}.log".format(datetime.date(datetime.now()))
        log = open(eName, 'a+')
        log.write("Not enough files in " + i + " to make a pt file")
print(datetime.now() - startTime)