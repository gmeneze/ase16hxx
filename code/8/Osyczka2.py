import sys
from Problem import *
sys.dont_write_bytecode = True
class Osyczka2(Problem):
    def __init__(self):
        """
        Osyczka2 class
        """
        self.points = []
        names = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6']
        lows = [0, 0, 1, 0, 1, 0]
        highs = [10, 10, 5, 6, 5, 10]
        decisions = [Decision(n, l, h) for n, l, h in zip(names, lows, highs)]
        objectives = [Objective("f1", True), Objective("f2", True)]
        Problem.__init__(self, decisions, objectives)

    @staticmethod
    def eval(self, point):
        def minimize(i):
            return -1 if self.objectives[i].domin else 1
        (x1, x2, x3, x4, x5, x6) = point.decisions
        f1 = -1 * (25 * ((x1 - 2) ** 2) + (x2 - 2) ** 2 + (x3 - 1) ** 2 * (x4 - 4) ** 2 + (x5 - 1) ** 2)
        f2 = x1 ** 2 + x2 ** 2 + x3 ** 2 + x4 ** 2 + x5 ** 2 + x6 ** 2
        point.objectives = [f1, f2]
        point.energy = int(f1 * minimize(0) + f2 * minimize(1))
        return point.objectives

    @staticmethod
    def ok(self, point):
        [x1, x2, x3, x4, x5, x6] = point.decisions
        if x1 + x2 - 2 < 0:
            return False
        if 6 - x1 - x2 < 0:
            return False
        if 2 - x2 + x1 < 0:
            return False
        if 2 - x1 + 3 * x2 < 0:
            return False
        if 4 - (x3 - 3) ** 2 - x4 < 0:
            return False
        if (x5 - 3) ** 3 + x6 - 4 < 0:
            return False
        for i, d in enumerate(point.decisions):
            if d < self.decisions[i].low or d > self.decisions[i].high:
                print i, d, self.decisions[i].low, self.decisions[i].high
                return False
        return True
