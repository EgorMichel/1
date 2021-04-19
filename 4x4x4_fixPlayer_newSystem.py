import numpy as np
import matplotlib.pyplot as plt
import numpy.random
from random import randint
import keyboard
import random
import time


def line_to_array(pos):
    position = (([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
                ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
                ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]),
                ([0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]))

    counter_ = 0

    for k in range(4):
        for z in range(4):
            for j in range(4):
                position[k][z][j] = pos[counter_]
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
    def __init__(self, parent=0, changes_w=1, changes_b=1):
        if parent == 0:
            self.bias = np.random.randint(-100, 100, 64)
            self.weights = np.random.randint(-100, 100, (64, 64))
            self.changed_weights = [[-1, -1]] * changes_w
            self.changed_bias = [-1] * changes_b

        if parent != 0:
            self.bias = np.zeros(64)
            self.weights = np.zeros((64, 64))

            for value in range(64):
                self.bias[value] = parent.bias[value]
                for val in range(64):
                    self.weights[value][val] = parent.weights[value][val]

            self.changed_weights = np.random.randint(0, 63, (changes_w, 2))
            self.changed_bias = np.random.randint(0, 63, changes_b)

            for changed_w in self.changed_weights:
                self.weights[changed_w[0]][changed_w[1]] += randint(-50, 50)

            for changed_b in self.changed_bias:
                self.bias[changed_b] += randint(-50, 50)

    def predict(self, x_):
        return np.dot(x_, self.weights) + self.bias


def cross(p1, p2):
    if p1.changed_weights[0][0] == -1:
        return p1

    p3 = Player()
    for b in range(64):
        p3.bias[b] = p2.bias[b]
        if randint(0, 1) == 0:
            for w in range(64):
                p3.weights[w][b] = p2.weights[w][b]
        else:
            for ww in range(64):
                p3.weights[ww][b] = p1.weights[ww][b]

    for element in p1.changed_weights:
        p3.weights[element[0]][element[1]] = p1.weights[element[0]][element[1]]

    for elem in p1.changed_bias:
        p3.bias[elem] = p1.bias[elem]

    return p3


def game_vs_random(p1):
    position = np.zeros(64)

    if randint(0, 1) == 0:
        while not check_win(position):

            res1 = p1.predict(position)
            while position[np.argmax(res1)] != 0:
                res1[np.argmax(res1)] = -99999999
            position[np.argmax(res1)] = 1
            if check_win(position):
                return p1

            res2 = randint(0, 63)
            while position[res2] != 0:
                res2 = randint(0, 63)
            position[res2] = -1

        return 0

    else:
        while not check_win(position):

            res2 = randint(0, 63)
            while position[res2] != 0:
                res2 = randint(0, 63)
            position[res2] = -1
            if check_win(position):
                return 0

            res1 = p1.predict(position)
            while position[np.argmax(res1)] != 0:
                res1[np.argmax(res1)] = -99999999
            position[np.argmax(res1)] = 1

        return p1


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


def check_quality(player):
    n = 25
    winrate_ = 0
    for y in range(n):
        res = game_vs_random(player)
        if player == res:
            winrate_ += 1
    return winrate_ * 4


def championship(players):
    qualities = np.zeros(len(players))
    counter = 0
    for one in players:
        qualities[counter] = check_quality(one)
        counter += 1
    return qualities


size = 100
iteration = 1
Agents = [Player()] * size
new_Agents = [Player()] * size
qual_plot = [50]
for j in range(size):
    Agents[j] = Player()

while not keyboard.is_pressed('ctrl'):
    print("Iteration", iteration, "...")
    result = championship(Agents)
    iteration += 1
    qual_plot.append(result[np.argmax(result)])
    print("Best result:", result[np.argmax(result)])
    print("Worst result:", result[np.argmin(result)])

    for h in range(size // 10):
        new_Agents[h] = Agents[np.argmax(result)]
        result[np.argmax(result)] = 0

    for t in range(size - size//10):
        new_Agents[size // 10 + t] = cross(new_Agents[randint(0, size // 10 - 1)],
                                           new_Agents[randint(0, size // 10 - 1)])
        if t + 1 < size - size//10:
            t += 1
        new_Agents[size // 10 + t] = cross(new_Agents[randint(0, size//10 - 1)], Agents[randint(0, size - 1)])
        if t + 1 < size - size//10:
            t += 1
        new_Agents[size // 10 + t] = Player(new_Agents[randint(0, size//10 - 1)])
        if t + 1 < size - size//10:
            t += 1
        new_Agents[size // 10 + t] = Player(new_Agents[randint(0, size - 1)])

    for current_agent in range(size):
        Agents[current_agent] = new_Agents[current_agent]


x = list(range(1, iteration + 1))
plt.plot(x, qual_plot)
plt.grid(True)
plt.xlabel('Iteration')
plt.ylabel('Winrate')
plt.title('Winrate vs random moves')
plt.show()
