import sys
import subprocess


def add(file=None):

    if file==None:
        file = sys.argv[2]

    subprocess.call('git add %s' % (file), shell=True)
