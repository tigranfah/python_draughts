# import tensorflow as tf
# import tensorflow.keras as keras
# import tensorflow.keras.layers as layers
# import numpy as np

import os
import copy
import sys
sys.path.insert(0, "./python-chess")

import chess

import exceptions
import board_proc as bp


class BoardBase:

    DEFAULT_LAYOUT = list(".o.o.o.oo.o.o.o..o.o.o.o.........X......O.O.O.O..O.O.O.OO.O.O.O.")
    SQUARE_NAMES = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
                    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
                    'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
                    'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
                    'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
                    'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
                    'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
                    'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
    
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
        return self.from_pos + self.to_pos


class Engine:

    def __init__(self, size):
        self.turn = True
        self.size = size
        self._layout = BoardBase.get_default_layout()
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

    def valid_push(self, move, jump=False):
        valid_moves = self.valid_moves(move.from_index, jump)
        for m, opp in valid_moves:
            # print(m, move.to_index)
            if m == move.to_index:
                move.eat_index = opp
                move.promotion = self.__is_promoted(move.to_index)
                self.force_push(move)
                if not jump and opp:
                    for j_m in move.jump_index:
                        move = Move.from_indices(move.to_index, j_m)
                        self.valid_push(move, True)
                break
        else:
            raise exceptions.InvalidMove(f"{move} is not a valid move.")


    def force_push(self, move):
        if self._layout[move.from_index] == ".":
            raise Exception(f"In {move.from_index} field there is no figure.")
        self._layout[move.to_index] = self._layout[move.from_index]
        self._layout[move.from_index] = "."
        if move.eat_index: self._layout[move.eat_index] = "."
        if move.promotion: self._layout[move.to_index] = self.__get_promotion(self._layout[move.to_index])

    def push(self, move):

        if self.turn and self.get(move.from_index) in ["x", "o"]:
            raise exceptions.InvalidMove(f"{move} is not a valid move.")
        elif not self.turn and self.get(move.from_index) in ["X", "O"]:
            raise exceptions.InvalidMove(f"{move} is not a valid move.")
            
#         print("here")

        self.valid_push(move)
        self.turn = not self.turn

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

    # def __check_turn(self, index):
    #     if self.turn and self.get(index) in ["o", "x"]:

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
