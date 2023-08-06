import os
import sys
import json
import h5py
import shutil
import fileinput
import subprocess

from manager import templates
from .server_init import server_init

# Function for copy
def copy_files(name, lib_name, file_path):
    lib_name += "_template"
    template_path = templates.__path__[0] + '/' + lib_name
    shutil.copy2(template_path + name, file_path)

# Function for create empty files
def create_empty_file(file_path):
    with open(file_path, 'a'):
        os.utime(file_path, None)

# Function for replace str line
def replace_str(file_path, search_exp, replace_exp):
    for line in fileinput.input(file_path, inplace=1):
        if search_exp in line:
            line = line.replace(search_exp, replace_exp)
        sys.stdout.write(line)

# Main func
def newnet(name=None):

    if name == None:
        name = sys.argv[2]

    libs = {"netpy", "keras"}

    # print("1.NetPy\n2.Keras")
    # lib_name = input("Print your choice: ").lower()

    lib_name = 'netpy'

    if lib_name not in libs:
        print("Unknown library!")
        return False

    # Directory where project is
    top_dir = str(name)

    # Directory with metadata for project
    data_dir = top_dir+'/net_data'

    # Directory with dataset
    dataset_dir = top_dir+'/data_set'

    # File with network settings
    init_file = top_dir + '/network.py'

    # File with network settings for testing
    test_file = top_dir + '/test.py'

    # File with network settings for training
    train_file = top_dir + '/train.py'

    # File with network settings for iq testing
    iq_test_file = top_dir + '/iq_test.py'


    # Json file with project settings
    settings_file = top_dir + '/conf.json'

    # Train data set
    train_Y, train_X = dataset_dir + '/train_Y.txt', dataset_dir + '/train_X.txt'

    # Test data set
    test_Y, test_X = dataset_dir + '/test_Y.txt', dataset_dir + '/test_X.txt'


    # If path does not exist
    if not os.path.isdir(top_dir):
        os.makedirs(top_dir)
        os.makedirs(data_dir)
        os.makedirs(dataset_dir)

        create_empty_file(train_Y)
        create_empty_file(train_X)

        create_empty_file(test_Y)
        create_empty_file(test_X)

        subprocess.call("cd "+top_dir+" && git init", shell=True)

        copy_files("/network.pyt", lib_name, init_file)
        copy_files("/test.pyt", lib_name, test_file)
        copy_files("/train.pyt", lib_name, train_file)
        copy_files("/iq_test.pyt", lib_name, iq_test_file)

        settings = {
                    'name': name,
                    'data_dir': 'net_data/',
                    'library': lib_name,
                    'link': None,
                   }

        with open(settings_file, 'w') as file:
            json.dump(settings, file, indent=4)

        if lib_name == "netpy":
            meta_data = {
                     'net': {
                        'name': name,
                        'total_epoch': 0,
                        'parent': None,
                        'loss': None,

                        'arch': {
                            'layers': [],
                            'connections': []
                        },

                        'iq_test': {
                            'iq': None,
                            'iq_min': None,
                            'iq_max': None,
                            'num_of_tests': None,
                        }
                     },

                     'train_parameters': {
                        'teacher': None,
                        'learning_rate': None,
                        'error': None,
                     },

                     'description': ''
                    }

            with open(data_dir + '/arch.json', 'w') as file:
                json.dump(meta_data, file, indent=4)


                old_line = "{name}"
                new_line = "name = '" +name+ "'"

                files = [init_file, test_file, train_file, iq_test_file]

                for i in range(len(files)):
                    replace_str(files[i], old_line, new_line)

        if lib_name == "keras":
            json_path_tmp = "{json_path}"
            weights_path_tmp = "{weights_path}"

            json_path = '"' + name + "_data" + '/' + name + '.json' + '"'
            weights_path = '"' + name + "_data" + '/' + name + '.h5' + '"'

            files = [init_file, train_file, test_file]

            for i in range(len(files)):
                replace_str(files[i], json_path_tmp, json_path)
                replace_str(files[i], weights_path_tmp, weights_path)


        server_init(name)
    else:
        print("I can't create net with this name :(")
