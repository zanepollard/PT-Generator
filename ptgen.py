import parse
import files

config = "config.yaml"
config_data = files.yaml_loader(config)

input_folders = config_data.get('input_folders')

for i in input_folders:
    temp = parse.parse()
    files.makePT(temp.parse(i), config_data)


