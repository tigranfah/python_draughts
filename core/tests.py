import board

b = board.Board()


def multi_eating():
    b.push_move("c3d4")
    b.push_move("d6c5")
    b.push_move("b2c3")
    b.push_move("f6e5")
    b.push_move("g3h4")
    b.push_move("h6g5")
    b.push_move("b4d6 g3")
    print("Sucess.")
