import sys
import json
import requests
import subprocess

from .login import login
from .graphql import create_project_mutation

from .constants import (
    whoami,
    config_path,
)

def server_init(title=None):
    if title==None:
        title = sys.argv[2]


    with open(config_path, "r") as config_file:
        config_data = json.load(config_file)
        token = config_data["token"]

    if token == None:
        login()

    conf_net_path = title+"/conf.json"

    with open(config_path, "r") as config_file:
        config_data = json.load(config_file)
        token = config_data["token"]
        server_adress = config_data["serverAdress"]

    token = 'jwt {}'.format(token)

    with open(conf_net_path, "r") as net_conf:
        json_data = json.load(net_conf)
        name = json_data["name"]
        lib_name = json_data["library"]

    mutation = create_project_mutation(name, lib_name)

    response = requests.post(
        server_adress+'graphql/',
        json={
            'query': mutation
        },
        headers={
            'Authorization': token
        },
    )

    code = int(response.status_code)

    if code == 200:
        response_json = response.json()
        git_adress = response_json['data']['createProject']['project']['gitAddress']

        remote_add_origin_command = 'cd %s && git remote add origin %s'
        commit_command = 'cd %s && git add . && git commit -m "%s"'
        push_command = 'cd %s && git push -u origin master'

        commit_msg = input('Commit: ')

        subprocess.call(remote_add_origin_command % (title, git_adress), shell=True)
        subprocess.call(commit_command % (title, commit_msg), shell=True)
        subprocess.call(push_command % (title), shell=True)

        with open(title+"/conf.json", 'r') as conf:
            json_data = json.load(conf)
            json_data["link"] = git_adress

        with open(title+"/conf.json", 'w') as conf:
            json.dump(json_data, conf, indent=4)

        return True
    else:
        print(response.content)
        return False
