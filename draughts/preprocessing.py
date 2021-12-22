import numpy as np


import engine


unique_cells = { cell : v for v, cell in enumerate(".oOxX") }
unique_values = { v : cell for v, cell in enumerate(".oOxX") }


def cell_to_value(cell):
    return unique_cells[cell]


def value_to_cell(value):
    return unique_values[value]


def board_layout_to_network_input(board_layout):
    array = []

    for cell in board_layout:
        base = np.zeros(5)
        base[cell_to_value(cell)] = 1
        array.append(base)

    return np.array(array).reshape(8, 8, 5).astype(np.int8)


def network_input_to_board_layout(inp):
    layout = []
    for values in inp:
        for bin_val in values:
            layout.append(value_to_cell(bin_val.argmax()))
        
    return layout


def move_to_network_output(move):
    from_in_base = np.zeros(64)
    from_in_base[move.from_index] = 1

    to_in_base = np.zeros(64)
    to_in_base[move.to_index] = 1

    return np.array([*from_in_base, *to_in_base]).astype(np.int8)


def network_output_to_move(output):
    from_index = output[:64].argmax()
    to_index = output[64:].argmax()
    return engine.Move.from_indices(from_index, to_index)


# if __name__ == "__main__":
    # print(cell_to_value("x"))
    # print(board_to_network_input())
