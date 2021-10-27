import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
import numpy as np

import os
import sys
sys.path.insert(0, "./python-chess")

import chess

import board_proc as bp


class UCIMove:

    def __init__(self, uci_str_move=None):
        if not uci_str_move: return
        self.from_pos = uci_str_move[:2]
        self.to_pos = uci_str_move[2:]
        self.promotion = None

    def __str__(self):
        return self.from_pos + self.to_pos

    def __repr__(self):
        return self.from_pos + self.to_pos


class Engine:

    def __init__(self, path_to_model):
        self._name = path_to_model.split("/")[-1]
        self._keras_model = keras.models.load_model(os.path.join("models", path_to_model))
        self._keras_model.load_weights(os.path.join("models", "weights.h5"))

    def predict(self, board, uci_move):
        inp = bp.board_to_input(board)
        inp.extend(bp.board_pos_to_num_pos(uci_move.from_pos))
        inp.extend(bp.board_pos_to_num_pos(uci_move.to_pos))
        inp = np.array(inp)
        inp = inp / inp.max()
        return self._keras_model.predict(np.array([inp]))[0]


def get_model(unit_size):
    model = keras.models.Sequential()
    model.add(layers.Dense(256, input_shape=(68, ), activation="relu"))
    model.add(layers.Dense(512, activation="relu"))
    # model.add(layers.Dense(512, activation="relu"))
    # model.add(layers.Dropout(0.3))
    model.add(layers.Dense(1024, activation="relu"))
    model.add(layers.Dropout(0.3))
    model.add(layers.Dense(1024, activation="relu"))
    model.add(layers.Dropout(0.3))
    # model.add(layers.Dense(512, activation="relu"))
    # model.add(layers.Dropout(0.3))
    model.add(layers.Dense(256, activation="relu"))
    model.add(layers.Dropout(0.3))
    model.add(layers.Dense(1, activation="sigmoid"))

    model.compile(optimizer="adam",
                  loss=keras.losses.BinaryCrossentropy(),
                  metrics=["accuracy"])

    return model

# model = get_model(512)
# model.save("models/model")
