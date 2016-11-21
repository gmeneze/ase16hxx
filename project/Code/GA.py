from random import *
from Solution import Solution

class GA(object):
    def __init__(self, cost_matrix, speed_matrix, iterations = 0, currentSolution = [], bestSolution = [], 
                        bestFitness = 0, population = [], mutationRate = 0.2):
        self.cost_matrix = cost_matrix
        self.speed_matrix = speed_matrix
        self.iterations = iterations
        self.currentSolution = currentSolution
        self.bestSolution = bestSolution
        self.bestFitness = bestFitness
        self.population = population
        self.mutationRate = mutationRate
        
    def generate_population(self, nodelist, num = 10):
        self.population = [self.generate_one_solution(nodelist) for _ in num]
                
                
    def generate_one_solution(self, nodelist):
        i = randint(0,len(nodelist))
        included = []
        path = []
        start = i
        while True:
            if i not in included:
                path.append(nodelist[i])
                included.append(i)
                if len(included) == len(nodelist):
                    path.append(nodelist[start])
                    break
            i = (i + int(random()))%len(nodelist)
        solution = Solution(path)
        solution.distance = 0
        solution.time = 0
        return solution
        
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
        for i in range(solution.__len__() - 1):
            j = solution[i]
            k = solution[i + 1]
            # print j , k
            cost += self.cost_matrix[j][k] / self.speed_matrix[j][k]
            # print cost
            # print 'end cost'
        return cost
                    
    
    def cdom(self, node1, node2, rev = False):
        if rev:
            return node1
        else:
            return node2
        
    def crossover(self, mom, dad):
        start = randint(0,len(mom))
        end = randint(0,len(mom))
        child = []
        if start > end:
            start, end = end, start
        for i in xrange(start, end + 1):
            child.append(mom[i])
        for i in xrange(len(dad)):
            if dad[i] not in child:
                child.append(dad[i])
        child.append(mom[start])
        return child
    
    def mutate(self, child):
        for i in xrange(len(child)):
            if random < self.mutationRate:
                j = randint(0,len(child))
                child[i], child[j] = child[j], child[i]
        return child
        
    def getfittest(self, population):
        best = population[0]
        for p in population:
            best = self.cdom(best, p)
        return best
        
    def getweakest(self, population):
        weak = population[0]
        for p in population:
            weak = self.cdom(weak, p, True)
        return weak
        
    def evolve(self, population):
        mom = population.remove(self.getfittest(population))
        dad = population.remove(self.getfittest(population))
        child = self.crossover(mom, dad)
        population.remove(self.getweakest(population))
        population.append(mom)
        population.append(dad)
        population.append(child)