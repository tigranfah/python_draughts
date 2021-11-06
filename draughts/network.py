import numpy as np


class Activation:

    @staticmethod
    def relu(x):
        return np.vectorise(lambda x : max(0, x))

    @staticmethod
    def sigmoid():
        return np.vectorise(lambda x : 1 / (1 + np.exp(-x)))


class Layer:

    def __init__(self, sunit_size, activation):
        self.unit_size = unit_size
        self.activation = activation

        self.W = np.empty(0)
        self.b = np.empty(0)

    def forward(self, X):
        return self.activation(np.dot(self.W, X) + self.b)

    @property
    def W(self):
        return self.W

    @W.setter
    def W(self, W):
        self.W = W

    @property
    def b(self):
        return self.b

    @b.setter
    def b(self, b):
        self.b = b


class Network:

    def __init__(self, input_shape):
        self.layers = []
        # self.layers = [
        #     Layer(input_shape, Activation.relu),
        #     Layer()]

    def forward(self, X):
        a = X
        for layer in self.layers:
            a = layer.forward(a)

        return a
