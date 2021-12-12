# import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
import numpy as np

from PIL import Image

import os
import copy
import sys

import exceptions
import board_proc as bp


class BoardBase:

    W = "O" # white normal
    WQ = "X" # white special

    B = "o" # black normal
    BQ = "x" # black special

    E = "." # empty

    WHITE = ("O", "X")
    BLACK = ("o", "x")

    DEFAULT_LAYOUT = list(".o.o.o.oo.o.o.o..o.o.o.o................O.O.O.O..O.O.O.OO.O.O.O.")
    SQUARE_NAMES = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
                    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
                    'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
                    'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
                    'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
                    'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
                    'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
                    'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']

    core_path = os.path.dirname(os.path.realpath(__file__))

    BOARD_IMG = Image.open(os.path.join(core_path, "res", 'board.jpg'))
    BOARD_IMG = BOARD_IMG.resize((int(BOARD_IMG.size[0]//1.5), int(BOARD_IMG.size[1]//1.5)))
    FIG_SIZE = 37
    WHITE_O_IMG = Image.open(os.path.join(core_path, "res", 'white_o.png')).resize((FIG_SIZE, FIG_SIZE))
    WHITE_X_IMG = Image.open(os.path.join(core_path, "res", 'white_x.png')).resize((FIG_SIZE, FIG_SIZE))
    BLACK_O_IMG = Image.open(os.path.join(core_path, "res", 'black_o.png')).resize((FIG_SIZE, FIG_SIZE))
    BLACK_X_IMG = Image.open(os.path.join(core_path, "res", 'black_x.png')).resize((FIG_SIZE, FIG_SIZE))
    FIELD_SIZE_IN_PIXEL = 44
    BOARD_OFFSET = 17

    @staticmethod
    def get_default_layout():
        return copy.deepcopy(BoardBase.DEFAULT_LAYOUT)

    @staticmethod
    def get_pos(index):
        if len(BoardBase.SQUARE_NAMES) <= index:
            raise exceptions.InvalidIndex(f"Positionn under index {index} does not exist.")
        return BoardBase.SQUARE_NAMES[index]

    @staticmethod
    def get_index(pos):
        if not pos in BoardBase.SQUARE_NAMES:
            raise exceptions.InvalidPosition(f"{pos} is not a valid board position.")
        return BoardBase.SQUARE_NAMES.index(pos)

    @staticmethod
    def get_figure_image(figure):
        return {
            "O" : BoardBase.WHITE_O_IMG,
            "X" : BoardBase.WHITE_X_IMG,
            "o" : BoardBase.BLACK_O_IMG,
            "x" : BoardBase.BLACK_X_IMG
        }[figure]


class Move:

    def __init__(self, str_move, eat_index=None, promotion=False):
        if not type(str_move) is str: raise ValueError(f"{str_move} must be a string.")
        if len(str_move) < 4: raise ValueError(f"{str_move} must have at least 4 character.")
        self.from_pos = str_move[:2]
        self.to_pos = str_move[2:4]
        self.jump_pos = str_move[4:].split()
        self.from_index = BoardBase.get_index(self.from_pos)
        self.to_index = BoardBase.get_index(self.to_pos)
        self.jump_index = [BoardBase.get_index(m) for m in self.jump_pos]
        self.eat_index = eat_index
        self.promotion = promotion

    @staticmethod
    def from_indices(from_ind, to_ind):
        return Move(f"{BoardBase.get_pos(from_ind)}{BoardBase.get_pos(to_ind)}")

    def __str__(self):
        return self.from_pos + self.to_pos

    def __repr__(self):
        return str(self)


class EngineBase:

    def __init__(self, size):
        self.turn = True
        self.size = size
        self._layout = BoardBase.get_default_layout()
        self._move_stack = []

    def force_push(self, move):
        if self._layout[move.from_index] == BoardBase.E:
            raise Exception(f"In {move.from_index} field there is no figure.")
        self._layout[move.to_index] = self._layout[move.from_index]
        self._layout[move.from_index] = BoardBase.E
        if move.eat_index: self._layout[move.eat_index] = BoardBase.E
        if move.promotion: self._layout[move.to_index] = self.get_promotion(self._layout[move.to_index])

    def get_index(self, index, x=0, y=0):
        if (index % self.size) + 1 + x <= 0 or (index % self.size) + 1 + x > self.size:
            return None
        if self.size - (index // self.size) + y <= 0 or self.size - (index // self.size) + y > self.size:
            return None
        return index + x + self.size * -y

    def get(self, index, x=0, y=0):
        return self._layout[self.get_index(index, x, y)]

    def get_opposite_figs(self, fig):
        return {
            "O" : ["o", "x"],
            "X" : ["o", "x"],
            "o" : ["O", "X"],
            "x" : ["O", "X"]
        }[fig]

    def get_promotion(self, fig):
        return {
            "O" : "X",
            "o" : "x"
        }[fig]

    def is_promoted(self, from_index, index):
        if not self.get(from_index) in ["o", "O"]: return False
        if 0 <= index < self.size or self.size**2-self.size <= index < self.size**2:
            return True
        return False

    @property
    def layout(self):
        return self._layout


class Engine(EngineBase):

    def __init__(self, size):
        EngineBase.__init__(self, size)

    def valid_moves(self, jump=False):
        figs = BoardBase.WHITE if self.turn else BoardBase.BLACK
        valid_moves = []
        for i in range(self.size**2):
            if self.get(i) in figs:
                valid_moves.extend([(i, m) for m, o in self.valid_moves_from_index(i, jump)])

        return valid_moves

    def valid_moves_from_index(self, from_index, jump=False):
        fig = self.get(from_index)
        valid_moves = []
        only_jump = jump
        possible_moves = None

        if fig in [BoardBase.W, BoardBase.B]:
            if jump:
                possible_moves = (from_index, -1, 1), (from_index, 1, 1), (from_index, -1, -1), (from_index, 1, -1)
            elif fig == BoardBase.W:
                possible_moves = (from_index, -1, 1), (from_index, 1, 1),
            elif fig == BoardBase.B:
                possible_moves = (from_index, -1, -1), (from_index, 1, -1)

            for i, x, y in possible_moves:
                if self.get_index(i, x, y):
                    index = self.get_index(i, x, y)
                    # print(index)
                    if not only_jump and self.get(index) == BoardBase.E:
                        valid_moves.append((index, None))
                    elif self.get(index) in self.get_opposite_figs(fig):
                        if self.get_index(from_index, x*2, y*2):
                            jump_index = self.get_index(from_index, x*2, y*2)
                            if self.get(jump_index) == BoardBase.E:
                                valid_moves.append((jump_index, index))

        elif fig in [BoardBase.WQ, BoardBase.BQ]:
            possible_moves = []
            possible_moves.append([(from_index, i, i) for i in range(1, self.size)])
            possible_moves.append([(from_index, -i, i) for i in range(1, self.size)])
            possible_moves.append([(from_index, i, -i) for i in range(1, self.size)])
            possible_moves.append([(from_index, -i, -i) for i in range(1, self.size)])

            for pos in possible_moves:
                opposite_fig = None
                only_jump = jump
                for i, x, y in pos:
                    if self.get_index(i, x, y):
                        index = self.get_index(i, x, y)
                        if not only_jump and self.get(index) == BoardBase.E:
                            valid_moves.append((index, opposite_fig))
                        elif self.get(index) in self.get_opposite_figs(fig):
                            if opposite_fig:
                                break
                            only_jump = False
                            opposite_fig = index

        return valid_moves

    def valid_push(self, move, jump=False):
        valid_moves = self.valid_moves_from_index(move.from_index, jump)
        for m, opp in valid_moves:
            # print(m, move.to_index)
            if m == move.to_index:
                move.eat_index = opp
                move.promotion = self.is_promoted(move.from_index, move.to_index)
                # print(move.to_index, move.promotion)
                self.force_push(move)
                if not jump and opp:
                    for j_m in move.jump_index:
                        move = Move.from_indices(move.to_index, j_m)
                        self.valid_push(move, True)
                break
        else:
            raise exceptions.InvalidMove(f"{move} is not a valid move.")

    def push(self, move):

        if self.turn and self.get(move.from_index) in BoardBase.BLACK:
            raise exceptions.InvalidMove(f"{move} is not a valid move.")
        elif not self.turn and self.get(move.from_index) in BoardBase.WHITE:
            raise exceptions.InvalidMove(f"{move} is not a valid move.")

        self.valid_push(move)
        self.turn = not self.turn


def get_conv_model(unit_size, conv_depth):
    model = keras.models.Sequential()
    model.add(layers.Conv2D(unit_size*2, (4, 4), input_shape=(12, 8, 4), activation="relu"))
    model.add(layers.MaxPooling2D((1, 1)))
    # for i in range(conv_depth):
    model.add(layers.Conv2D(unit_size, (2, 2), activation="relu"))
    model.add(layers.MaxPooling2D((1, 1)))
    model.add(layers.Conv2D(unit_size, (2, 2), activation="relu"))
    model.add(layers.MaxPooling2D((1, 1)))
    model.add(layers.Flatten())
    model.add(layers.Dense(unit_size, activation="relu"))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(unit_size, activation="relu"))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(1, activation="sigmoid"))

    model.compile(loss=keras.losses.MeanSquaredError(),
                  optimizer="adam",
                  metrics=["accuracy"])

    return model


class NetEngine(EngineBase):

    def __init__(self, size):
        EngineBase.__init__(self, size)
        current_path = os.path.dirname(os.path.realpath(__file__))
        # print(os.listdir(os.path.join(current_path, "..", "models")))
        # self.model = keras.models.load_model(os.path.join(current_path, "..", "models", "model"))
        self.th = 0.7
        self.model = get_conv_model(64, 1)
        self.model.load_weights(os.path.join(current_path, "..", "models", "conv_weights_64.h5"))

    def validate(self, move):
        inp = [bp.fig_to_num(cell) for cell in self._layout]
        x, y = bp.board_pos_to_num_pos(str(move)[:2])
        x1, y1 = bp.board_pos_to_num_pos(str(move)[2:])
        for p in (x, y, x1, y1):
            base_ = np.zeros(8)
            base_[p] = 1
            inp.extend(base_)

        inp = np.array(inp).astype("int").reshape(12, 8, -1)
        # print(inp.flatten())
        new_input = []
        for num in inp.flatten():
            base_4 = np.zeros(4)
            if num != 0:
                base_4[num-1] = 1
            new_input.append(base_4)

        new_input = np.array(new_input).reshape(12, 8, 4)

        return self.model.predict(np.array([new_input]))[0][0]

    def push(self, move):
        pred = self.validate(move)
        if pred < self.th: raise exceptions.InvalidMove(f"{move} is not a valid move.")
        valid_moves = Engine.valid_moves_from_index(self, move.from_index, False)
        _, opp = [m for m in valid_moves if move.to_index == m[0]][0]

        move.eat_index = opp
        move.promotion = self.is_promoted(move.from_index, move.to_index)

        self.force_push(move)

    def valid_moves_from_index(self, from_index, jump=False):
        valid_moves = []
        for pos in BoardBase.SQUARE_NAMES:
            pred = self.validate(BoardBase.get_pos(from_index) + pos)
            if pred > self.th:
                valid_moves.append((Move.from_indices(from_index, BoardBase.get_index(pos)), pred))

        return valid_moves

# model = get_conv_model(128, 0)
# model.save("models/model")
