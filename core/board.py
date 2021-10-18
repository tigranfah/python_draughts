# import pygame


# pygame.init()

import sys
sys.path.insert(0, "./python-chess")

import chess

import engine
from engine import UCIMove
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


class Window:

    __instance = None

    def __init__(self, size, title):
        if Window.__instance:
            raise SingletonClass(f"{__class__.__name__} is a singleton class.")

        self.__create_window(size, title)

        Window.__instance = self

    def __create_window(self, size, title):
        self.root = pygame.display.set_mode(size)
        pygame.display.set_caption(title)

    @staticmethod
    def get_instance():
        return Window.__instance


class Board:

    DEFAULT_LAYOUT = list("rnbqkbnrpppppppp................................PPPPPPPPRNBQKBNR")
    SQUARE_NAMES = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
                    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
                    'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
                    'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
                    'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
                    'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
                    'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
                    'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']

    def __init__(self):
        self._board_layout = Board.DEFAULT_LAYOUT
        self._engine = engine.Engine("model")

    def push_uci(self, uci_move):
        out = self._engine.predict(board, uci_move)
        if out > 0:
            self.force_move(uci_move)
            print(str(self))
        else:
            print(f"{uci_move} is illegal move.")

    def force_move(self, uci_move):
        from_index = Board.SQUARE_NAMES.index(uci_move.from_pos)
        to_index = Board.SQUARE_NAMES.index(uci_move.to_pos)
        if self._board_layout[from_index] == ".":
            raise Exception(f"In empty {uci_move.from_pos} field there is no figure.")
        self._board_layout[to_index] = self._board_layout[from_index]
        self._board_layout[from_index] = "."

    def __str__(self):
        return "\n".join([f"{' '.join(self._board_layout[i*8:i*8+8])}" for i in range(8)])

    def __repr__(self):
        return str(self)


# window = Window((500, 500), "neural net engine")
board = Board()

print("Type moves")
while True:
    move = UCIMove(input())
    board.push_uci(move)
    # board.force_move(UCIMove("c7c5"))
print(board)
