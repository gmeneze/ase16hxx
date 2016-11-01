import sys
from Problem import *
sys.dont_write_bytecode = True
class Schaffer(Problem):
    names = []
    lows = []
    highs = []
    decisions = []
    objectives = []

    def __init__(self):
        """
        Schaffer class
        """
        self.points = []
        self.names = ['x1']
        self.lows = [-10 ** 5]
        self.highs = [10 ** 5]
        self.decisions = [Decision(n, l, h) for n, l, h in zip(self.names, self.lows, self.highs)]
        self.objectives = [Objective("f1", True), Objective("f2", True)]
        Problem.__init__(self, self.decisions, self.objectives)

    def f1(self, p, i):
        if p >= self.highs[i] or p <= self.lows[i]:
            return None
        f1_ret = pow(p, 2)
        return f1_ret

    def f2(self, p, i):
        if p >= self.highs[i] or p <= self.lows[i]:
            return None
        f2_ret = pow(p - 2, 2)
        return f2_ret

    @staticmethod
    def eval(self, point):
        def minimize(i):
            return -1 if self.objectives[i].domin else 1
        f1 = self.f1(point.decisions[0], 0)
        f2 = self.f2(point.decisions[0], 0)
        point.objectives = [f1, f2]
        point.energy = int(f1 * minimize(0) + f2 * minimize(1))
        return point.objectives

    @staticmethod
    def ok(self, point):
        if point.decisions[0] >= self.highs[0] or point.decisions[0] <= self.lows[0]:
            return False
        return True