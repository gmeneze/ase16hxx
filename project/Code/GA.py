from random import *
from Solution import Solution
import math

class GA(object):
    def __init__(self, problem, iterations = 10, currentSolution = [], bestSolution = [],
                        bestFitness = 0, population = [], mutationRate = 0.2):
        self.problem = problem
        self.cost_matrix = problem.cost_matrix
        self.speed_matrix = problem.speed_matrix
        self.iterations = iterations
        self.currentSolution = currentSolution
        self.bestSolution = bestSolution
        self.bestFitness = bestFitness
        self.population = population
        self.mutationRate = mutationRate
        
    def generate_population(self, nodelist, num = 10):
        self.population = [self.generate_one_solution(nodelist) for _ in range(num)]
                
                
    def generate_one_solution(self, nodelist):
        i = randint(0,len(nodelist) - 1)
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
            i = (i + int(randint(0,len(nodelist))))%len(nodelist)
        solution = Solution(path)
        solution.distance = self.get_totaldistance(path)
        solution.time, solution.satisfaction = self.get_totaltime(path)
        return solution
        
    def get_totaldistance(self, solution):
        cost = 0
        # print 'begin cost'
        # print solution
        # print solution.__len__()
        for i in range(solution.__len__() - 1):
            j = solution[i].id
            k = solution[i + 1].id
             # print j , k
            cost += self.cost_matrix[j][k]
        return cost

    def get_totaltime(self,solution):
        time = 0
        satisfaction = 0
        print solution
        for i in range(solution.__len__() - 1):
            j = solution[i].id
            k = solution[i + 1].id
            print j , k
            time += self.cost_matrix[j][k] / self.speed_matrix[j][k]
            if time < solution[i].latestReach:
                satisfaction += solution[i].satisfaction
            time += solution[i+1].duration
            print time
            # print 'end cost'
        return time, satisfaction
                    
    
    def cdom(self, node1, node2, rev = False):
        x = [node1.distance, node1.time, node1.satisfaction]
        y = [node2.distance, node2.time, node2.satisfaction]

        def w(better):
            return -1 if better == less else 1

        def expLoss(w, x1, y1, n):
            return -1 * math.e ** (w * (x1 - y1) / n)

        def loss(x, y):
            losses = []
            n = min(len(x), len(y))
            for obj in x:
                x1, y1 = x[obj.pos], y[obj.pos]
                x1, y1 = obj.norm(x1), obj.norm(y1)
                losses += [expLoss(w(obj.want), x1, y1, n)]
            return sum(losses) / n

        l1 = loss(x, y)
        l2 = loss(y, x)

        response = l1 < l2
        if rev:
            return not response
        else:
            return response
        
    def crossover(self, mom, dad):
        start = randint(0,len(mom.path)-2)
        end = randint(0,len(mom.path)-2)
        child = []
        if start > end:
            start, end = end, start
        for i in xrange(start, end + 1):
            child.append(mom.path[i])
        for i in xrange(len(dad.path)):
            if dad.path[i] not in child:
                child.append(dad.path[i])
        child.append(mom.path[start])
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
            if self.cdom(p, best):
                best = p
        return best
        
    def getweakest(self, population):
        weak = population[0]
        for p in population:
            if self.cdom(weak, p):
                weak = p
        return weak
        
    def evolve(self, population):
        mom = self.getfittest(population)
        population.remove(mom)
        dad = self.getfittest(population)
        population.remove(dad)
        child = self.crossover(mom, dad)
        dist = self.get_totaldistance(child)
        time= self.get_totaltime(child)
        childSolution = Solution(child,dist,time)
        weak = self.getweakest(population)
        if self.cdom(childSolution, weak):
            population.remove(weak)
            population.append(mom)
            population.append(dad)
            population.append(childSolution)


    def solve(self, nodelist):
        self.generate_population(nodelist)
        for _ in range(self.iterations):
            self.evolve(self.population)
        for i in (self.getfittest(self.population).path):
            print i.id,
        print ""