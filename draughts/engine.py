from PIL import Image

import os
import copy
import sys
import enum

import exceptions


class GameState(enum.Enum):

    WHITE_WON = 1
    BLACK_WON = 2
    INDETERMINATE = 3


class Move:

    def __init__(self, str_move, eat_index=None, promotion=False):
        if not type(str_move) is str: raise ValueError(f"{str_move} must be a string.")

        if str_move == "":
            self.empty = True
        else:
            self.empty = False

        if not self.empty and len(str_move) != 4: raise ValueError(f"{str_move} must have 4 character.")

        # position info

        if self.empty:
            self.from_pos = ""
            self.to_pos = ""
            self.from_index = None
            self.to_index = None
        else:
            self.from_pos = str_move[0:2]
            self.to_pos = str_move[2:4]
            self.from_index = BoardBase.get_index(self.from_pos)
            self.to_index = BoardBase.get_index(self.to_pos)

        # eat info
        self.eat_index = eat_index
        self.eatten_fig = None

        # promotion info
        self.promotion = promotion

    @staticmethod
    def from_indices(from_ind, to_ind):
        return Move(f"{BoardBase.get_pos(from_ind)}{BoardBase.get_pos(to_ind)}")

    def __eq__(self, other):
        if self.from_pos == other.from_pos and self.to_pos == other.to_pos:
            return True
        return False

    def __str__(self):
        if self.empty: return "Move( '' )"
        return "Move( " + self.from_pos + self.to_pos + " )"

    def __repr__(self):
        return str(self)


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


class EngineBase:

    def __init__(self, size):
        self.size = size
        self.__init_engine()

    def __init_engine(self):
        self.turn = True
        self._layout = BoardBase.get_default_layout()
        self._move_stack = []
        self._fig_count = {}
        self.update_figure_count()

    def force_push(self, move):
        if move.empty: return

        self._layout[move.to_index] = self._layout[move.from_index]
        self._layout[move.from_index] = BoardBase.E
        if move.eat_index:
            move.eatten_fig = self._layout[move.eat_index]
            self._layout[move.eat_index] = BoardBase.E
        if move.promotion: self._layout[move.to_index] = self.get_promotion(self._layout[move.to_index])

    def force_undo(self, move):
        if move.empty: return

        if move.promotion:
            self._layout[move.to_index] = self.get_promotion(self._layout[move.to_index])

        self._layout[move.from_index] = self._layout[move.to_index]
        self._layout[move.to_index] = BoardBase.E

        if move.eat_index:
            self._layout[move.eat_index] = move.eatten_fig

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
            BoardBase.W : BoardBase.BLACK,
            BoardBase.WQ : BoardBase.BLACK,
            BoardBase.B : BoardBase.WHITE,
            BoardBase.BQ : BoardBase.WHITE
        }[fig]

    def get_promotion(self, fig):
        return {
            BoardBase.W : BoardBase.WQ,
            BoardBase.B : BoardBase.BQ,
            BoardBase.WQ : BoardBase.W,
            BoardBase.BQ : BoardBase.B
        }[fig]

    def is_promoted(self, from_index, index):
        if not self.get(from_index) in [BoardBase.W, BoardBase.B]: return False
        if 0 <= index < self.size or self.size**2-self.size <= index < self.size**2:
            return True
        return False

    def reset(self):
        self.__init_engine()

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, lay):
        self._layout = lay


class Engine(EngineBase):

    def __init__(self, size):
        EngineBase.__init__(self, size)
        self._current_valid_moves = self.get_valid_moves()

    def get_valid_moves(self, jump=False):
        figs = BoardBase.WHITE if self.turn else BoardBase.BLACK
        all_moves = []
        valid_moves = []
        for i in range(self.size**2):
            if self.get(i) in figs:
                for move in self.valid_moves_from_pos(BoardBase.get_pos(i), jump):
                    if move.eat_index: valid_moves.append(move)
                    all_moves.append(move)
        return valid_moves if valid_moves else all_moves

    def valid_moves_from_pos(self, from_pos, jump=False):
        from_index = BoardBase.get_index(from_pos)
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
                        valid_moves.append(Move(from_pos+BoardBase.get_pos(index), None,
                                                self.is_promoted(from_index, index)))
                    elif self.get(index) in self.get_opposite_figs(fig):
                        if self.get_index(from_index, x*2, y*2):
                            jump_index = self.get_index(from_index, x*2, y*2)
                            if self.get(jump_index) == BoardBase.E:
                                valid_moves.append(Move(from_pos+BoardBase.get_pos(jump_index), index,
                                                        self.is_promoted(from_index, jump_index)))

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
                            valid_moves.append(Move(from_pos+BoardBase.get_pos(index), opposite_fig,
                                                    self.is_promoted(from_index, index)))

                        elif self.get(index) in self.get_opposite_figs(fig):
                            if opposite_fig:
                                break
                            only_jump = False
                            opposite_fig = index

        return valid_moves

    def valid_push(self, move):

        if not move.empty:
            if self.turn and self.get(move.from_index) in BoardBase.BLACK:
                raise exceptions.InvalidMove(f"{move} is not a valid move.")
            elif not self.turn and self.get(move.from_index) in BoardBase.WHITE:
                raise exceptions.InvalidMove(f"{move} is not a valid move.")

        for m in self._current_valid_moves:
            if m == move:
                self.force_push(m)
                self.add_to_move_stack(m)

                if not m.eat_index is None and self.valid_moves_from_pos(move.to_pos, True):
                    self._current_valid_moves = [Move(""), *self.valid_moves_from_pos(move.to_pos, True)]
                else:
                    self.turn = not self.turn
                    self._current_valid_moves = self.get_valid_moves(False)
                break
        else:
            raise exceptions.InvalidMove(f"{move} is not a valid move.")

    def undo(self):
        for move in self._move_stack[-1][::-1]:
            self.force_undo(move)
        self.remove_from_move_stack()

    def push(self, move):

        self.valid_push(move)
        self.update_figure_count()

    def update_figure_count(self):
        self._fig_count = {BoardBase.W : 0, BoardBase.B : 0,
                           BoardBase.WQ : 0, BoardBase.BQ : 0,
                           BoardBase.E : 0 }
        for cell in self._layout:
            if self._fig_count[cell] == 0:
                self._fig_count[cell] = 1
            else:
                self._fig_count[cell] += 1

    def evaluate(self):
        return self._fig_count[BoardBase.W] - self._fig_count[BoardBase.B] + 3 * (self._fig_count[BoardBase.WQ] - self._fig_count[BoardBase.BQ])

    def is_draw(self):
        if self._fig_count[BoardBase.WQ] == 1 and self._fig_count[BoardBase.BQ] == 1:
            for move in self.valid_moves():
                if move.eat_index != None:
                    return True
        return False

    def is_finished(self):
        if len(self.valid_moves()) == 0:
            if self.turn: return GameState.BLACK_WON
            elif not self.turn: return GameState.WHITE_WON
        if self._fig_count[BoardBase.B] == 0 and self._fig_count[BoardBase.BQ] == 0:
            return GameState.WHITE_WON
        elif self._fig_count[BoardBase.W] == 0 and self._fig_count[BoardBase.WQ] == 0:
            return GameState.BLACK_WON

        return GameState.INDETERMINATE

    def valid_moves(self):
        return self._current_valid_moves

    def add_to_move_stack(self, move):
        if self._move_stack and (self._move_stack[-1][-1].to_index == move.from_index or move.empty):
            self._move_stack[-1].append(move)
        else:
            self._move_stack.append(list([move]))

    def remove_from_move_stack(self):
        self._move_stack.pop()


# class AIMovePicker:
#
#     def __init__(self, board):
#         self._board = board
#
#     def grid_search(self):
#         for self.board.valid_moves():
