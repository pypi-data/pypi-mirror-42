import subprocess

whoami = (subprocess.check_output(['bash', '-c', 'whoami']))[:-1].decode('utf-8')
config_path = '/home/%s/.nethub_manager.json' % (whoami)
