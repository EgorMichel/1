import numpy as np
import matplotlib.pyplot as plt
import numpy.random
from random import randint
import random


class Player:
    def __init__(self, parent=0, analog=0):
        self.changed_elements = [[-1, -1]] * 256
        self.bias = [0] * 64
        self.weights = [[0] * 64] * 64
        if parent == 0:
            self.weights = np.random.randint(-10000, 10000, (64, 64)) / 10000
            self.bias = np.random.randint(-10000, 10000, 64) / 10000

        if parent != 0 and analog == 0:

            self.bias = parent.bias
            self.weights = parent.weights

            for i in range(8):
                self.bias[randint(0, 63)] += (randint(-50000, 50000) / 10000)

            for i in range(256):

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


p11 = Player()
print(p11.weights[0])
p22 = Player(p11)
print(p22.weights[0])
p33 = cross(p11, p22)
print(p33.weights[0])
