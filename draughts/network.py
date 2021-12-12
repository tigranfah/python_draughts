import numpy as np
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
import pickle


def get_conv_model(unit_size, conv_depth):
    model = keras.models.Sequential()
    model.add(layers.Conv2D(unit_size, (2, 2), input_shape=(12, 8, 1), activation="relu"))
    model.add(layers.MaxPooling2D((1, 1)))
    for i in range(conv_depth):
      model.add(layers.Conv2D(unit_size, (1, 1), activation="relu"))
      model.add(layers.Conv2D(unit_size, (1, 1), activation="relu"))
      model.add(layers.MaxPooling2D((1, 1)))
    model.add(layers.Flatten())
    model.add(layers.Dense(unit_size*2, activation="relu", kernel_regularizer=keras.regularizers.l1_l2(l1=1e-8, l2=1e-7)))
    model.add(layers.Dropout(0.3))
    model.add(layers.Dense(unit_size, activation="relu", kernel_regularizer=keras.regularizers.l1_l2(l1=1e-8, l2=1e-7)))
    model.add(layers.Dropout(0.3))
    model.add(layers.Dense(1, activation="sigmoid"))

    sgd = keras.optimizers.SGD(learning_rate=0.1, momentum=0.0)

    model.compile(loss=keras.losses.MeanSquaredError(),
                  optimizer="adam",
                  metrics=["accuracy"])

    return model


model = get_conv_model(128, 0)
model.load_weights("models/conv_weights_256_3.h5")

with open("models/weights.pickle", "wb") as file:
    pickle.dump(model.get_weights(), file)
# for i in model.get_weights():
#     print(i.shape)


# class CNN:
#
#     def __init__(self, input_shape):
#
#         self._input_shape = input_shape
#         self.W =
#         self.B =
#         self.filters

    #     self._conv_layers()
    #
    # def conv_layers
