#! /usr/local/bin/python3

import sys
import os

sys.path.insert(1, './python-chess')

import chess

board = chess.Board()

print(chess.Move.from_uci("a8a1") in board.legal_moves)
print(board.push_san("e4"))
print(board.push_san("e5"))
print(board.is_checkmate())

print(board)
