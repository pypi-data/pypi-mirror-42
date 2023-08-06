# Authors: Daichi Yoshikawa <daichi.yoshikawa@gmail.com>
# License: BSD 3 clause

import sys
sys.path.append('../..')

import matplotlib.pyplot as plt
import pickle
import numpy as np
import dnnet
from dnnet.neuralnet import NeuralNetwork
from dnnet.utils.nn_utils import scale_normalization

from dnnet.training.optimizer import AdaGrad
from dnnet.training.weight_initialization import DefaultInitialization, He
from dnnet.training.loss_function import LossFunction

from dnnet.layers.activation import Activation, ActivationLayer
from dnnet.layers.affine import AffineLayer
from dnnet.layers.batch_norm import BatchNormLayer
from dnnet.layers.convolution import ConvolutionLayer
from dnnet.layers.dropout import DropoutLayer
from dnnet.layers.pooling import PoolingLayer

from data import get_mnist


dtype = np.float32
model = NeuralNetwork(input_shape=(1, 28, 28), dtype=dtype)

model.add(
    ConvolutionLayer(
        filter_shape=(32, 3, 3), pad=(0, 0), strides=(1, 1),
        weight_initialization=He()))
model.add(BatchNormLayer())
model.add(ActivationLayer(activation=Activation.Type.relu))

model.add(
    ConvolutionLayer(
        filter_shape=(32, 3, 3), pad=(0, 0), strides=(1, 1),
        weight_initialization=He()))
model.add(BatchNormLayer())
model.add(ActivationLayer(activation=Activation.Type.relu))
model.add(DropoutLayer(drop_ratio=0.25))

model.add(
    ConvolutionLayer(
        filter_shape=(64, 3, 3), pad=(0, 0), strides=(1, 1),
        weight_initialization=He()))
model.add(BatchNormLayer())
model.add(ActivationLayer(activation=Activation.Type.relu))

model.add(
    ConvolutionLayer(
        filter_shape=(64, 3, 3), pad=(0, 0), strides=(1, 1),
        weight_initialization=He()))
model.add(BatchNormLayer())
model.add(ActivationLayer(activation=Activation.Type.relu))

model.add(AffineLayer(output_shape=256, weight_initialization=He()))
model.add(BatchNormLayer())
model.add(ActivationLayer(activation=Activation.Type.relu))
model.add(DropoutLayer(drop_ratio=0.5))

model.add(AffineLayer(output_shape=10, weight_initialization=DefaultInitialization()))
model.add(BatchNormLayer())
model.add(ActivationLayer(activation=Activation.Type.softmax))
model.compile()

config_str = model.get_config_str()
print(config_str)

data_dir = '../../data'
x, y = get_mnist(data_dir)
scale_normalization(x)
x = x.reshape(-1, 1, 28, 28)

optimizer = AdaGrad(learning_rate=1e-3, weight_decay=1e-3, dtype=dtype)
print('Learning Rate :', optimizer.learning_rate)

lc = model.fit(
    x=x, y=y, epochs=5, batch_size=100, optimizer=optimizer,
    loss_function=LossFunction.Type.multinomial_cross_entropy,
    learning_curve=True, shuffle=True, shuffle_per_epoch=True,
    test_data_ratio=0.142857, # Use 60,000 for training and 10,000 for test.
    train_data_ratio_for_eval=0.01)
lc.plot(figsize=(8,10), fontsize=12)
model.save(path='output', name='mnist_conv_net.dat')

#model.visualize_filters(index=0, n_rows=4, n_cols=8, filter_shape=(3, 3), figsize=(8, 8))
#model.visualize_filters(index=0, shape=None, figsize=(8, 8))
#model.show_filters(0, shape=(28, 28), layout=(10, 10), figsize=(12, 12))
