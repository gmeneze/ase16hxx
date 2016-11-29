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
from GA import GA
from TSP import TSP
from Objective import Objective
from NSGA import NSGA
from NSGA2 import NSGA2
#import numpy as np
from random import *
import sys,re,traceback,random, operator, string, time
import deap
sys.dont_write_bytecode=True


class Problem(object):
    def __init__(self, num_of_nodes, num_of_vehicles):
        self.drawer = Drawer()
        self.nodelist = []
        self.vehicle = []
        self.num_of_nodes = num_of_nodes
        self.num_of_vehicles = num_of_vehicles
        self.cost_matrix = [[0 for _ in range(num_of_nodes)] for _ in range(num_of_nodes)]
        self.speed_matrix = [[0 for _ in range(num_of_nodes)] for _ in range(num_of_nodes)]
        self.objectives = []
        self.decisions = []
        self.generate_nodes()
        self.generate_vehicles()
        self.generate_cost_matrix()
        self.generate_speed_matrix()

    def __repr__(self):
        print (self.nodelist)
        print (self.cost_matrix)
        print (self.speed_matrix)

    
    def generate_nodes(self):
        """
        generate nodes randomly
        """
        maxdays = self.num_of_nodes / 2
        for i in range(self.num_of_nodes):
            day = randint(1,maxdays)
            time = 24 * day + 20
            self.nodelist.append(Node(i, random.randint(0, self.drawer.window_length),
                                      random.randint(0, self.drawer.window_height), randint(1,5), time, randint(1,5)))
        
    
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
                self.cost_matrix[j][i] = self.cost_matrix[i][j] = route.get_distance()

    def generate_speed_matrix(self):
        """
        generate speeds randomly
        """
        for i in range(self.num_of_nodes):
            for j in range(self.num_of_nodes):
                if i == j:
                    self.speed_matrix[i][j] = 0
                else: 
                    #route = Route(self.nodelist[i], self.nodelist[j])
                    self.speed_matrix[i][j] = random.randint(20, 100)


"""
for i in range(10):
    newProblem = Problem(30,1)
    #for n in newProblem.nodelist:
        #print(n.id, n.xcordinate, n.ycordinate)
    #for v in newProblem.vehicle:
        #print(v.v_id, v.x, v.y)
    #print(newProblem.cost_matrix)40
    #print(newProblem.speed_matrix)
    current_soln = list(range(0, newProblem.num_of_nodes))
    current_soln.append(0)
    #print(current_soln)
    #print(newProblem.determine_cost(current_soln))
    print("Iteration"+str(i))
    for iterations in range(10,10,10):
        print("IterationSize = "+str(iterations))
        for tabulen in range(10,30,10):
            print("Tabu List Length = " + str(tabulen))
            print("Optimizing Distance")
            tsp = TSP(newProblem.cost_matrix, newProblem.speed_matrix, current_soln, 10, 10, newProblem.num_of_nodes,1)
            best_solution = tsp.solve_tabu()
            #drawer = Drawer()
            #drawer.draw_path(newProblem.nodelist,best_solution)
            print("Optimizing Time")
            tsp = TSP(newProblem.cost_matrix, newProblem.speed_matrix, current_soln, 10, 10, newProblem.num_of_nodes,2)
            best_solution = tsp.solve_tabu()
            print("-----------------------------------------Solution--------------------------------------------------")
            #drawer = Drawer()
            #drawer.draw_path(newProblem.nodelist,best_solution)
        print("-------------------------------------------------------TabuLen------------------------------------")
    print("----------------------------------------------------Inner Iteration------------------------------------")
print("------------------------------------------------------Outer Iteration----------------------------------------")
"""


newProblem = Problem(30,1)
newProblem.objectives.append(Objective("distance"))
newProblem.objectives.append(Objective("time"))
newProblem.objectives.append(Objective("satisfaction", None ,False))
newProblem.__repr__()
"""
ga = GA(newProblem, "cdom")
ga.solve(newProblem.nodelist)


nsga = NSGA(newProblem)
nsga.main(10)
"""

nsga = NSGA2(newProblem)
population = nsga.main()
mini = 1000000
ind = None
for i in population[0]:
    print (i.fitness.values[0], i.fitness.values[1], i.fitness.values[2])
    if i.fitness.values[0] < mini:
        mini = i.fitness.values[0]
        ind = i
print (ind)
print (ind.fitness.values[0], ind.fitness.values[1], ind.fitness.values[2])