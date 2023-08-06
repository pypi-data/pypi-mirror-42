import numpy as np


class beispiel(object):
    def __init__(self):
        self.a = None

    def calc_res(self, x):
        self.a = x**2

    def seq_calc(self):
        self.a = 2*self.a

class beispiel_2(beispiel):
    def __init__(self):
        super().__init__()

    def seq_calc(self):
        self.a = 10 - self.a
