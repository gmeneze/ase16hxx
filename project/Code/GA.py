from random import *
from Solution import Solution
import math, sys

class GA(object):
    def __init__(self, problem, domn = "cdom", iterations = 250, currentSolution = [], bestSolution = [],
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
        self.domn = domn
        
    def generate_population(self, nodelist, num = 100):
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
        distance = self.get_totaldistance(path)
        time, satisfaction = self.get_totaltime(path)
        solution = Solution(path, distance, time, satisfaction)
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
        #print solution
        for i in range(solution.__len__() - 1):
            j = solution[i].id
            k = solution[i + 1].id
            #print j , k
            time += self.cost_matrix[j][k] / self.speed_matrix[j][k]
            if time < solution[i].latestReach:
                satisfaction += solution[i].satisfaction
            time += solution[i+1].duration
            #print time
            # print 'end cost'
        return time, satisfaction
                    
    
    def cdom(self, node1, node2, rev = False):
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

    def bdom(self, node1, node2, rev = False):
        x = [node1.distance, node1.time, node1.satisfaction]
        y = [node2.distance, node2.time, node2.satisfaction]
        less = 0
        dominates = True
        for obj, obj1 in zip(x,y):
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

    def dom(self, node1, node2, rev = False):
        if self.domn == "cdom":
            return self.cdom(node1, node2, rev)
        else:
            return self.bdom(node1, node2, rev)

        
    def crossover(self, mom, dad):
        start = randint(0,len(mom.path)-2)
        end = randint(0,len(mom.path)-2)
        child = []
        if start > end:
            start, end = end, start
        for i in range(start, end + 1):
            child.append(mom.path[i])
        for i in range(len(dad.path)):
            if dad.path[i] not in child:
                child.append(dad.path[i])
        child.append(mom.path[start])
        return child
    
    def mutate(self, child):
        for i in range(len(child)):
            if random < self.mutationRate:
                j = randint(0,len(child))
                child[i], child[j] = child[j], child[i]
        return child

    def condition(self, dom, dominated):
        if dom == "bdom":
            if dominated == 0:
                return True
        elif dom == "cdom":
            if dominated < 20:
                return True
        return False
        
    def getfittest(self, population):
        best = []
        for p in population:
            dominates = 0
            dominated = 0
            for oth in population:
                if self.dom(p, oth):
                    dominates += 1
                elif self.dom(oth,p):
                    dominated += 1
            if self.condition(self.domn, dominated):
                best.append(p)
        mind = 10000000
        try:
            b = best[randint(0,len(best) - 1)]
        except:
            b = population[randint(0,len(population) - 1)]
        for p in best:
            if p.distance.value < mind:
                b = p
                mind = p.distance.value
        return b
        
    def getweakest(self, population):
        weakest = None
        maxdominated = 0
        for p in population:
            dominates = 0
            dominated = 0
            for oth in population:
                if self.dom(p, oth):
                    dominates += 1
                elif self.dom(oth, p):
                    dominated += 1
            if dominated > maxdominated:
                maxdominated = dominated
                weakest = p
        if weakest == None:
            weakest = population[-1]
        return weakest
        
    def evolve(self, population):
        prob = 0.5
        if random() > prob:
            mom = self.getfittest(population)
            population.remove(mom)
            dad = self.getfittest(population)
            population.remove(dad)
        else:
            mom = population[randint(0,len(population) - 1)]
            population.remove(mom)
            dad = population[randint(0,len(population) - 1)]
            population.remove(dad)

        child = self.crossover(mom, dad)
        dist = self.get_totaldistance(child)
        time, satisfaction = self.get_totaltime(child)
        childSolution = Solution(child,dist,time, satisfaction)
        weak = self.getweakest(population)
        population.append(mom)
        population.append(dad)
        if self.dom(childSolution, weak):
            population.remove(weak)
            population.append(childSolution)

    def condition(self, dom, dominated):
        if dom == "bdom":
            if dominated == 0:
                return True
        elif dom == "cdom":
            if dominated < 20:
                return True
        return False

    def solve(self, nodelist):
        self.generate_population(nodelist)
        print ("Iterations")
        for i in range(self.iterations):
            if i %50 == 0:
                print(i, end='', flush=True)
            elif i % 5 == 0:
                print (".", end='', flush=True)
            self.evolve(self.population)
        fittest = self.getfittest(self.population)
        weakest = self.getweakest(self.population)
        print ("Population")
        for i in self.population:
            print (i.distance.value, i.time.value, i.satisfaction.value)
        print ("Now")
        print (fittest.distance.value, fittest.time.value, fittest.satisfaction.value)
        print(weakest.distance.value, weakest.time.value, weakest.satisfaction.value)
        pareto = []
        for ind in self.population:
            dominates = 0
            dominated = 0
            for oth in self.population:
                if oth == ind:
                    continue
                if self.dom(ind, oth):
                    dominates += 1
                elif self.dom(oth, ind):
                    dominated += 1
            if self.condition(self.domn, dominated):
                pareto.append(ind)
        return self.population, pareto
