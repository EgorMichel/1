# -*- coding: utf-8 -*-
"""4x4x4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lMKKhQ3efZly5vcO0k90fjB09IW_cYUL
"""

import numpy as np
import matplotlib.pyplot as plt
import numpy.random
from random import randint
import random


def line_to_array(pos):
    position = (([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
                ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
                ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
                ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]))

    counter_ = 0

    for k in range(4):
        for i in range(4):
            for j in range(4):
                position[k][i][j] = pos[counter_]
                counter_ += 1

    return position


def check_win(pos):
    if 0 not in pos:
        return True

    position = line_to_array(pos)

    for k in range(4):
        for i in range(4):
            for j in range(4):
                if position[k][0][0] == position[k][1][1] == position[k][2][2] == position[k][3][3] != 0 \
                        or position[k][3][0] == position[k][2][1] == position[k][1][2] == position[k][0][3] != 0 \
                        or position[k][0][j] == position[k][1][j] == position[k][2][j] == position[k][3][j] != 0 \
                        or position[k][i] == [1, 1, 1, 1] or position[k][i] == [2, 2, 2, 2] \
                        or position[0][i][j] == position[1][i][j] == position[2][i][j] == position[3][i][j] != 0 \
                        or position[0][i][0] == position[1][i][1] == position[2][i][2] == position[3][i][3] != 0 \
                        or position[3][i][0] == position[2][i][1] == position[1][i][2] == position[0][i][3] != 0 \
                        or position[0][0][j] == position[1][1][j] == position[2][2][j] == position[3][3][j] != 0 \
                        or position[3][0][j] == position[2][1][j] == position[1][2][j] == position[0][3][j] != 0 \
                        or position[0][0][0] == position[1][1][1] == position[2][2][2] == position[3][3][3] != 0 \
                        or position[3][0][0] == position[2][1][1] == position[1][2][2] == position[0][3][3] != 0 \
                        or position[0][0][3] == position[1][1][2] == position[2][2][1] == position[3][3][0] != 0 \
                        or position[0][3][0] == position[1][2][1] == position[2][1][2] == position[3][0][3] != 0:
                    return True
    return False


class Player:
    def __init__(self, parent=0, analog=0):
        self.changed_elements = [[-1, -1]] * 128
        self.bias = [0] * 64
        self.weights = [[0] * 64] * 64
        if parent == 0:
            self.weights = np.random.randint(-10000, 10000, (64, 64)) / 10000
            self.bias = np.random.randint(-10000, 10000, 64) / 10000

        if parent != 0 and analog == 0:

            for i in range(len(parent.bias)):
                self.bias[i] = parent.bias[i]
                for j in range(len(parent.weights[i])):
                    self.weights[i][j] = parent.weights[i][j]

            for i in range(8):
                self.bias[randint(0, 63)] += (randint(-50000, 50000) / 10000)

            for i in range(32):

                self.changed_elements[i] = [randint(0, 63), randint(0, 63)]

            for elem in self.changed_elements:
                self.weights[elem[0]][elem[1]] += (randint(-50000, 50000) / 10000)

        if analog != 0:
            self.bias = analog.bias
            self.weights = analog.weights
            self.changed_elements = analog.changed_elements

    def predict(self, x):
        return np.dot(x, self.weights) + self.bias


def cross(p1, p2):
    if p1.changed_elements[0][0] == p2.changed_elements[0][0] == -1:
        return p1

    p3 = Player(0, p2)
    p3.bias = p1.bias
    p3.changed_elements = p1.changed_elements

    for element in p1.changed_elements:
        p3.weights[element[0]][element[1]] = p1.weights[element[0]][element[1]]

    return p3


def game(p1, p2):
    position = np.zeros(64)

    while not check_win(position):
        res1 = p1.predict(position)
        while position[np.argmax(res1)] != 0:
            res1[np.argmax(res1)] = -999999
        position[np.argmax(res1)] = 1
        if check_win(position):
            return p1

        res2 = p2.predict((-1) * position)
        while position[np.argmax(res2)] != 0:
            res2[np.argmax(res2)] += -999999

        position[np.argmax(res2)] = -1

    return p2


def game_with_comments(p1, p2):
    position = np.zeros(64)

    while not check_win(position):
        res1 = p1.predict(position)
        while position[np.argmax(res1)] != 0:
            res1[np.argmax(res1)] = -999999
        position[np.argmax(res1)] = 1
        print('X - ', np.argmax(res1))
        if check_win(position):
            return p1

        res2 = p2.predict((-1) * position)
        while position[np.argmax(res2)] != 0:
            res2[np.argmax(res2)] += -999999

        position[np.argmax(res2)] = -1
        print('O - ', np.argmax(res2))

    return p2


def game_count_moves(p1, p2):
    position = np.zeros(64)
    moves_ = 0
    while not check_win(position):
        moves_ += 1
        res1 = p1.predict(position)

        while position[np.argmax(res1)] != 0:
            res1[np.argmax(res1)] = -999999

        position[np.argmax(res1)] = 1

        if check_win(position):
            return [p1, moves_]

        moves_ += 1
        res2 = p2.predict((-1) * position)

        while position[np.argmax(res2)] != 0:
            res2[np.argmax(res2)] += -999999

        position[np.argmax(res2)] = -1

    return [p2, moves_]


pandas = [Player()] * 50
for i in range(50):
    pandas[i] = Player()


def check_quality(player):
    n = 25
    winrate_ = 0
    moves_ = 0
    for i in range(n):
        res = game_count_moves(player, pandas[i])
        moves_ += res[1]
        if player == res[0]:
            winrate_ += 1

        res = game_count_moves(pandas[i + 1], player)
        moves_ += res[1]
        if player == res[0]:
            winrate_ += 1

    return [winrate_ * 2, moves_ / (2 * n)]


def championship(players):
    n = len(players)
    while n > 2:
        n = n // 2
        for i in range(n):
            players[i] = game(players[i], players[-1 - i - len(players) + 2 * n])

    return players[0], players[1]


Players = [Player()] * 1024
Me = 500
for i in range(1024):
    Players[i] = Player()

winrate = [0] * Me
moves = [0] * Me
for iteration in range(Me):
    random.shuffle(Players)
    print("Iteration № " + str(iteration) + '...')
    for tour in range(8):

        Players[0 + tour * 128], Players[1 + tour * 128] = championship(Players[128 * tour: 128 * tour + 128])
        Players[2 + tour * 128] = cross(Players[0 + tour * 128], Players[1 + tour * 128])

        qual = check_quality(Players[0 + tour * 128])
        winrate[iteration] += qual[0]
        moves[iteration] += qual[1]

        counter = 3

        while counter <= 127:

            Players[counter + 128 * tour] = Player(Players[0 + tour * 128])
            counter += 1

            if counter > 127:
                break

            Players[counter + 128 * tour] = Player(Players[1 + tour * 128])
            counter += 1

            if counter > 127:
                break

            Players[counter + 128 * tour] = Player(Players[2 + tour * 128])
            counter += 1

    winrate[iteration] /= 8
    moves[iteration] /= 8
    print("AVG winrate on", iteration, "iteration is: ", round(winrate[iteration], 2))
    print("AVG moves on", iteration, "iteration is: ", round(moves[iteration], 2))

x = list(range(1, Me + 1))

plt.plot(x, winrate)
plt.grid(True)
plt.xlabel('Iteration')
plt.ylabel('Winrate')
plt.title('Winrate vs random moves')
plt.show()

plt.plot(x, moves)
plt.grid(True)
plt.xlabel('Iteration')
plt.ylabel('Moves')
plt.title('Moves per game')
plt.show()


best = championship(Players)
RESULT = game_with_comments(best[0], best[1])

with open("hello.txt", "w") as file:
    file.write(str(RESULT.bias))
    for i in range(64):
        file.write(str(RESULT.weights[i]))

