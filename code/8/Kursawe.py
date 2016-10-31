from Problem import *

class Kursawe(Problem):
    def __init__(self):
        """
        Kursawe class
        """
        self.points = []
        names = ['x1', 'x2', 'x3']
        lows = [-5, -5, -5]
        highs = [5, 5, 5]
        decisions = [Decision(n, l, h) for n, l, h in zip(names, lows, highs)]
        objectives = [Objective("f1", True), Objective("f2", True)]
        Problem.__init__(self, decisions, objectives)

    @staticmethod
    def eval(self, point):
        def minimize(i):
            return -1 if self.objectives[i].domin else 1
        (x1, x2, x3) = point.decisions
        f1, f2 = 0, 0
        f1 = -10 * (math.e ** (-0.2 * math.sqrt(x1 ** 2 + x2 ** 2)) - math.e ** (-0.2 * math.sqrt(x2 ** 2 + x3 ** 2)))
        for x in point.decisions:
            f2 += (math.fabs(x) ** 0.8 + 5 * math.sin(x ** 3))
        point.objectives = [f1, f2]
        point.energy = int(f1 * minimize(0) + f2 * minimize(1))
        return point.objectives

    @staticmethod
    def ok(self, point):
        return True