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
import sys,re,traceback,random, operator, string, time
sys.dont_write_bytecode=True

class Problem(object):
    def __init__(self, num_of_nodes, num_of_vehicles):
        self.drawer = Drawer()
        self.nodelist = []
        self.vehicle = []
        self.routelist = []
        self.num_of_nodes = num_of_nodes
        self.num_of_vehicles = num_of_vehicles
        self.cost_matrix = [[0]*num_of_nodes]*num_of_nodes
        self.objectives = []
        self.decisions = []
    
    def generate_nodes(self):
        """
        generate nodes randomly
        """
        for i in range(self.num_of_nodes):
            self.nodelist.append(Node(i, random.randint(self.drawer.window_length, self.drawer.window_height))
        
    
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
        for i in xrange(num_of_nodes):
            for j in xrange(i+1, num_of_nodes):
                route = Route(nodelist[i], nodelist[j])
                self.cost_matrix[i][j] = self.cost_matrix[j][i] = route.distance * route.cost_factor
                
    
    def determine_route(self):
        """
        iterate over vehicle list and 
        generate optimal route per vehicle
        """
    
    

