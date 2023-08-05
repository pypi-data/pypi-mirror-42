import os
import sys
import h5py
import json
import numpy as np

def save_attributes_to_hdf5_group(group, name, data):

    HDF5_OBJECT_HEADER_LIMIT = 64512

    bad_attributes = [x for x in data if len(x) > HDF5_OBJECT_HEADER_LIMIT]

    # Expecting this to never be true.
    if len(bad_attributes) > 0:
        raise RuntimeError('The following attributes cannot be saved to HDF5 '
                           'file because they are larger than %d bytes: %s'
                           % (HDF5_OBJECT_HEADER_LIMIT,
                              ', '.join([x for x in bad_attributes])))

    data_npy = np.asarray(data)

    num_chunks = 1
    chunked_data = np.array_split(data_npy, num_chunks)

    # This will never loop forever thanks to the test above.
    while any(map(lambda x: x.nbytes > HDF5_OBJECT_HEADER_LIMIT, chunked_data)):
        num_chunks += 1
        chunked_data = np.array_split(data_npy, num_chunks)

    if num_chunks > 1:
        for chunk_id, chunk_data in enumerate(chunked_data):
            group.attrs['%s%d' % (name, chunk_id)] = chunk_data
    else:
        group.attrs[name] = data


def keras_to_keras_merge(master_net, second_net):
    print("Coming soon!")

def keras_to_keras_merge_test(master_net, second_net):
    
    with open(master_net+'/'+master_net+'_data/'+master_net+'.json', 'r') as master:
        master_data = json.load(master)
        num_of_master_layers = len(master_data["config"])
        num_of_master_in_neurons = master_data["config"][0]["config"]["batch_input_shape"][1]
        name_of_master_in_layer = master_data["config"][0]["config"]["name"]
        name_of_master_hid_layer = master_data["config"][1]["config"]["name"]

    with open(second_net+'/'+second_net+'_data/'+second_net+'.json', 'r') as second:
        second_data = json.load(second)
        num_of_second_layers = len(second_data["config"])
        num_of_second_in_neurons = second_data["config"][0]["config"]["batch_input_shape"][1]
        name_of_second_in_layer = second_data["config"][0]["config"]["name"]
        name_of_second_hid_layer = second_data["config"][1]["config"]["name"]


    if num_of_master_layers != num_of_second_layers:
        print('Non-valid architecture')
        return False
    elif num_of_master_in_neurons != num_of_second_in_neurons:
        print('Non-valid architecture')
    else:
        master_weights = h5py.File(master_net+'/'+master_net+'_data/'+master_net+'.h5', 'r')
        second_weights = h5py.File(second_net+'/'+second_net+'_data/'+second_net+'.h5', 'r')


        current_master_weights = master_weights[name_of_master_in_layer][name_of_master_in_layer]["kernel:0"][:]
        current_second_weights = second_weights[name_of_second_in_layer][name_of_second_in_layer]["kernel:0"][:]

        cur_master_line = len(current_master_weights)
        cur_master_col = len(current_master_weights[0])
        cur_second_line = len(current_second_weights)
        cur_second_col = len(current_second_weights[0])

        print(len(current_master_weights), len(current_master_weights[0]), "/n")

        current_master_weights = np.append(current_master_weights, current_second_weights, axis=1)

        print(len(current_master_weights), len(current_master_weights[0]), "/n")

        current_master_weights = np.array(current_master_weights, dtype='float32')


        data_new = h5py.File(master_net+"/"+master_net+"_data/tmp.h5", "w")

        backend = "tensorflow"
        version = "2.1.4"
        layers = [name_of_master_in_layer, name_of_master_hid_layer]

        data_new.attrs["backend"] = str(backend).encode('utf8')
        data_new.attrs["keras_version"] = str(version).encode('utf8')
        save_attributes_to_hdf5_group(data_new, 
                                      "layer_names", 
                                      [layer.encode('utf8') for layer in layers],
                                     )

        group = data_new.create_group(name_of_master_in_layer)
       
        weight_names = [name_of_master_in_layer+"/kernel:0",name_of_master_in_layer+"/bias:0"]

        save_attributes_to_hdf5_group(group, 
                                      "weight_names", 
                                      [weight.encode('utf8') for weight in weight_names],
                                     )

        group2 = data_new.create_group(name_of_master_in_layer + "/" +name_of_master_in_layer)

        param_dset = group2.create_dataset("kernel:0",
                                           data=current_master_weights,
                                           maxshape=(None, None)
                                          )

        param_dset[:] = np.asarray(current_master_weights)

        group2.create_dataset("bias:0",
                              data=[0],
                             )
        
        current_master_weights = master_weights[name_of_master_hid_layer][name_of_master_hid_layer]["kernel:0"]
        current_second_weights = second_weights[name_of_second_hid_layer][name_of_second_hid_layer]["kernel:0"]

        cur_master_line = len(current_master_weights)
        cur_master_col = len(current_master_weights[0])
        cur_second_line = len(current_second_weights)
        cur_second_col = len(current_second_weights[0])

        right_top_matrix = np.zeros((cur_master_line, cur_second_col))
        left_bot_matrix = np.zeros((cur_second_line, cur_master_col))

        current_master_weights = np.append(current_master_weights, right_top_matrix, axis = 1)

        bottom_matrix = np.append(left_bot_matrix, current_second_weights, axis=1)

        current_master_weights = np.vstack((current_master_weights, bottom_matrix))
        current_master_weights = np.array(current_master_weights, dtype='float32')
        

        group = data_new.create_group(name_of_master_hid_layer)

        weight_names = [
                        name_of_master_hid_layer+"/kernel:0",
                        name_of_master_hid_layer+"/bias:0",
                       ]

        save_attributes_to_hdf5_group(group, 
                                      "weight_names", 
                                      [weight.encode('utf8') for weight in weight_names],
                                     )


        group2 = data_new.create_group(name_of_second_hid_layer + "/" + name_of_master_hid_layer)

        param_dset = group2.create_dataset("kernel:0", 
                                           data=current_master_weights,
                                           maxshape=(None, None),
                                          )

        param_dset[:] = np.asarray(current_master_weights)

        group2.create_dataset("bias:0",
                              data=[0],
                             )

        data_new.flush()

        master_weights.close()
        second_weights.close()

        os.remove(master_net+"/"+master_net+"_data"+"/"+master_net+".h5")
        os.rename(master_net+"/"+master_net+"_data/tmp.h5", 
                  master_net+"/"+master_net+"_data"+"/"+master_net+".h5",
                 )

        with open(master_net+'/'+master_net+'_data/'+master_net+'.json', 'r') as config:
            json_data = json.load(config)
            json_data["config"][0]["config"]["units"] += cur_second_line
            json_data["config"][1]["config"]["units"] += cur_second_col

        with open(master_net+'/'+master_net+'_data/tmp.json', 'w') as config:
            config.write(json.dumps(json_data, indent=4))

        os.remove(master_net+"/"+master_net+"_data/"+master_net+".json")
        os.rename(master_net+"/"+master_net+"_data/tmp.json",
                  master_net+"/"+master_net+"_data/"+master_net+".json"
                 )
