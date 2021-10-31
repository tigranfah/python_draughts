import board


def multi_eating():
    b = board.Board()
    b.push_move("c3d4")
    b.push_move("d6c5")
    b.push_move("b2c3")
    b.push_move("f6e5")
    b.push_move("g3h4")
    b.push_move("h6g5")
    b.push_move("b4d6 g3")
    print(b)

    # black
    # b.push_move("e3d4")
    # b.push_move("d6c5")
    # b.push_move("g3f4")
    # b.push_move("c5e3")
    # b.push_move("e3d4")
    # b.push_move("h2g3")
    # b.push_move("b6c5")
    # b.push_move("g1h2")
    # b.push_move("e3g1")


def multi_eating_queen():
    b = board.Board()
    b.push_move("e3d4")
    b.push_move("f6e5")
    b.push_move("d4f6")
    b.push_move("d6e5")
    b.push_move("g3f4")
    b.push_move("c7d6")
    b.push_move("h2g3")
    b.push_move("d8c7")
    b.push_move("g3h4")
    b.push_move("b6c5")
    b.push_move("f6d8 a5")
    print(b)
