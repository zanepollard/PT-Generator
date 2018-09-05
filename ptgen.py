import parse 
import files
import os
from datetime import datetime
startTime = datetime.now()
config = "config.yaml"
config_data = files.yaml_loader(config)



input_folders = config_data.get('input_folders')
cwd = os.getcwd()
pt = []
temp = parse.parse()
#temp.vTwo() 

for i in input_folders:
    folder = os.path.abspath(i)
    f = files.fileFind(folder)
    if config_data.get('multiDayPT') == False: 
        for x in range(len(f[0])):
            temp = parse.parse()
            pt.append(temp.parse(folder, [f[0][x],f[1][x],f[2][x]], config_data))
    else:
        temp = parse.parse()
        pt.append(temp.parse(folder, f, config_data))
    for q in pt:
        os.chdir(cwd)
        files.makePT(q, i,config_data,cwd)
        del q #??
    
    os.chdir(cwd)
print(datetime.now() - startTime)