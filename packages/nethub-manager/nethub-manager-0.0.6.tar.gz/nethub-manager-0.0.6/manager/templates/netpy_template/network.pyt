''' It's network init file '''

from netpy.nets import FeedForwardNet
from netpy.modules import LinearLayer, SigmoidLayer, FullConnection


net = FeedForwardNet({name})

# Add your layers here
input_layer = LinearLayer()
hidden_layer = SigmoidLayer()
output_layer = SigmoidLayer()

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

