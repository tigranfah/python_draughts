import board
import engine

import pygame

pygame.init()

import os
import re


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


white = (255, 255, 255)
black = (0, 0, 0)

class Window:

    __instance = None

    def __init__(self, size, title):
        if Window.__instance:
            raise SingletonClass(f"{__class__.__name__} is a singleton class.")

        self.__create_window(size, title)

        self.board = board.Board()

        Window.__instance = self

    def __create_window(self, size, title):
        self.size = size
        self.root = pygame.display.set_mode(size)
        pygame.display.set_caption(title)

        self.field_size = int(size[0] / 8)

        dir_path = os.path.dirname(os.path.realpath(__file__))

        self.W_O = pygame.image.load(os.path.join(dir_path, "res", 'white_o.png'))
        self.W_X = pygame.image.load(os.path.join(dir_path, "res", 'white_x.png'))
        self.B_O = pygame.image.load(os.path.join(dir_path, "res", 'black_o.png'))
        self.B_X = pygame.image.load(os.path.join(dir_path, "res", 'black_x.png'))

        self.W_O = pygame.transform.scale(self.W_O, (self.field_size, self.field_size))
        self.W_X = pygame.transform.scale(self.W_X, (self.field_size, self.field_size))
        self.B_O = pygame.transform.scale(self.B_O, (self.field_size, self.field_size))
        self.B_X = pygame.transform.scale(self.B_X, (self.field_size, self.field_size))

    # def get_pos_by_click(self):
    #     x, y = pygame.mouse.get_pos()
    #     x = x // self.field_size
    #     y = y // self.field_size
    #     index = x + y * 8
    #     return engine.BoardBase.get_pos(index)

    def run(self):
        global WHITE
        global BLACK
        W = True

        while True:
            for even in pygame.event.get():
                if even == pygame.QUIT:
                    break

            for i in range(8):
                for j in range(8):
                    color = white if W else black
                    if j != 7: W = not W
                    pygame.draw.rect(self.root, color, (j * self.field_size, i * self.field_size,
                                                        (j + 1)*self.field_size, (i + 1)*self.field_size))

            self.draw_figure(self.board._engine.layout)

            pygame.display.flip()

            move = input()
            try:
                self.board.push(move)
            except Exception as ex:
                print(ex)

        pygame.quit()

    def draw_figure(self, figs):
        fig_dict = {
            "O" : self.W_O,
            "X" : self.W_X,
            "o" : self.B_O,
            "x" : self.B_X
        }

        for i in range(8):
            for j in range(8):
                fig = figs[j + i*8]
                if fig == ".":
                    continue
                df = fig_dict[fig]
                self.root.blit(df, (j*self.field_size, i*self.field_size))

    @staticmethod
    def get_instance():
        return Window.__instance


def test_game():
    win = Window((500, 500), "Fker")
    win.run()


if __name__ == "__main__":
    test_game()
