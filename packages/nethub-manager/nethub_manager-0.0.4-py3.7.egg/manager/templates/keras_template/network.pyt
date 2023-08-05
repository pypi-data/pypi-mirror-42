''' It's network init file '''

from keras.models import Sequential
from keras.layers import Dense
import json

net = Sequential()
net.add(Dense(2, input_dim=3, activation='sigmoid'))
net.add(Dense(1, activation='sigmoid'))

net.compile(loss='binary_crossentropy',
            optimizer='ADAM',
            metrics=['accuracy'],
           )

net_json = net.to_json()
net_json = json.loads(net_json)

with open({json_path},"w") as file:
    json.dump(net_json, file, indent=4)

net.save_weights({weights_path})
