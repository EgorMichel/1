import time

import pygame
import pygame_menu
import sys

pygame.init()
FPS = 10
screen = pygame.display.set_mode((580, 500))
pygame.display.set_caption("Крестики - нолики")
logo = pygame.image.load("4-Pack-Tic-Tac-Toe-Game-Board-and-X-O-Silicone-Molds-Set-Epoxy-Resin-Craft.jpg")

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)

cell_size = 23

position = (([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
            ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
            ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
            ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]))


def start():
    global position
    position = (([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
                ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
                ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
                ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]))


start()
current_player = [1]


def click(event_):
    for k in range(4):
        for i in range(4):
            for j in range(4):

                if event_.button == 2:
                    for k1 in range(4):
                        for i2 in range(4):
                            for j3 in range(4):
                                position[k1][i2][j3] = 0
                                current_player[0] = 0

                if 2 * (3 - k) * cell_size + cell_size * i < event_.pos[0] < 2 * (3 - k) * cell_size + cell_size * (
                        i + 1) and \
                        cell_size * j + k * 6 * cell_size < event_.pos[1] < cell_size * (j + 1) + k * cell_size * 6:
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
        pygame.draw.line(screen, RED, (x_, y_), (x_ + cell_size, y_ + cell_size), 7)
        pygame.draw.line(screen, RED, (x_ + cell_size, y_), (x_, y_ + cell_size), 7)

    if n == 2:
        pygame.draw.circle(screen, YELLOW, (x_ + cell_size // 2, y_ + cell_size // 2), cell_size // 2, 7)


class Draw(object):
    def __init__(self):
        self.win = False
        self.pos = position
        self.message = ''
        self.who_wins = ''

    def draw(self):

        for k in range(4):
            for i in range(4):
                for j in range(4):

                    if position[k][0][0] == position[k][1][1] == position[k][2][2] == position[k][3][3] != 0:
                        if self.win is False:
                            self.message = 'Horizontal diagonal left to right'
                        self.win = True

                    if position[k][3][0] == position[k][2][1] == position[k][1][2] == position[k][0][3] != 0:
                        if self.win is False:
                            self.message = 'Horizontal diagonal right to left'
                        self.win = True

                    if position[k][0][j] == position[k][1][j] == position[k][2][j] == position[k][3][j] != 0:
                        if self.win is False:
                            self.message = 'Horizontal line'
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[k][i] == [1, 1, 1, 1] or position[k][i] == [2, 2, 2, 2]:
                        if self.win is False:
                            self.message = 'Horizontal column'
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[0][i][j] == position[1][i][j] == position[2][i][j] == position[3][i][j] != 0:
                        if self.win is False:
                            self.message = 'Vertical line'
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[0][i][0] == position[1][i][1] == position[2][i][2] == position[3][i][3] != 0:
                        if self.win is False:
                            self.message = 'Vertical diagonal left to right'
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[3][i][0] == position[2][i][1] == position[1][i][2] == position[0][i][3] != 0:
                        if self.win is False:
                            self.message = 'Vertical diagonal right to left'
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[0][0][j] == position[1][1][j] == position[2][2][j] == position[3][3][j] != 0:
                        if self.win is False:
                            self.message = 'Vertical diagonal 2 left to right'
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[3][0][j] == position[2][1][j] == position[1][2][j] == position[0][3][j] != 0:
                        if self.win is False:
                            self.message = 'Vertical diagonal 2 right to left'
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[0][0][0] == position[1][1][1] == position[2][2][2] == position[3][3][3] != 0:
                        if self.win is False:
                            self.message = 'Main diagonal 1'
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[3][0][0] == position[2][1][1] == position[1][2][2] == position[0][3][3] != 0:
                        if self.win is False:
                            self.message = 'Main diagonal 2'
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[0][0][3] == position[1][1][2] == position[2][2][1] == position[3][3][0] != 0:
                        if self.win is False:
                            self.message = 'Main diagonal 3'
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[0][3][0] == position[1][2][1] == position[2][1][2] == position[3][0][3] != 0:
                        if self.win is False:
                            self.message = 'Main diagonal 4'
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    pygame.draw.rect(screen, BLACK,
                                     (cell_size * i + 2 * (3 - k) * cell_size, cell_size * j + 6 * cell_size * k,
                                      cell_size,
                                      cell_size), 2)
                    draw_figure(position[k][i][j], 2 * (3 - k) * cell_size + cell_size * i,
                                cell_size * j + 6 * k * cell_size)


pygame.font.init()
text_font = pygame.font.Font(None, 60)

clock = pygame.time.Clock()


def start_the_game():
    draw = Draw()
    frame_count = 0
    finished = False
    while not finished:
        clock.tick(FPS)
        if current_player[0] == 1:
            frame_count = "Ход крестиков"
        if current_player[0] == 2:
            frame_count = "Ход ноликов"
        text_image = text_font.render(str(frame_count), True, WHITE)
        text_x = 250
        text_y = 20
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not finished:
                click(event)
        screen.fill(BLUE)
        screen.blit(text_image, (text_x, text_y))
        draw.draw()
        if draw.win is True:
            draw.win = False
            start()
            screen.fill(GREEN)
            message1 = text_font.render(draw.message, True, WHITE)
            message2 = text_font.render(draw.who_wins, True, WHITE)
            screen.blit(message1, (150, 210))
            screen.blit(message2, (180, 250))
            pygame.display.update()
            time.sleep(5)
            break
        pygame.display.update()


menu = pygame_menu.Menu('Tic Tac Toe', 320, 280,
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Имя игрока :', default='Игрок 1')
menu.add.button('Игра с ботом', start_the_game)
menu.add.button('Игра с человеком', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

while True:

    screen.blit(logo, (0, 0))

    events = pygame.event.get()
    for eve in events:
        if eve.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
