import sys
import engine
from engine import Move
from exceptions import SingletonClass
import copy

import preprocessing as preproc
import numpy as np


class Board:

    NUMBERS = tuple(range(8, 0, -1))
    DIGITS = tuple("abcdefgh")

    def __init__(self, net=True):
        self._engine = engine.Engine(8)

    def valid_moves(self):
        return tuple(self._engine.valid_moves())

    def push(self, str_move):
        move = Move(str_move)
        self.push_move(move)

    def push_move(self, move):
        self._engine.push(move)

    @property
    def engine(self):
        return self._engine

    def __str__(self):
        return "\n".join([f"{' '.join(self._engine.layout[i*8:i*8+8])}" for i in range(8)])

    def __repr__(self):
        return str(self)

    def show(self):
        offset = engine.BoardBase.BOARD_OFFSET
        fs = engine.BoardBase.FIELD_SIZE_IN_PIXEL
        board_img = copy.deepcopy(engine.BoardBase.BOARD_IMG)
        for i in range(8):
            for j in range(8):
                if self._engine.layout[j + i*8] == ".": continue
                fig_img = engine.BoardBase.get_figure_image(self._engine.layout[j + i*8])
                board_img.paste(fig_img, (offset + j*fs, offset + i*fs), mask=fig_img.split()[3])
        return board_img
