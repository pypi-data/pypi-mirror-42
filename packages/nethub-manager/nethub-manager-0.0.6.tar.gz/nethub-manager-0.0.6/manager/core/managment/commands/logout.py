import os
import subprocess

def logout():
    whoami = (subprocess.check_output(['bash','-c','whoami']))[:-1]
    whoami = whoami.decode("utf-8")
    path = ("/home/"+whoami+"/.nethub_token.json")

    if os.path.isfile(path):
        os.remove(path)
        return True

