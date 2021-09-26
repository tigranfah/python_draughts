import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers

import os


class Models:

    __networks__ = None

    def __init__(self):
        if type(Models.__networks__) is None:
            raise Exception(f"{__class__.__name__} is a singleton class.")

        Models.__networks__ = {}
        for dir in os.listdir("models"):
            Models.add_model("myModel", os.path.join("models", dir))
        print(Models.__networks__)

    @staticmethod
    def add_model(name, path_to_model):
        Models.__networks__[name] = keras.models.load_model(path_to_model)

    @staticmethod
    def get_model(name):
        Models.__networks__.get(name)

    @staticmethod
    def remove_model(name):
        del Models.__networks__[name]


Models()
# model = keras.Sequential()
# model.add(layers.Dense(4, input_shape=(4, ), activation="relu"))
# model.add(layers.Dense(13, activation="relu"))
# model.add(layers.Dense(2, activation="relu"))
#
# model.compile(loss="mse", optimizer="adam")
#
# model.save("models/my_model")
