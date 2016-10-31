#! /usr/bin/python

import random, sys
import copy, math, sys


def shuffle(lst):
    """
    lsit Shuffling
    """
    random.shuffle(lst)
    return lst


def display(lst):
  """
  Print whithout going to new line
  """
  print lst,
  sys.stdout.flush()


class Object:
    """
    Object class
    """

    def __init__(self, **kwargs):
        self.has().update(**kwargs)

    def has(self):
        return self.__dict__

    def update(self, **kwargs):
        self.has().update(kwargs)
        return self

    def __repr__(self):
        show = [':%s %s' % (k, self.has()[k])
                for k in sorted(self.has().keys())
                if k[0] is not "_"]
        txt = ' '.join(show)
        if len(txt) > 60:
            show = map(lambda x: '\t' + x + '\n', show)
        return '{' + ' '.join(show) + '}'


class Decision(Object):
    """
    Decisions for the Optimization
    """
    def __init__(self, name, low, high):
        Object.__init__(self, name=name, low=low, high=high)


class Objective(Object):
    """
    Objectives for the Optimization
    """
    def __init__(self, name, domin=True):
        Object.__init__(self, name=name, domin=domin)


class Point(Object):
    """
    Class for the points in the population
    """

    def __init__(self, decisions):
        Object.__init__(self)
        self.decisions = decisions
        self.objectives = None
        self.energy = None

    def __eq__(self, other):
        return self.decisions == other.decisions

    def copypoint(self):
        new = Point(self.decisions)
        new.objectives = self.objectives
        new.energy = self.energy
        return new


class Problem(Object):
    """
    Problem class
    """
    def __init__(self, decisions, objectives):
        Object.__init__(self)
        self.decisions = decisions
        self.objectives = objectives

    @staticmethod
    def eval(point):
        return point.objectives

    @staticmethod
    def ok(self, point):
        return True

    def any(self, retries=500):
        for _ in xrange(retries):
            point = Point([random.randint(int(d.low), d.high) for d in self.decisions])
            if self.ok(self, point):
                self.eval(self, point)
                self.points.append(point)
                return point
        raise RuntimeError("Exceeded max runtimes of %d" % retries)

