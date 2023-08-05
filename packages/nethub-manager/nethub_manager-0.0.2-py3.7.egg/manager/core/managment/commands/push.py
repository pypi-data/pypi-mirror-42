import sys
import subprocess

def push():
    subprocess.call('git push', shell=True)
