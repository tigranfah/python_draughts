import sys

import chess

import engine
from engine import Move
from exceptions import SingletonClass


class Board:

    NUMBERS = tuple(range(8, 0, -1))
    DIGITS = tuple("abcdefgh")

    def __init__(self, net=True):
        self._engine = engine.Engine(8)
#         self._engine = engine.NetEngine(8)

    # def push(self, move):
    #     print(f"Probability {out}")
    #     if out > 0.5:
    #         self.force_move(move)
    #         print(str(self))
    #     else:
    #         print(f"{move} is illegal move.")

    def valid_moves(self):
        return tuple(Move(engine.BoardBase.get_pos(f) + engine.BoardBase.get_pos(t)) for f, t in self._engine.valid_moves())

    def push(self, str_move):
        move = Move(str_move)
        self.push_move(move)

    def push_move(self, move):
        self._engine.push(move)

    def __str__(self):
        s = "\n".join([f"{' '.join(self._engine.layout[i*8:i*8+8])}" for i in range(8)])
        # s += f"\n  {' '.join(Board.DIGITS)}"
        return s

    def __repr__(self):
        return str(self)
