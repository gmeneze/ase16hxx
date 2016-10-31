from Problem import *

class Schaffer(Problem):
    def __init__(self):
        """
        Schaffer class
        """
        self.points = []
        names = ['x1']
        lows = [-10 ** 5]
        highs = [10 ** 5]
        decisions = [Decision(n, l, h) for n, l, h in zip(names, lows, highs)]
        objectives = [Objective("f1", True), Objective("f2", True)]
        Problem.__init__(self, decisions, objectives)

    @staticmethod
    def eval(self, point):
        def minimize(i):
            return -1 if self.objectives[i].domin else 1
        f1 = point.decisions[0] ** 2
        f2 = (point.decisions[0] - 2) ** 2
        point.objectives = [f1, f2]
        point.energy = int(f1 * minimize(0) + f2 * minimize(1))
        return point.objectives

    @staticmethod
    def ok(self, point):
        return True