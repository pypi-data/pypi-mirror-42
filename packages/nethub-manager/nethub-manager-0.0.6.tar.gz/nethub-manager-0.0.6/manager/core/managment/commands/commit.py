import sys
import subprocess

def commit(msg=None):

    if msg == None:
        commit_msg = input('Commit: ')
        commit_command = 'git commit -m "%s"' % (commit_msg)
        subprocess.call(commit_command, shell=True)
