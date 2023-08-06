import os
import sys
import json
import importlib


def merge():
    master_net = sys.argv[2]
    second_net = sys.argv[3]

    if not os.path.isdir(master_net):
        print("Can't find net with name %s" % (master_net))
    elif not os.path.isdir(second_net):
        print("Can't find net with name %s" % (second_net))
    else:

        with open(master_net+'/conf.json', 'r') as master_conf:
            master_data = json.load(master_conf)
            master_lib = master_data["library"]

        with open(second_net+'/conf.json', 'r') as second_conf:
            second_data = json.load(second_conf)
            second_lib = second_data["library"]

        print("Merge " + second_lib + " to " + master_lib)

        function = second_lib + '_to_' + master_lib + '_merge'
        module = importlib.import_module("manager.core.managment.commands.merges")
        merge = getattr(module , function)


        merge(master_net, second_net)

        print('Successfully merge %s -> %s' % (second_net, master_net))

