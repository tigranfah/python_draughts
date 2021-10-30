# import pygame


# pygame.init()

import sys
sys.path.insert(0, "./python-chess")

import chess

import engine
from engine import Move
from exceptions import SingletonClass

import enum


class Figure(enum.Enum):

    K = 0
    k = 1
    Q = 2
    q = 3
    R = 4
    r = 5
    B = 6
    b = 7
    N = 8
    n = 9
    P = 10
    p = 11


# class Window:
#
#     __instance = None
#
#     def __init__(self, size, title):
#         if Window.__instance:
#             raise SingletonClass(f"{__class__.__name__} is a singleton class.")
#
#         self.__create_window(size, title)
#
#         Window.__instance = self
#
#     def __create_window(self, size, title):
#         self.root = pygame.display.set_mode(size)
#         pygame.display.set_caption(title)
#
#     @staticmethod
#     def get_instance():
#         return Window.__instance


class Board:

    def __init__(self):
        self._engine = engine.Engine(8)

    def push(self, move):
        # out = self._engine.predict(board, move)
        print(f"Probability {out}")
        if out > 0.5:
            self.force_move(move)
            print(str(self))
        else:
            print(f"{move} is illegal move.")

    # def force_move(self, move):
    #     from_index = engine.Engine.SQUARE_NAMES.index(move.from_pos)
    #     to_index = engine.Engine.SQUARE_NAMES.index(move.to_pos)
    #     if self._engine.layout[from_index] == ".":
    #         raise Exception(f"In empty {move.from_pos} field there is no figure.")
    #     self._engine.layout[to_index] = self._engine.layout[from_index]
    #     self._engine.layout[from_index] = "."
    #
    # def evaluate(self, move):
    #     for m, opps in self._engine.is_valid(move):
    #         print(engine.Engine.SQUARE_NAMES[m])
    #         if engine.Engine.SQUARE_NAMES.index(move.to_pos) == m:
    #             self.force_move(move)


# window = Window((500, 500), "neural net engine")
board = Board()

print("Type moves")
while True:
    print(board._engine)
    move = Move(input())
    board._engine.push(move)
    # board.force_move(move)
    # board.force_move(Move("c7c5"))
