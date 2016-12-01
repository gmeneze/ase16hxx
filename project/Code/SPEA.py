import array, random, math, sys, numpy
from deap import creator, base, tools, algorithms

class SPEA(object):
    def __init__(self, problem):
        self.problem = problem
        self.distance_map = problem.cost_matrix
        self.speed_map = problem.speed_matrix
        self.IND_SIZE = problem.num_of_nodes
        self.toolbox = base.Toolbox()
        self.initdeap()

    def initdeap(self):
        creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, 1.0))
        creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMulti)
        self.toolbox.register("indices", random.sample, range(self.IND_SIZE), self.IND_SIZE)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.indices)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("mate", tools.cxPartialyMatched)
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
        self.toolbox.register("select", tools.selSPEA2)
        self.toolbox.register("evaluate", self.evalTSP)

    def evalTSP(self, individual):
        j, k = individual[-1], individual[0]
        distance = self.distance_map[j][k]
        time = self.distance_map[j][k] / self.speed_map[j][k]
        satisfaction = 0
        for gene1, gene2 in zip(individual[0:-1], individual[1:]):
            j, k = gene1, gene2
            distance += self.distance_map[j][k]
            time += self.distance_map[j][k] / self.speed_map[j][k]

            if time < self.problem.nodelist[k].latestReach:
                satisfaction += self.problem.nodelist[k].satisfaction
            time += self.problem.nodelist[k].duration
        return distance, time, satisfaction,

    def bdom(self, ind1, ind2, rev = False):
        x = [ind1.fitness.values[0], ind1.fitness.values[1], ind1.fitness.values[2]]
        y = [ind2.fitness.values[0], ind2.fitness.values[1], ind2.fitness.values[2]]
        less = 0
        dominates = True
        i = 0
        for obj, obj1 in zip(x, y):
            if ind1.fitness.weights[i] < 0:
                if obj > obj1:
                    dominates = False
                    break
                elif obj < obj1:
                    less = 1
            else:
                if obj < obj1:
                    dominates = False
                    break
                elif obj > obj1:
                    less = 1
            i += 1
        if dominates:
            if less == 0:
                dominates = False
            else:
                dominates = True
        if rev:
            return not dominates
        else:
            return dominates

    def cdom(self, node1, node2, rev = False):
        x = [node1.fitness.values[0], node1.fitness.values[1], node1.fitness.values[2]]
        y = [node2.fitness.values[0], node2.fitness.values[1], node2.fitness.values[2]]

        def w(i):
            return -1 if node1.fitness.weights[i] < 0 else 1

        def expLoss(w, x1, y1, n):
            try:
                return -1 * math.e ** (w * (x1 - y1) / n)
            except:
                return sys.maxsize

        def loss(x, y):
            losses = []
            n = min(len(x), len(y))
            i = 0
            for obj, obj1 in zip(x, y):
                x1, y1 = obj, obj1
                losses += [expLoss(w(i), x1, y1, n)]
                i += 1
            return sum(losses) / n

        l1 = loss(x, y)
        l2 = loss(y, x)

        response = l1 < l2
        if rev:
            return not response
        else:
            return response

    def condition(self, dom, dominated):
        if dom == self.bdom:
            if dominated == 0:
                return True
        elif dom == self.cdom:
            if dominated < 20:
                return True
        return False

    def main(self, dom):
        random.seed(169)

        NGEN = 25#0
        MU = 100
        CXPB = 0.9

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        # stats.register("avg", numpy.mean, axis=0)
        # stats.register("std", numpy.std, axis=0)
        stats.register("min", numpy.min, axis=0)
        stats.register("max", numpy.max, axis=0)

        logbook = tools.Logbook()
        logbook.header = "gen", "evals", "std", "min", "avg", "max"

        pop = self.toolbox.population(n=MU)
        #pop = self.toolbox.population(n=300)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in pop if not ind.fitness.valid]
        fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # This is just to assign the crowding distance to the individuals
        # no actual selection is done
        pop = self.toolbox.select(pop, len(pop))

        record = stats.compile(pop)
        logbook.record(gen=0, evals=len(invalid_ind), **record)
        print(logbook.stream)

        # Begin the generational process
        for gen in range(1, NGEN):
            # Vary the population
            #offspring = tools.selTournamentDCD(pop, len(pop))
            offspring = pop
            offspring = [self.toolbox.clone(ind) for ind in offspring]

            for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
                if random.random() <= CXPB:
                    self.toolbox.mate(ind1, ind2)

                self.toolbox.mutate(ind1)
                self.toolbox.mutate(ind2)
                del ind1.fitness.values, ind2.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # Select the next generation population
            pop = self.toolbox.select(pop + offspring, MU)
            record = stats.compile(pop)
            logbook.record(gen=gen, evals=len(invalid_ind), **record)
            print(logbook.stream)

        pareto = []
        for ind in pop:
            dominates = 0
            dominated = 0
            for oth in pop:
                if oth == ind:
                    continue
                if dom(ind, oth):
                    dominates += 1
                elif dom(oth, ind):
                    dominated += 1
            if self.condition(dom, dominated):
                pareto.append(ind)
        #print("Final population hypervolume is %f" % tools.hypervolume(pop, [11.0, 11.0]))
        return pop, logbook, pareto
