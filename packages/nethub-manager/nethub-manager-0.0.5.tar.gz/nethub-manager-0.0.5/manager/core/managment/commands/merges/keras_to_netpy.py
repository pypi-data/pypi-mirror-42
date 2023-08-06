import os
import sys
import h5py
import json
import numpy as np

def keras_to_netpy_merge(netpy_net, keras_net):

    with open(netpy_net+'/'+netpy_net+'_data/'+netpy_net+'.json', 'r') as master:
        master_data = json.load(master)
        num_of_master_layers = len(master_data['net']['arch']['layers'])
        num_of_master_connections = len(master_data['net']['arch']['connections'])
        num_of_master_in_neurons = master_data['net']['arch']['layers'][0]['num_of_neurons']
        num_of_master_modules = num_of_master_layers + num_of_master_connections

    with open(keras_net+'/'+keras_net+'_data/'+keras_net+'.json', 'r') as second:
        second_data = json.load(second)
        num_of_second_layers = len(second_data["config"])
        num_of_second_in_neurons = second_data["config"][0]["config"]["batch_input_shape"][1]
        name_of_second_in_layer = second_data["config"][0]["config"]["name"]
        name_of_second_hid_layer = second_data["config"][1]["config"]["name"]
    
    if num_of_master_layers != num_of_second_layers+1:
        print('Non-valid architecture')
        return False
    elif num_of_master_in_neurons != num_of_second_in_neurons:
        print('Non-valid architecture')
    else:
        netpy_weights = h5py.File(netpy_net+'/'+netpy_net+'_data/'+netpy_net+'.h5', 'r+')
        keras_weights = h5py.File(keras_net+'/'+keras_net+'_data/'+keras_net+'.h5', 'r')

        current_master_weights = netpy_weights['weights_0_2'][:]
        current_second_weights = keras_weights[name_of_second_in_layer][name_of_second_in_layer]["kernel:0"][:]

        cur_master_line = len(current_master_weights)
        cur_master_col = len(current_master_weights[0])
        cur_second_line = len(current_second_weights)
        cur_second_col = len(current_second_weights[0])

        current_master_weights = np.append(current_master_weights, current_second_weights, axis=1)

        netpy_weights['weights_0_2'].resize((cur_master_line, cur_master_col+cur_second_col))
        netpy_weights['weights_0_2'][:] = current_master_weights

        current_master_weights = netpy_weights['weights_2_4'][:]
        current_second_weights = keras_weights[name_of_second_hid_layer][name_of_second_hid_layer]["kernel:0"]

        cur_master_line = len(current_master_weights)
        cur_master_col = len(current_master_weights[0])
        cur_second_line = len(current_second_weights)
        cur_second_col = len(current_second_weights[0])

        right_top_matrix = np.zeros((cur_master_line, cur_second_col))
        left_bot_matrix = np.zeros((cur_second_line, cur_master_col))

        current_master_weights = np.append(current_master_weights, right_top_matrix, axis=1)
        bottom_matrix = np.append(left_bot_matrix, current_second_weights, axis=1)

        current_master_weights = np.vstack((current_master_weights, bottom_matrix))

        netpy_weights['weights_2_4'].resize((cur_master_line+cur_second_line,
                                             cur_master_col+cur_second_col))

        netpy_weights['weights_2_4'][:] = current_master_weights

    netpy_weights.close()
    keras_weights.close()

    with open(netpy_net+'/'+netpy_net+'_data/'+netpy_net+'.json', 'r') as log:
        json_data = json.load(log)
        json_data['net']['arch']['layers'][-2]['num_of_neurons'] = len(current_master_weights)
        json_data['net']['arch']['layers'][-1]['num_of_neurons'] = len(current_master_weights[0])

    with open(netpy_net+'/'+netpy_net+'_data/'+netpy_net+'.json', 'w') as log:
        log.write(json.dumps(json_data, indent=4))
