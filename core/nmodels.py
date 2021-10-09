import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
import numpy as np

import os
import sys
sys.path.insert(0, "../python-chess")

import chess

import board_proc as bp


def legal_move(board, move):
    fr, to = board_pos_to_num_pos(str(move)[:2]), board_pos_to_num_pos(str(move)[2:])
    fin_f, fin_t = None, None
    all_from = [board_pos_to_num_pos(str(m)[:2]) for m in board.legal_moves]
    all_to = [board_pos_to_num_pos(str(m)[2:]) for m in board.legal_moves]
    from_dist = 100
    for f in all_from:
        if np.all(fr == f):
            fin_f = fr
            break
        if from_dist > dist(f, fr):
            from_dist = dist(f, fr)
            print("Found", f)
            fin_f = f
    to_dist = 100
    print("ff", fin_f)
    for f, t in zip(all_from, all_to):
        if not np.all(fin_f == f):
            continue
        if np.all(to == t):
            fin_t = to
            break
        if to_dist > dist(t, to):
            to_dist = dist(t, to)
            fin_t = t

    print(fin_f, fin_t)
    return fin_f, fin_t


def next_move(board):
    inp = np.array(board_to_input(board))
    inp = inp / inp.max()
    # inp = np.array([base_4bits(x_) for x_ in inp])
    inp = inp.reshape(8, 8, 1)
    # print(inp)
    net_move = model1.predict(np.array([inp]))[0]
    # net_move = (net_move*8).round().astype(np.int8)
    # net_move = net_move - 1
    x1 = decimal(net_move[:3])
    y1 = decimal(net_move[3:6])
    x2 = decimal(net_move[6:9])
    y2 = decimal(net_move[9:12])
    print(x1, y1, x2, y2)
    net_move = f"{num_pos_to_board_pos([x1, y1])}{num_pos_to_board_pos([x2, y2])}"
    legal = False
    for m in board.legal_moves:
        if str(m) == net_move:
            board.push_uci(net_move)
            legal = True
    if not legal:
        f, t = legal_move(board, net_move)
        net_move = f"{num_pos_to_board_pos(f)}{num_pos_to_board_pos(t)}"
        board.push_uci(net_move)


class Model:

    def __init__(self, path_to_model):
        self.name = path_to_model.split("/")[0]
        self.model = keras.models.load_model(path_to_model)


class ConvNetModel(Model):

    def __init__(self, path_to_model):
        super().__init__(path_to_model)
        self.input_shape = self.model.layers[0].input_shape[1:]
        self.output_size = self.model.layers[-1].output_shape[-1]

    def get_input_for_model(self, board):
        inp = np.array(bp.board_to_input(board))
        inp = (inp / inp.max()).reshape(*self.input_shape)
        return np.array([inp])

    def convert_move(self, model_move):
        model_move = [bp.to_decimal(model_move[i:i+self.output_size//4]) for i in range(0, self.output_size, self.output_size//4)]
        return f"{bp.num_pos_to_board_pos(model_move[:2])}{bp.num_pos_to_board_pos(model_move[2:])}"

    def predict(self, board):
        input = self.get_input_for_model(board)
        model_move = self.model.predict(input)[0]
        uci_move = self.convert_move(model_move)
        return uci_move


class NModels:

    __instance = None
    __model = None

    def __init__(self):
        if type(NModels.__instance) is None:
            raise Exception(f"{__class__.__name__} is a singleton class.")

        NModels.__instance = self

    @staticmethod
    def set_model(model):
        NModels.__instance.__model = model

    @staticmethod
    def get_model():
        return NModels.__instance.__model


NModels()

board = chess.Board()
NModels.set_model(ConvNetModel("../models/my_model"))
uci_move = NModels.get_model().predict(board)
print(uci_move)
# model = keras.models.Sequential()
# model.add(layers.Conv2D(128, (4, 4), input_shape=(8, 8, 1), activation="relu"))
# model.add(layers.MaxPooling2D((1, 1)))
# model.add(layers.Flatten())
# model.add(layers.Dense(128, activation="relu", kernel_regularizer=keras.regularizers.l1_l2(l1=1e-6, l2=1e-5)))
# model.add(layers.Dropout(0.2))
# model.add(layers.Dense(12, activation="sigmoid"))
#
# model.compile(loss="mse", optimizer="adam")
#
# model.save("../models/my_model")
