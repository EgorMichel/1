import pygame
from random import randint
import time

pygame.init()
FPS = 10
screen = pygame.display.set_mode((600, 600))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)

cell_size = 70

position = (([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
            ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
            ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
            ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]))

current_player = [1]


# def check_win():
#     # floors:
#     for k in range(4):


def click(event_):
    for k in range(4):
        for i in range(4):
            for j in range(4):

                if event_.button == 2:
                    for k1 in range(4):
                        for i2 in range(4):
                            for j3 in range(4):
                                position[k1][i2][j3] = 0
                                current_player[0] = 1

                if 0.75 * i + cell_size * i < event_.pos[0] < 0.75 * i + cell_size * (i + 1) and \
                        0.5 * j + cell_size * j + k * 120 < event_.pos[1] < 0.5 * j + cell_size * (j + 1) + k * 120:
                    if event_.button == 1 and position[k][i][j] == 0:
                        position[k][i][j] = current_player[0]
                    elif event_.button == 3:
                        position[k][i][j] = 0

                    if current_player[0] == 1:
                        current_player[0] = 2
                    else:
                        current_player[0] = 1


def draw_figure(n, x_, y_):
    if n == 1:
        pygame.draw.line(screen, RED, (x_, y_), (x_ + 0.5 * cell_size, y_ + 0.5 * cell_size), 2)
        pygame.draw.line(screen, RED, (x_ + 0.5 * cell_size, y_), (x_, y_ + 0.5 * cell_size), 2)

    if n == 2:
        pygame.draw.circle(screen, YELLOW, (x_ + cell_size // 2, y_ + cell_size // 2), cell_size // 3, 2)


# position = (([1, 1, 1, 1], [1, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1]),
#             ([1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
#             ([1, 0, 1, 0], [0, 0, 0, 0], [1, 0, 1, 0], [0, 0, 0, 0]),
#             ([1, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 1]))

def draw():
    for k in range(4):
        pygame.draw.polygon(screen, BLACK, ((0, cell_size * (2 + 2 * k)),
                                            (1.5 * cell_size, cell_size * (0.5 + 2 * k)),
                                            (4.5 * cell_size, cell_size * (0.5 + 2 * k)),
                                            (3 * cell_size, cell_size * (2 + 2 * k))), 2)
        for i in range(4):
            for j in range(4):

                if position[k][0][0] == position[k][1][1] == position[k][2][2] == position[k][3][3] != 0:
                    print('Horizontal diagonal left to right')

                if position[k][3][0] == position[k][2][1] == position[k][1][2] == position[k][0][3] != 0:
                    print('Horizontal diagonal right to left')

                if position[k][0][j] == position[k][1][j] == position[k][2][j] == position[k][3][j] != 0:
                    print('Horizontal line')

                if position[k][i] == [1, 1, 1, 1] or position[k][i] == [2, 2, 2, 2]:
                    print('Horizontal column')

                if position[0][i][j] == position[1][i][j] == position[2][i][j] == position[3][i][j] != 0:
                    print('Vertical line')

                if position[0][i][0] == position[1][i][1] == position[2][i][2] == position[3][i][3] != 0:
                    print('Vertical diagonal left to right')

                if position[3][i][0] == position[2][i][1] == position[1][i][2] == position[0][i][3] != 0:
                    print('Vertical diagonal right to left')

                if position[0][0][j] == position[1][1][j] == position[2][2][j] == position[3][3][j] != 0:
                    print('Vertical diagonal 2 left to right')

                if position[3][0][j] == position[2][1][j] == position[1][2][j] == position[0][3][j] != 0:
                    print('Vertical diagonal 2 right to left')

                if position[0][0][0] == position[1][1][1] == position[2][2][2] == position[3][3][3] != 0:
                    print('Main diagonal 1')

                if position[3][0][0] == position[2][1][1] == position[1][2][2] == position[0][3][3] != 0:
                    print('Main diagonal 2')

                if position[0][0][3] == position[1][1][2] == position[2][2][1] == position[3][3][0] != 0:
                    print('Main diagonal 3')

                if position[0][3][0] == position[1][2][1] == position[2][1][2] == position[3][0][3] != 0:
                    print('Main diagonal 4')

                draw_figure(position[k][i][j], cell_size * i, cell_size * j + 120 * k)


clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    screen.fill(BLUE)
    draw()
    pygame.display.update()
