import time
import numpy as np
import pygame
import pygame_menu
import sys
from random import randint

pygame.init()
cell_size = 30
FPS = 10
height = 22 * cell_size
width = 10 * cell_size + 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Крестики - нолики")

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)

mutation_chance = 0.1
mutation_coef = 0.05
mutation_parametr = 0.01
cross_chance = 0.9
cross_parametr = 0.2
population = 256
iterations = 20000
tournament_count = 4
evaluation_precise = 25


class Player:
    def __init__(self):
        self.bias = np.random.randint(-2, 2, 64)
        self.weights = np.random.randint(-2, 2, (64, 64))

    def mutation(self):
        for i in range(64):
            if randint(1, 100) <= 100 * mutation_parametr:
                self.bias[i] += randint(-1, 1)
                if self.bias[i] > 10:
                    self.bias[i] = 10
                if self.bias[i] < -10:
                    self.bias[i] = -10

            for j in range(64):
                if randint(1, 100) <= 100 * mutation_parametr:
                    self.weights[i][j] += randint(-5, 5)
                    if self.weights[i][j] > 100:
                        self.weights[i][j] = 100
                    if self.weights[i][j] < -100:
                        self.weights[i][j] = -100

    def predict(self, input_values):
        return np.dot(input_values, self.weights) + self.bias


linear_bot = Player()
with open('LinearAI/_player1_weights.txt', 'r') as file:
    linear_bot.weights = np.loadtxt(file)
with open('LinearAI/_player1_bias.txt', 'r') as file:
    linear_bot.bias = np.loadtxt(file)


def array_to_line(array):
    line = []
    for k in range(4):
        for i in range(4):
            for j in range(4):
                line.append(array[k][i][j])
    return line


def line_to_array(pos):
    position__ = (([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
                  ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
                  ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
                  ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]))

    counter = 0

    for k in range(4):
        for i in range(4):
            for j in range(4):
                position__[k][i][j] = pos[counter]
                counter += 1

    return position__


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


def move_ai():
    line = array_to_line(position)
    if current_player[0] == 1:
        res1 = linear_bot.predict(line)
        while line[np.argmax(res1)] != 0:
            res1[np.argmax(res1)] = float('-inf')

        index = np.argmax(res1)
        print(index)

        counter_ = 0
        for k_ in range(4):
            for i_ in range(4):
                for j_ in range(4):
                    if index == counter_:
                        position[k_][i_][j_] = 1
                        counter_ += 1
                        break
                    counter_ += 1
        current_player[0] = -1


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
                        current_player[0] = -1
                    else:
                        current_player[0] = 1


def draw_figure(n, x_, y_):
    if n == 1:
        pygame.draw.line(screen, RED, (x_, y_), (x_ + cell_size, y_ + cell_size), 7)
        pygame.draw.line(screen, RED, (x_ + cell_size, y_), (x_, y_ + cell_size), 7)

    if n == -1:
        pygame.draw.circle(screen, YELLOW, (x_ + cell_size // 2, y_ + cell_size // 2), cell_size // 2, 7)


class Button:
    def __init__(self, color, x, y, w, h, surface, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text
        self.surface = surface

    def show(self):
        # Call this method to draw the button on the screen

        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('arial', 36)
            text = font.render(self.text, True, BLACK)
            self.surface.blit(text,
                              (self.x + (self.width // 2 + text.get_width() // 2),
                               self.y + (self.height // 2 + text.get_height() // 2)))

    def is_pressed(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if (pos[0] > self.x) and pos[0] < self.x + self.width:
            if pos[1] > self.y and (pos[1] < self.y + self.height):
                return True
        return False


class CheckWin:
    def __init__(self):
        self.who_wins = ''
        self.win = False

    def check(self):
        for k in range(4):
            for i in range(4):
                for j in range(4):

                    if position[k][0][0] == position[k][1][1] == position[k][2][2] == position[k][3][3] != 0:
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[k][3][0] == position[k][2][1] == position[k][1][2] == position[k][0][3] != 0:
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[k][0][j] == position[k][1][j] == position[k][2][j] == position[k][3][j] != 0:
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[k][i] == [1, 1, 1, 1] or position[k][i] == [-1, -1, -1, -1]:
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[0][i][j] == position[1][i][j] == position[2][i][j] == position[3][i][j] != 0:
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[0][i][0] == position[1][i][1] == position[2][i][2] == position[3][i][3] != 0:
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[3][i][0] == position[2][i][1] == position[1][i][2] == position[0][i][3] != 0:
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[0][0][j] == position[1][1][j] == position[2][2][j] == position[3][3][j] != 0:
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[3][0][j] == position[2][1][j] == position[1][2][j] == position[0][3][j] != 0:
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[0][0][0] == position[1][1][1] == position[2][2][2] == position[3][3][3] != 0:
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[3][0][0] == position[2][1][1] == position[1][2][2] == position[0][3][3] != 0:
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[0][0][3] == position[1][1][2] == position[2][2][1] == position[3][3][0] != 0:
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

                    if position[0][3][0] == position[1][2][1] == position[2][1][2] == position[3][0][3] != 0:
                        if current_player[0] == 1:
                            self.who_wins = 'Circle wins'
                        else:
                            self.who_wins = 'Cross wins'
                        self.win = True

    def message(self):
        if self.win:
            font = pygame.font.Font(None, 56)
            text = font.render(self.who_wins, True, BLUE)
            screen.blit(text, (10 * (cell_size + 1), 180))


class Render(object):
    def __init__(self):
        self.win = False
        self.pos = position
        self.message = ''
        self.who_wins = ''

    def draw(self):
        for k in range(4):
            for i in range(4):
                for j in range(4):
                    counter___ = 0

                    f1 = pygame.font.Font(None, 25)
                    text1 = f1.render(str(counter___), True, (180, 0, 0))
                    screen.blit(text1, (cell_size * i + 2 * (3 - k) * cell_size, cell_size * j + 6 * cell_size * k,
                                        cell_size,
                                        cell_size))
                    counter___ += 1

                    pygame.draw.rect(screen, BLACK,
                                     (cell_size * i + 2 * (3 - k) * cell_size, cell_size * j + 6 * cell_size * k,
                                      cell_size,
                                      cell_size), 2)
                    draw_figure(position[k][i][j], 2 * (3 - k) * cell_size + cell_size * i,
                                cell_size * j + 6 * k * cell_size)

    def game_over(self):
        if self.win is True:
            start()
            screen.fill(GREEN)
            message1 = text_font.render(self.message, True, BLUE)
            message2 = text_font.render(self.who_wins, True, BLUE)
            screen.blit(message1, (width // 2 - 160, height // 2))
            screen.blit(message2, (width // 2 - 160, height // 2 + 30))
            pygame.display.update()
            time.sleep(5)


pygame.font.init()
text_font = pygame.font.Font(None, 55)

clock = pygame.time.Clock()


def start_with_ai():
    current_player[0] = 1
    render = Render()
    check_win = CheckWin()
    frame_count = ''
    finished = False
    while not finished:
        clock.tick(FPS)
        move_ai()
        if current_player[0] == 1:
            frame_count = "Ход компьютера"
        if current_player[0] == -1:
            frame_count = "Ваш ход"
        text_image = text_font.render(str(frame_count), True, BLUE)
        text_x = 10 * (cell_size + 1)
        text_y = 20
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not finished:
                click(event)
        screen.fill(CYAN)
        screen.blit(text_image, (text_x, text_y))
        render.draw()
        check_win.check()
        check_win.message()
        keys = pygame.key.get_pressed()
        if render.win is True or keys[pygame.K_p]:
            break
        pygame.display.update()


def start_the_game():
    render = Render()
    check_win = CheckWin()
    frame_count = ''
    finished = False
    while not finished:
        clock.tick(FPS)
        if current_player[0] == 1:
            frame_count = "Ход крестиков"
        if current_player[0] == -1:
            frame_count = "Ход ноликов"
        text_image = text_font.render(str(frame_count), True, BLUE)
        text_x = 10 * (cell_size + 1)
        text_y = 20
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not check_win.win:
                click(event)
        screen.fill(CYAN)
        screen.blit(text_image, (text_x, text_y))
        render.draw()
        check_win.check()
        check_win.message()
        keys = pygame.key.get_pressed()
        if render.win is True or keys[pygame.K_p]:
            break
        pygame.display.update()


def help_():
    hint = True
    button = Button(BLUE, width - 40, height + 20, 80, 40, screen, 'Back')
    screen.fill(GREEN)
    font = pygame.font.SysFont('arial', 36)
    message = font.render("Press 'p' key to return to the menu", True, BLUE)
    screen.blit(message, (width // 2 - 200, height // 2))
    button.show()
    pygame.display.update()
    while hint:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button.is_pressed(event.pos):
                        hint = False
                        break
        clock.tick(FPS)
        pygame.display.update()


menu = pygame_menu.Menu('Tic Tac Toe', width, height,
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add.button('Игра с ботом', start_with_ai)
menu.add.button('Игра с человеком', start_the_game)
menu.add.button('Помощь', help_)
menu.add.button('Выход', pygame_menu.events.EXIT)

while True:

    events = pygame.event.get()
    for eve in events:
        if eve.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
