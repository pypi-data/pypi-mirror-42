from netpy.nets import FeedForwardNet


net = FeedForwardNet({name})

test = []

net.load_net_data()
net.load_weights()

print(net.forward(test))
