#import numpy as np
import copy
class TSP(object):
    def __init__(self, cost_matrix, initial_solution, num_iterations, tabu_len, num_of_nodes):
        self.cost_matrix = cost_matrix
        self.current_solution = initial_solution
        self.num_iterations = num_iterations
        self.num_of_nodes = num_of_nodes
        self.tabu_len = tabu_len
        self.tabu_list = [[0 for _ in range(num_of_nodes)] for _ in range(num_of_nodes)]
        self.cost = self.determine_cost(self.current_solution)
        self.best_solution = initial_solution
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
        for i in range(solution.__len__()-1):
            j = solution[i]
            k = solution[i + 1]
            #print j , k
            cost += self.cost_matrix[j][k]
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
                            self.tabu_list[i][j]= self.tabu_list[j][i] = self.tabu_len
        self.current_solution = best_temp

    def update_tabu(self):
        #print "Tabu List"
        #print(np.matrix(self.tabu_list))
        for i in range(self.num_of_nodes):
            for j in range(self.num_of_nodes):
                if (self.tabu_list[i][j] != 0):
                    self.tabu_list[i][j] = self.tabu_list[i][j] - 1

    def solve_tabu(self):
        #self.best_cost = self.cost
        #self.best_solution = self.current_solution
        print("Initial")
        print(self.best_solution)
        print(self.best_cost)
        for i in range(self.num_iterations):
            self.get_next_solution()
            print("Current Soln: %s", str(self.current_solution))
            #print "==Best Soln Before:"+ str(self.best_solution)
            self.cost = self.determine_cost(self.current_solution)
            #print "==Best Soln After:"+ str(self.best_solution)
            print("Current Cost:", str(self.cost))
            if self.cost < self.best_cost:
                self.best_cost = self.cost
                print("Updating best Solution")
                self.best_solution = copy.deepcopy(self.current_solution)
                print("Best Soln: %s", str(self.best_solution))
                print("Best Cost: %s", str(self.best_cost))
        print("final Soln:")
        print(self.best_solution)
        #print self.current_solution
        print(self.best_cost)
        return self.best_solution




