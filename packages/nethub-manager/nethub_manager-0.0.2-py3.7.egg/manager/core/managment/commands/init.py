import json
import subprocess

from .login import login
from .constants import (
    whoami,
    config_path,
)

def init():
    config = {
        'serverAdress': None,
        'gitServerAdress': None,
        'token': None,
        'nets': []
    }

    server_adress = input("Server adress (default: 'http://127.0.0.1:21020/'): ")

    if server_adress == '':
        server_adress = 'http://127.0.0.1:21020/'

    git_server_adress = server_adress[:-2]+'6/'

    config['serverAdress'] = server_adress
    config['gitServerAdress'] = git_server_adress

    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=4)

    # login()
