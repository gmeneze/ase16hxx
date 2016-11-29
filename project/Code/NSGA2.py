import numpy, array, random

from deap import creator, base, tools, algorithms



class NSGA2(object):
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
        self.toolbox.register("select", tools.selNSGA2)
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

    def main(self):
        random.seed(169)

        NGEN = 250
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
            offspring = tools.selTournamentDCD(pop, len(pop))
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

        #print("Final population hypervolume is %f" % tools.hypervolume(pop, [11.0, 11.0]))
        return pop, logbook