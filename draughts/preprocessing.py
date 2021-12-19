import numpy as np


unique_cells = { cell : v for v, cell in enumerate(".oOxX") }


def cell_to_value(cell):
    return unique_cells.get(cell)


def board_layout_to_network_input(board_layout):
    array = []

    for cell in board_layout:
        base = np.zeros(5)
        base[cell_to_value(cell)] = 1
        array.append(base)

    return np.array(array).reshape(8, 8, 5)


# if __name__ == "__main__":
    # print(cell_to_value("x"))
    # print(board_to_network_input())
