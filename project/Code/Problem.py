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
from Route import Route
from TSP import TSP
import numpy as np
import sys,re,traceback,random, operator, string, time
sys.dont_write_bytecode=True

class Problem(object):
    def __init__(self, num_of_nodes, num_of_vehicles):
        self.drawer = Drawer()
        self.nodelist = []
        self.vehicle = []
        self.num_of_nodes = num_of_nodes
        self.num_of_vehicles = num_of_vehicles
        self.cost_matrix = [[0 for _ in range(num_of_nodes)] for _ in range(num_of_nodes)]
        self.objectives = []
        self.decisions = []
        self.generate_nodes()
        self.generate_vehicles()
        self.generate_cost_matrix()
    
    def generate_nodes(self):
        """
        generate nodes randomly
        """
        for i in range(self.num_of_nodes):
            self.nodelist.append(Node(i, random.randint(0, self.drawer.window_length), random.randint(0, self.drawer.window_height)))
        
    
    def generate_vehicles(self):
        """
        generate vehicles randomly
        """
        for i in range(self.num_of_vehicles):
            self.vehicle.append(Vehicle(i, x = self.nodelist[0].xcordinate, y = self.nodelist[0].ycordinate))
        
    
    
    def generate_cost_matrix(self):
        """
        generate costs randomly
        """
        for i in range(self.num_of_nodes):
            for j in range(i+1, self.num_of_nodes):
                route = Route(self.nodelist[i], self.nodelist[j])
                self.cost_matrix[j][i] = self.cost_matrix[i][j] = route.get_cost()


    
newProblem = Problem(10,1)
for n in newProblem.nodelist:
    print(n.id, n.xcordinate, n.ycordinate)
for v in newProblem.vehicle:
    print(v.v_id, v.x, v.y)
print(newProblem.cost_matrix)
current_soln = list(range(0, newProblem.num_of_nodes))
current_soln.append(0)
print(current_soln)
#print(newProblem.determine_cost(current_soln))
tsp = TSP(newProblem.cost_matrix, current_soln, 10, 10, newProblem.num_of_nodes)
best_solution = tsp.solve_tabu()
Drawer.draw_path(newProblem.nodelist,best_solution)

