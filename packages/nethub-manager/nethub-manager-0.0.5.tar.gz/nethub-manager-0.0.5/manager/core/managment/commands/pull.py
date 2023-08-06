import sys
import subprocess

def pull():
    subprocess.call('git pull', shell=True)
