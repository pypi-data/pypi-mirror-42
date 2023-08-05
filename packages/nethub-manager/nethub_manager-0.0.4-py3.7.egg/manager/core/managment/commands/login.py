import requests
import json
import getpass
import subprocess
import os.path

from .constants import (
    whoami,
    config_path,
)

from .graphql import token_auth_mutation

def login():

    with open(config_path, 'r') as config_file:
        config_data = json.load(config_file)
        server_adress = config_data["serverAdress"]

    username = str(input('Login: '))
    password = getpass.getpass('Password:')

    mutation = token_auth_mutation(username, password)

    response = requests.post(
        server_adress+'graphql/',
        json={
            'query': mutation
        },
    )

    if int(response.status_code) == 200:
        response_json = response.json()
        token = str(response_json['data']['tokenAuth']['token'])

        with open(config_path, 'r') as config_file:
            config_data = json.load(config_file)
            config_data['token'] = token

        with open(config_path, 'w') as config_file:
            config_file.write(json.dumps(config_data, indent=4))

        print('Login successful!')
        return True

    """
    Для тестирования, что бы не вводить логин и пароль

        # response = requests.post("http://127.0.0.1:21031/api-token-auth/",
        # data={'username': 'root', 'password': 'vaz2107top' })

        # Получаем токен
        token = response.json()
        # Получаю код состояния http
        code = int(response.status_code)
        # Если логин и пароль верны, то сохранить токен
        if code == 200:
            with open(path, 'w') as outfile:
                json.dump(token, outfile)
            print("Login successful")
            return True
        else:
            # Если логи и пароль не верны print ошибки
            str_token = json.dumps(token)
            a,b = str_token.split('"]')
            c,d = a.split('["')
            print("Error code:", code)
            print(d)
            return False
        """
