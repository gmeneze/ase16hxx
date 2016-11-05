#!/usr/bin/python
"""
Problem.py (c) 2016 gmeneze@ncsu.edu, dnair@ncsu.edu, smurali8@ncsu.edu. MIT licence
USAGE: 
    python Problem.py
OUTPUT:
    Produces an output in the format of :-

"""

from __future__ import division,print_function
from Node import Node
from Vehicle import Vehicle
from Algorithm import Algorithm
from Drawer import Drawer
import sys,re,traceback,random, operator, string, time
sys.dont_write_bytecode=True

class Route(object):
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.cost_factor = random.randint(1, 3)
        self.distance = self.get_distance()
        
    def get_distance(self):
        self.distance = ((abs(self.start_node.xcordinate - self.end_node.xcordinate))**2 + (abs(self.start_node.ycordinate - self.end_node.ycordinate)) ** 2) ** 0.5
        return self.distance
    
    def get_cost(self):
        return self.distance * self.cost_factor
    
    