from keras.models import model_from_json
import numpy as np

test = np.array()

json_file = open({json_path})
net_json = json_file.read()
json_file.close()

net = model_from_json(net_json)
net.load_weights({weights_path})

net.compile(loss='binary_crossentropy',
            optimizer='ADAM',
            metrics=['accuracy'],
           )

print(net.predict(test))
