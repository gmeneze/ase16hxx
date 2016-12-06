#import numpy as np
import copy, math, sys
from Solution import Solution
class Tabu(object):
    def __init__(self, problem, cost_matrix, speed_matrix, initial_solution, num_iterations, tabu_len, num_of_nodes,metric):
        self.problem = problem
        self.cost_matrix = cost_matrix
        self.speed_matrix = speed_matrix
        self.current_solution = initial_solution
        self.num_iterations = num_iterations
        self.num_of_nodes = num_of_nodes
        self.tabu_len = tabu_len
        self.tabu_list = [[0 for _ in range(num_of_nodes)] for _ in range(num_of_nodes)]
        self.best_solution = initial_solution
        self.metric = metric
        self.cost = self.determine_cost(self.current_solution)
        self.best_cost = self.cost
    
    def determine_cost(self, solution):
        """
        iterate over route and
        determine cost
        """

        cost = 0
        #print 'begin cost'
        #print solution
        #print solution.__len__()
        if self.metric == 1:
            for i in range(solution.__len__()-1):
                j = solution[i]
                k = solution[i + 1]
            #print j , k
                cost += self.cost_matrix[j][k]
        if self.metric == 2:
            #print("In speed")
            for i in range(solution.__len__() - 1):
                j = solution[i]
                k = solution[i + 1]
                # print j , k
                cost += self.cost_matrix[j][k]/self.speed_matrix[j][k]
        #print cost
        #print 'end cost'
        return cost

    def get_next_solution(self):
        # self.best_cost = self.cost
        initial_solution = self.current_solution
        best_temp = initial_solution
        best_temp_cost = self.determine_cost(initial_solution)
        for i in range(1, initial_solution.__len__() - 1):
            for j in range(2, initial_solution.__len__() - 1):
                if (i != j):
                    temp_solution = initial_solution
                    if self.tabu_list[i][j] == 0:
                        temp_solution[i], temp_solution[j] = temp_solution[j], temp_solution[i]
                        temp_cost = self.determine_cost(temp_solution)
                        self.update_tabu()
                        if temp_cost < best_temp_cost:
                            best_temp = temp_solution
                            best_temp_cost = temp_cost
                            if self.metric == 1:
                                self.tabu_list[i][j]= self.tabu_list[j][i] = self.tabu_len
                            if self.metric == 2:
                                self.tabu_list[i][j] = self.tabu_len
        self.current_solution = best_temp

    def update_tabu(self):
        #print "Tabu List"
        #print(np.matrix(self.tabu_list))
        for i in range(self.num_of_nodes):
            for j in range(self.num_of_nodes):
                if (self.tabu_list[i][j] != 0):
                    self.tabu_list[i][j] = self.tabu_list[i][j] - 1

    def get_totaldistance(self, solution):
        cost = 0
        # print 'begin cost'
        # print solution
        # print solution.__len__()
        for i in range(solution.__len__() - 1):
            j = solution[i]
            k = solution[i + 1]
             # print j , k
            cost += self.cost_matrix[j][k]
        return cost

    def get_totaltime(self,solution):
        cost = 0
        satisfaction = 0
        for i in range(solution.__len__() - 1):
            j = solution[i]
            k = solution[i + 1]
            # print j , k
            cost += self.cost_matrix[j][k] / self.speed_matrix[j][k]
            if cost < self.problem.nodelist[solution[i]].latestReach:
                satisfaction += self.problem.nodelist[solution[i]].satisfaction
            # print cost
            # print 'end cost'
        return cost, satisfaction

    def solve_tabu(self):
        #self.best_cost = self.cost
        #self.best_solution = self.current_solution
        #print("Initial")
        #print(self.best_solution)
        #print(self.best_cost)
        for i in range(self.num_iterations):
            self.get_next_solution()
            #print("Current Soln: %s", str(self.current_solution))
            #print "==Best Soln Before:"+ str(self.best_solution)
            self.cost = self.determine_cost(self.current_solution)
            #print "==Best Soln After:"+ str(self.best_solution)
            #print("Current Cost:", str(self.cost))
            if self.cost < self.best_cost:
                self.best_cost = self.cost
                #print("Updating best Solution")
                self.best_solution = copy.deepcopy(self.current_solution)
                #print("Best Soln: %s", str(self.best_solution))
                #print("Best Cost: %s", str(self.best_cost))
        print("final Soln:")
        print(self.best_solution)
        #print self.current_solution
        #print(self.best_cost)
        print("Distance")
        print(self.get_totaldistance(self.best_solution))
        print("Time")
        time, sat = self.get_totaltime(self.best_solution)
        print(time, sat)
        solution = Solution(self.best_solution, self.get_totaldistance(self.best_solution), time, sat)
        return solution

def cdom(node1, node2, rev=False):
    x = [node1.distance, node1.time, node1.satisfaction]
    y = [node2.distance, node2.time, node2.satisfaction]

    def w(objective):
        return -1 if objective.do_minimize == True else 1

    def expLoss(w, x1, y1, n):
        try:
            return -1 * math.e ** (w * (x1 - y1) / n)
        except:
            return sys.maxsize

    def loss(x, y):
        losses = []
        n = min(len(x), len(y))
        for obj, obj1 in zip(x, y):
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


def bdom( node1, node2, rev=False):
    x = [node1.distance, node1.time, node1.satisfaction]
    y = [node2.distance, node2.time, node2.satisfaction]
    less = 0
    dominates = True
    for obj, obj1 in zip(x, y):
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


def dom(node1, node2, domn = "bdom", rev=False):
    if domn == "cdom":
        return cdom(node1, node2, rev)
    else:
        return bdom(node1, node2, rev)


def condition(dominated, dom = "bdom"):
    if dom == "bdom":
        if dominated == 0:
            return True
    elif dom == "cdom":
        if dominated < 20:
            return True
    return False

def tabumain(newProblem):
    tabupop = []
    current_soln = list(range(0, newProblem.num_of_nodes))
    current_soln.append(0)
    for iterations in range(10, 30, 10):
        print("IterationSize = " + str(iterations))
        for tabulen in range(10, 30, 10):
            print("Tabu List Length = " + str(tabulen))
            print("Optimizing Distance")
            tabu = Tabu(newProblem, newProblem.cost_matrix, newProblem.speed_matrix, current_soln, 10, 10,
                        newProblem.num_of_nodes, 1)
            best_solution = tabu.solve_tabu()
            tabupop.append(best_solution)
            print("Optimizing Time")
            tabu = Tabu(newProblem, newProblem.cost_matrix, newProblem.speed_matrix, current_soln, 10, 10,
                        newProblem.num_of_nodes, 2)
            best_solution = tabu.solve_tabu()
            tabupop.append(best_solution)
            print(
                "-----------------------------------------Solution--------------------------------------------------")
        print("-------------------------------------------------------TabuLen------------------------------------")
    print("----------------------------------------------------Inner Iteration------------------------------------")
    pareto = []
    print("pareto")
    for ind in tabupop:
        dominates = 0
        dominated = 0
        for oth in tabupop:
            if oth == ind:
                continue
            if dom(ind, oth):
                dominates += 1
            elif dom(oth, ind):
                dominated += 1
        if condition(dominated):
            print("appended")
            pareto.append(ind)

    return tabupop, pareto
