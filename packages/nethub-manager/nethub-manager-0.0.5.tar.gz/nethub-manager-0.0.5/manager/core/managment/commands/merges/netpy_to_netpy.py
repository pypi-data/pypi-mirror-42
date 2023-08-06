import os
import sys
import h5py
import json
import numpy as np

def netpy_to_netpy_merge(master_net, second_net):

    with open(master_net+'/net_data/arch.json', 'r') as master:
        master_data = json.load(master)
        num_of_master_layers = len(master_data['net']['arch']['layers'])
        num_of_master_connections = len(master_data['net']['arch']['connections'])
        num_of_master_in_neurons = master_data['net']['arch']['layers'][0]['num_of_neurons']
        num_of_master_modules = num_of_master_layers + num_of_master_connections

    with open(second_net+'/net_data/arch.json', 'r') as second:
        second_data = json.load(second)
        num_of_second_layers = len(second_data['net']['arch']['layers'])
        num_of_second_connections = len(second_data['net']['arch']['connections'])
        num_of_second_in_neurons = second_data['net']['arch']['layers'][0]['num_of_neurons']
        num_of_second_modules = num_of_second_layers + num_of_second_connections

    if num_of_master_layers != num_of_second_layers:
        print('Non-valid architecture.')
    elif num_of_master_in_neurons!= num_of_second_in_neurons:
        print('Non-valid architecture.')
    else:

        master_weights = h5py.File(master_net+'/net_data/weights.h5', 'r+')
        second_weights = h5py.File(second_net+'/net_data/weights.h5', 'r+')


        current_master_weights = master_weights['weights_0_2'][:]
        current_second_weights = second_weights['weights_0_2'][:]

        cur_master_line = len(current_master_weights)
        cur_master_col = len(current_master_weights[0])
        cur_second_line = len(current_second_weights)
        cur_second_col = len(current_second_weights[0])

        current_master_weights = np.append(current_master_weights, current_second_weights, axis=1)

        master_weights['weights_0_2'].resize((cur_master_line, cur_master_col+cur_second_col))
        master_weights['weights_0_2'][:] = current_master_weights

        for i in range(3, num_of_master_modules, 2):
            current_master_weights = master_weights['weights_'+str(i-1)+'_'+str(i+1)][:]
            current_second_weights = second_weights['weights_'+str(i-1)+'_'+str(i+1)][:]

            cur_master_line = len(current_master_weights)
            cur_master_col = len(current_master_weights[0])
            cur_second_line = len(current_second_weights)
            cur_second_col = len(current_second_weights[0])

            right_top_matrix = np.zeros((cur_master_line, cur_second_col))
            left_bot_matrix = np.zeros((cur_second_line, cur_master_col))

            current_master_weights = np.append(current_master_weights, right_top_matrix, axis=1)
            bottom_matrix = np.append(left_bot_matrix, current_second_weights, axis=1)

            current_master_weights = np.vstack((current_master_weights, bottom_matrix))

            master_weights['weights_'+str(i-1)+'_'+str(i+1)].resize((cur_master_line+cur_second_line,
                                                                     cur_master_col+cur_second_col))
            master_weights['weights_'+str(i-1)+'_'+str(i+1)][:] = current_master_weights

        master_weights.close()

        with open(master_net+'/net_data/arch.json', 'r') as log:
            json_data = json.load(log)
            json_data['net']['arch']['layers'][-2]['num_of_neurons'] = len(current_master_weights)
            json_data['net']['arch']['layers'][-1]['num_of_neurons'] = len(current_master_weights[0])

        with open(master_net+'/net_data/arch.json', 'w') as log:
            log.write(json.dumps(json_data, indent=4))


