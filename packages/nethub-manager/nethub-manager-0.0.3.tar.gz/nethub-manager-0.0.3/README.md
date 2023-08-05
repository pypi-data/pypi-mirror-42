# Nethub-Manager

CLI Util for your neuronets!

## Install
```sh
sudo python3 setup.py install
```

## Getting Started

First, you need to initialize all settings with command _init_:
```sh
nhm init
```

Then, you need to login (you need to register on your nethub server):
```sh
nhm login
```

Okay, let's create first net (NetPy):
```sh
nhm newnet my_first_net
```

And write your first commit!
```sh
Commit: My first commit!
```

You can see your net in web-browser
![NetHub](pics/nethub.png)


Let's change our network init file (`network.py`). Add some neurons:
```python
''' It's network init file '''

from netpy.nets import FeedForwardNet
from netpy.modules import LinearLayer, SigmoidLayer, FullConnection


net = FeedForwardNet(name = 'my_first_net')

# Add your layers here
input_layer = LinearLayer(3)
hidden_layer = SigmoidLayer(2)
output_layer = SigmoidLayer(1)

# Add your layers to the net here
net.add_Input_Layer(input_layer)
net.add_Layer(hidden_layer)
net.add_Output_Layer(output_layer)

# Add your connections here
con_in_hid = FullConnection(input_layer, hidden_layer)
con_hid_out = FullConnection(hidden_layer, output_layer)

# Add your connections to the net here
net.add_Connection(con_in_hid)
net.add_Connection(con_hid_out)

# Save your net
net.save()

``` 

Push your changes to server:
```sh
cd my_first_net
nhm add network.py
nhm commit
nhm push
```
