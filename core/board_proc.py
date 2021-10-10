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


def binary_4bits(x):
    return {
        0 : [0, 0, 0, 0],
        1 : [0, 0, 0, 1],
        2 : [0, 0, 1, 0],
        3 : [0, 0, 1, 1],
        4 : [0, 1, 0, 0],
        5 : [0, 1, 0, 1],
        6 : [0, 1, 1, 0],
        7 : [0, 1, 1, 1],
        8 : [1, 0, 0, 0],
        9 : [1, 0, 0, 1],
        10 : [1, 0, 1, 0],
        11 : [1, 0, 1, 1],
        12 : [1, 1, 0, 0],
    }[x]


def binary_3bits(x):
    return {
        0 : [0, 0, 0],
        1 : [0, 0, 1],
        2 : [0, 1, 0],
        3 : [0, 1, 1],
        4 : [1, 0, 0],
        5 : [1, 0, 1],
        6 : [1, 1, 0],
        7 : [1, 1, 1],
    }[x]


def to_decimal(x):
    bits = [1 if x_ >= 0.5 else 0 for x_ in x]
    if len(bits) == 3:
        for i in range(0, 8):
          if np.all(binary_3bits(i) == bits):
            return i
    elif len(bits) == 4:
        for i in range(0, 13):
          if np.all(binary_4bits(i) == bits):
            return i

def dist2d(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)


if __name__ == "__main__":
    print(to_decimal([1, 1, 0, 0]))
    print(to_decimal([1, 0, 0, 0]))
    print(to_decimal([1, 0, 0]))
    print(to_decimal([1, 1, 1]))
    print(binary_3bits(7))
    print(binary_4bits(8))
    print(dist2d(0, 0, 1, 1))
