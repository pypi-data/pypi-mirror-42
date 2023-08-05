from keras.models import model_from_json
import numpy as np
import json


json_file = open({json_path})
net_json = json_file.read()
json_file.close()

net = model_from_json(net_json)
net.load_weights({weights_path})

net.compile(loss='binary_crossentropy',
            optimizer='ADAM',
            metrics=['accuracy'],
           )

train_X = np.loadtxt('data_set/train_X.txt')
train_Y = np.loadtxt('data_set/train_Y.txt')

num_of_epoch = 8

net.fit(train_X,
        train_Y,
        epochs=num_of_epoch,
       )

net_json = net.to_json()
net_json = json.loads(net_json)

with open({json_path}, "w") as file:
    json.dump(net_json, file, indent=4)

net.save_weights({weights_path})
