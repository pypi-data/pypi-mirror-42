import os
import sys
import json
import shutil

from .newnet import newnet, replace_str
from distutils.dir_util import copy_tree


def copy_file(first_net, second_net ,file_name):
    shutil.copy2(first_net+'/'+file_name, second_net+'/'+file_name)

def path_to_h5_file(netname):
    return netname+'/'+netname+'_data/'+netname+'.h5'

def fork():
    first_net = sys.argv[2]
    second_net = sys.argv[3]

    if not os.path.isdir(first_net):
        print("Can't find net with this name :(")
    elif os.path.isdir(second_net):
        print("Net with name %s already exist!" % (second_net))
    else:

        if not os.path.isdir(second_net):
            newnet(str(second_net))

            copy_file(first_net, second_net, 'network.py')
            copy_file(first_net, second_net, 'test.py')
            copy_file(first_net, second_net, 'train.py')
            copy_file(first_net, second_net, 'iq_test.py')

            files = [
                '/network.py',
                '/test.py',
                '/train.py',
                '/iq_test.py',
            ]

            old_line = "net = FeedForwardNet(name = '" +first_net+"')"
            new_line = "net = FeedForwardNet(name = '" +second_net+"')"

            for i in range(len(files)):
                replace_str(second_net+files[i], old_line, new_line)

            copy_tree(first_net+'/data_set', second_net+'/data_set')

            if os.path.isfile(path_to_h5_file(first_net)):
                shutil.copy2(
                    path_to_h5_file(first_net),
                    path_to_h5_file(second_net)
                )

            shutil.copy2(
                first_net+'/'+first_net+'_data/'+first_net+'.json',
                second_net+'/'+second_net+'_data/parent_data.json'
            )

            shutil.copy2(
                first_net+'/'+first_net+'_data/'+first_net+'.json',
                second_net+'/'+second_net+'_data/'+second_net+'.json'
            )


            with open(second_net+'/'+second_net+'_data/'+second_net+'.json', 'r') as log:
                json_data = json.load(log)
                json_data['net']['name'] = second_net
                json_data['net']['total_epoch'] = 0
                json_data['net']['parent'] = first_net
                json_data['net']['loss'] = 0
                json_data['net']['iq_test']['iq'] = 0
                json_data['net']['iq_test']['iq_min'] = 0
                json_data['net']['iq_test']['iq_max'] = 0
                json_data['net']['iq_test']['num_of_tests'] = 0

                json_data['train_parameters']['teacher'] = None
                json_data['train_parameters']['learning_rate'] = None
                json_data['train_parameters']['error'] = None

            with open(second_net+'/'+second_net+'_data/'+second_net+'.json', 'w') as log:
                log.write(json.dumps(json_data, indent=4))
