# import tensorflow as tf
# import tensorflow.keras as keras
# import tensorflow.keras.layers as layers
# import numpy as np

import os
import copy
import sys
sys.path.insert(0, "./python-chess")

import chess

import board_proc as bp


DEFAULT_LAYOUT = list(".o.o.o.oo.o.o.o..o.o.o.o.........X......O.O.O.O..O.O.O.OO.O.O.O.")
SQUARE_NAMES = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
                'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
                'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
                'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
                'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
                'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
                'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
                'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']


class Move:

    def __init__(self, str_move, eat_index=None, promotion=False):
        if not type(str_move) is str: raise ValueError(f"{str_move} must be a string.")
        if len(str_move) != 4: raise ValueError(f"{str_move} must have 4 character.")
        self.from_pos = str_move[:2]
        self.to_pos = str_move[2:]
        self.from_index = SQUARE_NAMES.index(self.from_pos)
        self.to_index = SQUARE_NAMES.index(self.to_pos)
        self.eat_index = eat_index
        self.promotion = promotion

    @staticmethod
    def from_indices(from_ind, to_ind):
        return Move(f"{SQUARE_NAMES[from_ind]}{SQUARE_NAMES[to_ind]}")

    def __str__(self):
        return self.from_pos + self.to_pos

    def __repr__(self):
        return self.from_pos + self.to_pos


class Engine:

    def __init__(self, size):
        self.turn = True
        self.size = size
        self._layout = DEFAULT_LAYOUT
        self._move_stack = []
        # self.board = board

    def valid_moves(self, from_index, jump=False):
        fig = self.get(from_index)
        valid_moves = []
        only_jump = jump
        possible_moves = None

        if fig in ["O", "o"]:
            if jump:
                possible_moves = (from_index, -1, 1), (from_index, 1, 1), (from_index, -1, -1), (from_index, 1, -1)
            elif fig == "O":
                possible_moves = (from_index, -1, 1), (from_index, 1, 1),
            elif fig == "o":
                possible_moves = (from_index, -1, -1), (from_index, 1, -1)

            for i, x, y in possible_moves:
                if self.get_index(i, x, y):
                    index = self.get_index(i, x, y)
                    # print(index)
                    if not only_jump and self.get(index) == ".":
                        valid_moves.append((index, None))
                    elif self.get(index) in self.__get_opposite_figs(fig):
                        if self.get_index(from_index, x*2, y*2):
                            jump_index = self.get_index(from_index, x*2, y*2)
                            # print(Engine.SQUARE_NAMES[jump_index])
                            if self.get(jump_index) == ".":
                                valid_moves.append((jump_index, index))

        elif fig in ["X", "x"]:
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
                        if not only_jump and self.get(index) == ".":
                            valid_moves.append((index, opposite_fig))
                        elif self.get(index) in self.__get_opposite_figs(fig):
                            if opposite_fig:
                                break
                            only_jump = False
                            opposite_fig = index

        return valid_moves

    def force_push(self, move):
        if self._layout[move.from_index] == ".":
            raise Exception(f"In {move.from_index} field there is no figure.")
        self._layout[move.to_index] = self._layout[move.from_index]
        self._layout[move.from_index] = "."
        if move.eat_index: self._layout[move.eat_index] = "."
        if move.promotion: self._layout[move.to_index] = self.__get_promotion(self._layout[move.to_index])

    def __push_jump(self, from_index):
        jump_moves = self.valid_moves(from_index, jump=True)
        if not jump_moves: return
        while True:
            print("Jump.")
            print(self)
            to_index = SQUARE_NAMES.index(input())
            for m, opp in jump_moves:
                if m == to_index:
                    move = Move.from_indices(from_index, to_index)
                    move.eat_index = opp
                    move.promotion = self.__is_promoted(to_index)
                    self.force_push(move)
                    if opp == 1:
                        self.__push_jump(to_index)
                    return

    def push(self, move):
        # if not self.is_valid(move):
        #     print(f"{move} is not valid.")

        valid_moves = self.valid_moves(move.from_index)
        print([(SQUARE_NAMES[m], opp) for m, opp in valid_moves])

        for m, opp in valid_moves:
            if m == move.to_index:
                move.eat_index = opp
                move.promotion = self.__is_promoted(move.to_index)
                self.force_push(move)
                if opp:
                    self.__push_jump(move.to_index)

        # self.turn = not self.turn

    def get_index(self, index, x=0, y=0):
        if (index % self.size) + 1 + x <= 0 or (index % self.size) + 1 + x > self.size:
            return None
        if self.size - (index // self.size) + y <= 0 or self.size - (index // self.size) + y > self.size:
            return None
        return index + x + self.size * -y

    def get(self, index, x=0, y=0):
        return self._layout[self.get_index(index, x, y)]

    @property
    def layout(self):
        return self._layout

    def __get_opposite_figs(self, fig):
        return {
            "O" : ["o", "x"],
            "X" : ["o", "x"],
            "o" : ["O", "X"],
            "x" : ["O", "X"]
        }[fig]

    def __get_promotion(self, fig):
        return {
            "O" : "X",
            "o" : "x"
        }[fig]

    def __is_promoted(self, index):
        if not self.get(index) in ["o", "O"]: return False
        if 0 <= index < self.size or self.size**2-self.size <= index < self.size**2:
            return True
        return False

    def __str__(self):
        return "\n".join([f"{' '.join(self._layout[i*8:i*8+8])}" for i in range(8)])

    def __repr__(self):
        return str(self)


# def get_model(unit_size):
#     model = keras.models.Sequential()
#     model.add(layers.Dense(256, input_shape=(68, ), activation="relu"))
#     model.add(layers.Dense(512, activation="relu"))
#     # model.add(layers.Dense(512, activation="relu"))
#     # model.add(layers.Dropout(0.3))
#     model.add(layers.Dense(1024, activation="relu"))
#     model.add(layers.Dropout(0.3))
#     model.add(layers.Dense(1024, activation="relu"))
#     model.add(layers.Dropout(0.3))
#     # model.add(layers.Dense(512, activation="relu"))
#     # model.add(layers.Dropout(0.3))
#     model.add(layers.Dense(256, activation="relu"))
#     model.add(layers.Dropout(0.3))
#     model.add(layers.Dense(1, activation="sigmoid"))
#
#     model.compile(optimizer="adam",
#                   loss=keras.losses.BinaryCrossentropy(),
#                   metrics=["accuracy"])
#
#     return model

# model = get_model(512)
# model.save("models/model")
