from netpy.teachers import BackPropTeacher
from netpy.nets import FeedForwardNet
import numpy as np


net = FeedForwardNet({name})
net.load_net_data()
# net.load_weights()

num_of_epoch = 8

train_X = np.loadtxt('data_set/train_X.txt')
train_Y = np.loadtxt('data_set/train_Y.txt')

teacher = BackPropTeacher(net,
                          error = 'MSE')

teacher.train(train_X, train_Y, 
              num_of_epoch,
              learning_rate = [0.001, 0.002])

