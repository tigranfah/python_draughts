import numpy as np


unique_cells = sorted(set("""
r n b q k b n r
p p p p . p p p
. . . . . . . .
. . . . p . . .
. . . . P . . .
. . . . . N . .
P P P P . P P P
R N B Q K B . R"""))

unique_cells.remove("\n")
unique_cells.remove(" ")

unique_figures = np.array(list(set([x.upper() for x in unique_cells[1:]])))


fig_dict = {n : i for i, n in enumerate(unique_cells)}
num_dict = {i : n for i, n in enumerate(unique_cells)}


def fig_to_num(f): return fig_dict[f]
def num_to_fig(n): return num_dict[n]


def board_to_input(board):
    inp = []
    board = str(board).replace("\n", '').replace(" ", '')
    board.replace(" ", '')
    for s in board:
        inp.append(fig_to_num(s))
    return inp


def input_to_board(inp):
    board = []
    for n in inp:
        board.append(num_to_fig(n))
    return np.array(board).reshape(8, 8)


board_pos_dict = {p : n for n, p in enumerate("abcdefgh")}
num_pos_dict = {n : p for n, p in enumerate("abcdefgh")}


def board_pos_to_num_pos(b_pos):
    return np.array([8 - int(b_pos[1]), board_pos_dict[b_pos[0]]])

def num_pos_to_board_pos(pos):
    return f"{num_pos_dict[pos[1]]}{8 - pos[0]}"


def move_to_output(board, uci_move):
    output = np.zeros(4)
    from_pos = board_pos_to_num_pos(uci_move[:2])
    to_pos = board_pos_to_num_pos(uci_move[2:])
    
    # set the pos
    output[:2] = from_pos
    output[2:] = to_pos
    return output