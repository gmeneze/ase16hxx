import math
import sys
from Objective import Objective

class Solution(object):
    def __init__(self, path, distance = None, time = None, satisfaction = None):
        self.path = path
        self.distance = Objective("distance", distance)
        self.time = Objective("time", time)
        self.satisfaction = Objective("satisfaction", satisfaction, False)
        self.fitness = None
        self.crowding_dist = None
        self.valid = True

    def getfitness(self, population):
        dominates = 0
        for i in population:
            if self.dominates(i):
                dominates += 1
        self.fitness = dominates

    def dominates(self, node):
        return self.bdom(self, node)

    def cdom(self, node1, node2, rev = False):
        x = [node1.distance, node1.time, node1.satisfaction]
        y = [node2.distance, node2.time, node2.satisfaction]

        def w(objective):
            return -1 if objective.do_minimize == True else 1

        def expLoss(w, x1, y1, n):
            try:
                return -1 * math.e ** (w * (x1 - y1) / n)
            except:
                return sys.maxint

        def loss(x, y):
            losses = []
            n = min(len(x), len(y))
            for obj, obj1 in zip(x,y):
                x1, y1 = obj.value, obj1.value
                losses += [expLoss(w(obj), x1, y1, n)]
            return sum(losses) / n

        l1 = loss(x, y)
        l2 = loss(y, x)

        response = l1 < l2
        if rev:
            return not response
        else:
            return response

    def bdom(self, node1, node2, rev = False):
        x = [node1.distance, node1.time, node1.satisfaction]
        y = [node2.distance, node2.time, node2.satisfaction]
        less = 0
        dominates = True
        for obj, obj1 in zip(x,y):
            if obj.do_minimize:
                if obj.value > obj1.value:
                    dominates = False
                    break
                elif obj.value < obj1.value:
                    less = 1
            else:
                if obj.value < obj1.value:
                    dominates = False
                    break
                elif obj.value > obj1.value:
                    less = 1
        if dominates:
            if less == 0:
                dominates = False
            else:
                dominates = True
        if rev:
            return not dominates
        else:
            return dominates