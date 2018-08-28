import parse
import files
import os

config = "config.yaml"
config_data = files.yaml_loader(config)

input_folders = config_data.get('input_folders')
cwd = os.getcwd()
for i in input_folders:
    temp = parse.parse()
    files.makePT(temp.parse(os.path.abspath(i)), i, config_data)
    os.chdir(cwd)