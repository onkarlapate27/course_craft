import yaml
import os

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yml')
    with open(config_path, 'r') as file:
        config_data = yaml.safe_load(file)
    return config_data

settings = load_config()