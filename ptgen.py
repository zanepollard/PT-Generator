import parse
import files

config = "config.yaml"

config_data = files.yaml_loader(config)

input_folders = config_data.get('input_folders')

files.makePT(parse.parse(input_folders[0]), config_data)


