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
from SPEA import SPEA
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

    def normalize(self, pareto):
        low_distance = float("inf")
        low_time = float("inf")
        low_satisfaction = float("inf")
        high_distance = 0
        high_time = 0
        high_satisfaction = 0
        for solution in pareto:
            values = solution.fitness.values
            if values[0] < low_distance:
                low_distance = values[0]
            if values[0] > high_distance:
                high_distance = values[0]
            if values[1] < low_time:
                low_time = values[1]
            if values[1] > high_time:
                high_time = values[1]
            if values[2] < low_satisfaction:
                low_satisfaction = values[2]
            if values[2] > high_satisfaction:
                high_satisfaction = values[2]
        for solution in pareto:
            temp_dist, temp_time, temp_satisfaction = solution.fitness.values
            if high_distance == low_distance:
                sol_dist = 0
            else:
                sol_dist = (temp_dist - low_distance) / (high_distance - low_distance)
            if high_time == low_time:
                sol_time = 0
            else:
                sol_time = (temp_time - low_time) / (high_time - low_time)
            if high_satisfaction == low_satisfaction:
                sol_sat = 0
            else:
                sol_sat = 1 - (
                    (temp_satisfaction - low_satisfaction) / (high_satisfaction - low_satisfaction))
            solution.fitness.values = (sol_dist, sol_time, sol_sat)
        return pareto


    def GA_normalize(self, pareto):
        low_distance = float("inf")
        low_time = float("inf")
        low_satisfaction = float("inf")
        high_distance = 0
        high_time = 0
        high_satisfaction = 0
        for solution in pareto:
            if solution.distance.value < low_distance:
                low_distance = solution.distance.value
            if solution.distance.value > high_distance:
                high_distance = solution.distance.value
            if solution.time.value < low_time:
                low_time = solution.time.value
            if solution.time.value > high_time:
                high_time = solution.time.value
            if solution.satisfaction.value < low_satisfaction:
                low_satisfaction = solution.satisfaction.value
            if solution.satisfaction.value > high_satisfaction:
                high_satisfaction = solution.satisfaction.value
        for solution in pareto:
            temp_dist = solution.distance.value
            temp_time = solution.time.value
            temp_satisfaction = solution.satisfaction.value
            if high_distance == low_distance:
                solution.distance.value = 0
            else:
                solution.distance.value = (temp_dist - low_distance) / (high_distance - low_distance)
            if high_time == low_time:
                solution.time.value = 0
            else:
                solution.time.value = (temp_time - low_time) / (high_time - low_time)
            if high_satisfaction == low_satisfaction:
                solution.satisfaction.value = 0
            else:
                solution.satisfaction.value = 1 - (
                    (temp_satisfaction - low_satisfaction) / (high_satisfaction - low_satisfaction))
        return pareto

    def sortlist(self, pareto):
        sorted(pareto, key=lambda tup: (tup[0], tup[1], tup[2]))
        return pareto

    def GA_sortlist(self, pareto):
        sum_list = []
        for solution in pareto:
            temp_sum = (solution.distance.value , solution.time.value , solution.satisfaction.value)
            sum_list.append(temp_sum)
        sorted(sum_list, key=lambda tup: (tup[0], tup[1], tup[2]))
        return sum_list

    def euclid(self, one, two):
        try:
            values1 = one.fitness.values
            values2 = two.fitness.values
        except:
            values1 = one
            values2 = two

        dist_euclid = ((values1[0] - values2[0]) ** 2 + (values1[1] - values2[1]) ** 2 + (
                values1[2] - values2[2]) ** 2) ** 0.5
        return dist_euclid
        
    def closest(self,one,many):
        min_dist = float("inf")
        closest_point = None
        for this in many:
            dist = self.euclid(this, one)
            if dist < min_dist:
                min_dist = dist
                closest_point = this
        return min_dist, closest_point
        
    def igd(self,obtained, ideals):
        igd_val = sum([self.closest(ideal,obtained)[0] for ideal in ideals])/len(ideals)
        return igd_val

    def spread(self, pareto_soln):
        n = len(pareto_soln)
        d_l = self.euclid(pareto_soln[0], pareto_soln[1])
        d_f = self.euclid(pareto_soln[n - 1], pareto_soln[n - 2])
        distances = []
        for i in range(1, n - 1):
            distances.append(self.euclid(pareto_soln[i], pareto_soln[i + 1]))
        d_bar = sum(distances) / len(distances)
        d_sum = sum([abs(d_i - d_bar) for d_i in distances])
        delta = (d_f + d_l + d_sum) / (d_f + d_l + (n - 1) * d_bar)
        return delta


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


commpareto = []

start_time = time.time()
print ("GA BDOM")
ga = GA(newProblem, "bdom")
gabpop, gabpareto = ga.solve(newProblem.nodelist)
end_time = time.time()
print("Time taken : %s"  % (end_time - start_time))

start_time = time.time()
print ("GA CDOM")
ga.domn = "cdom"
gacpop, gacpareto = ga.solve(newProblem.nodelist)
end_time = time.time()
print("Time taken : %s"  % (end_time - start_time))

start_time = time.time()
print ("NSGA2 BDOM")
nsga = NSGA2(newProblem)
nsgabpopulation, logbook, nsgabpareto = nsga.main(nsga.bdom)
end_time = time.time()
print("Time taken : %s"  % (end_time - start_time))

start_time = time.time()
print ("NSGA2 CDOM")
nsgacpopulation, logbook, nsgacpareto = nsga.main(nsga.cdom)
end_time = time.time()
print("Time taken : %s"  % (end_time - start_time))

start_time = time.time()
print ("SPEA BDOM")
spea = SPEA(newProblem)
speabpopulation, logbook, speabpareto = spea.main(spea.bdom)
end_time = time.time()
print("Time taken : %s"  % (end_time - start_time))

start_time = time.time()
print ("SPEA CDOM")
speacpopulation, logbook, speacpareto = spea.main(spea.cdom)
end_time = time.time()
print("Time taken : %s"  % (end_time - start_time))


print(len(gabpareto))
temp_pareto = newProblem.GA_normalize(gabpareto)
sums = newProblem.GA_sortlist(temp_pareto)
spread_val = newProblem.spread(sums)
print ("GA BDOM Spread")
print(spread_val)

print(len(gacpareto))
temp_pareto = newProblem.GA_normalize(gacpareto)
sums = newProblem.GA_sortlist(temp_pareto)
spread_val = newProblem.spread(sums)
print ("GA CDOM Spread")
print(spread_val)

print(len(nsgabpareto))
temp_pareto = newProblem.normalize(nsgabpareto)
sums = newProblem.sortlist(temp_pareto)
spread_val = newProblem.spread(sums)
print ("NSGA BDOM Spread")
print(spread_val)

print(len(nsgacpareto))
temp_pareto = newProblem.normalize(nsgacpareto)
sums = newProblem.sortlist(temp_pareto)
spread_val = newProblem.spread(sums)
print ("NSGA CDOM Spread")
print(spread_val)

commpareto.append(speabpareto)
temp_pareto = newProblem.normalize(speabpareto)
sums = newProblem.sortlist(temp_pareto)
spread_val = newProblem.spread(sums)
print ("SPEA BDOM Spread")
print(spread_val)

commpareto.append(speacpareto)
temp_pareto = newProblem.normalize(speacpareto)
sums = newProblem.sortlist(temp_pareto)
spread_val = newProblem.spread(sums)
print ("SPEA CDOM Spread")
print(spread_val)


commpareto.append([(sol.distance.value, sol.time.value, sol.satisfaction.value) for sol in gabpareto])
commpareto.append([(sol.distance.value, sol.time.value, sol.satisfaction.value) for sol in gacpareto])
commpareto.append([sol.fitness.values for sol in nsgabpareto])
commpareto.append([sol.fitness.values for sol in nsgacpareto])
commpareto.append([sol.fitness.values for sol in speabpareto])
commpareto.append([sol.fitness.values for sol in speacpareto])


ideal_pareto = newProblem.normalize(compareto)
#ideal_sorted = newProblem.sortlist(ideal_pareto)
obtain_pareto = newProblem.normalize(nsgabpareto)
#obtain_sorted = newProblem.sortlist(obtain_pareto)
igd_val = newProblem.igd(ideal_pareto,obtain_pareto)
print(igd_val)


"""
ga = GA(newProblem, "cdom")
ga.solve(newProblem.nodelist)


nsga = NSGA(newProblem)
nsga.main(10)


nsga = NSGA2(newProblem)
population, logbook, pareto = nsga.main()


nsga = SPEA(newProblem)
#nsga = NSGA2(newProblem)
population, logbook, pareto = nsga.main(nsga.bdom)
mini = 1000000
ind = None
for i in population:
    print (i.fitness.values[0], i.fitness.values[1], i.fitness.values[2])
    if i.fitness.values[0] < mini:
        mini = i.fitness.values[0]
        ind = i
print (ind)
print (ind.fitness.values[0], ind.fitness.values[1], ind.fitness.values[2])
print (pareto)
print (len(pareto))
"""