import sys
import random
import numpy
import bisect

from collections import Sequence, defaultdict
from itertools import repeat, chain
from math import sin, cos, pi, exp, e, sqrt
from operator import attrgetter, itemgetter
from copy import deepcopy
from Support import Statistics, Logbook
from Solution import Solution

class NSGA(object):
    def __init__(self, problem):
        self.problem = problem
        self.cost_matrix = problem.cost_matrix
        self.speed_matrix = problem.speed_matrix

    def uniform(self, low = 0.0, up = 1.0, size=30):
        try:
            return [random.uniform(a, b) for a, b in zip(low, up)]
        except TypeError:
            return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]

    def zdt1(self, individual):
        """ZDT1 multiobjective function.

        :math:`g(\\mathbf{x}) = 1 + \\frac{9}{n-1}\\sum_{i=2}^n x_i`

        :math:`f_{\\text{ZDT1}1}(\\mathbf{x}) = x_1`

        :math:`f_{\\text{ZDT1}2}(\\mathbf{x}) = g(\\mathbf{x})\\left[1 - \\sqrt{\\frac{x_1}{g(\\mathbf{x})}}\\right]`
        """
        g = 1.0 + 9.0 * sum(individual[1:]) / (len(individual) - 1)
        f1 = individual[0]
        f2 = g * (1 - sqrt(f1 / g))

        return f1, f2

    def mutPolynomialBounded(self, individual, eta = 20.0, low = 0.0, up = sys.maxsize, indpb = 1.0/30):
        """Polynomial mutation as implemented in original NSGA-II algorithm in
        C by Deb.

        :param individual: :term:`Sequence <sequence>` individual to be mutated.
        :param eta: Crowding degree of the mutation. A high eta will produce
                    a mutant resembling its parent, while a small eta will
                    produce a solution much more different.
        :param low: A value or a :term:`python:sequence` of values that
                    is the lower bound of the search space.
        :param up: A value or a :term:`python:sequence` of values that
                   is the upper bound of the search space.
        :returns: A tuple of one individual.
        """
        size = 3
        if not isinstance(low, Sequence):
            low = repeat(low, size)
        elif len(low) < size:
            raise IndexError("low must be at least the size of individual: %d < %d" % (len(low), size))
        if not isinstance(up, Sequence):
            up = repeat(up, size)
        elif len(up) < size:
            raise IndexError("up must be at least the size of individual: %d < %d" % (len(up), size))

        indobj = [individual.distance.value, individual.time.value, individual.satisfaction.value]
        for i, xl, xu in zip(xrange(size), low, up):
            if random.random() <= indpb:
                x = indobj[i]
                delta_1 = (x - xl) / (xu - xl)
                delta_2 = (xu - x) / (xu - xl)
                rand = random.random()
                mut_pow = 1.0 / (eta + 1.)

                if rand < 0.5:
                    xy = 1.0 - delta_1
                    val = 2.0 * rand + (1.0 - 2.0 * rand) * xy ** (eta + 1)
                    delta_q = val ** mut_pow - 1.0
                else:
                    xy = 1.0 - delta_2
                    val = 2.0 * (1.0 - rand) + 2.0 * (rand - 0.5) * xy ** (eta + 1)
                    delta_q = 1.0 - val ** mut_pow

                x = x + delta_q * (xu - xl)
                x = min(max(x, xl), xu)
                indobj[i] = x

        return individual,


    def initRepeat(self, container, func, n):
        """Call the function *container* with a generator function corresponding
        to the calling *n* times the function *func*.

        :param container: The type to put in the data from func.
        :param func: The function that will be called n times to fill the
                     container.
        :param n: The number of times to repeat func.
        :returns: An instance of the container filled with data from func.

        This helper function can can be used in conjunction with a Toolbox
        to register a generator of filled containers, as individuals or
        population.

            >>> initRepeat(list, random.random, 2) # doctest: +ELLIPSIS,
            ...                                    # doctest: +NORMALIZE_WHITESPACE
            [0.4761..., 0.6302...]
        See the :ref:`list-of-floats` and :ref:`population` tutorials for more examples.
        """

        return container(func() for _ in xrange(n))

    def cxSimulatedBinaryBounded(self, ind1, ind2, eta= 20.0, low = 0.0, up = sys.maxsize):
        """Executes a simulated binary crossover that modify in-place the input
        individuals. The simulated binary crossover expects :term:`sequence`
        individuals of floating point numbers.

        :param ind1: The first individual participating in the crossover.
        :param ind2: The second individual participating in the crossover.
        :param eta: Crowding degree of the crossover. A high eta will produce
                    children resembling to their parents, while a small eta will
                    produce solutions much more different.
        :param low: A value or a :term:`python:sequence` of values that is the lower
                    bound of the search space.
        :param up: A value or a :term:`python:sequence` of values that is the upper
                   bound of the search space.
        :returns: A tuple of two individuals.
        This function uses the :func:`~random.random` function from the python base
        :mod:`random` module.
        .. note::
           This implementation is similar to the one implemented in the
           original NSGA-II C code presented by Deb.
        """
        size = 3
        if not isinstance(low, Sequence):
            low = repeat(low, size)
        elif len(low) < size:
            raise IndexError("low must be at least the size of the shorter individual: %d < %d" % (len(low), size))
        if not isinstance(up, Sequence):
            up = repeat(up, size)
        elif len(up) < size:
            raise IndexError("up must be at least the size of the shorter individual: %d < %d" % (len(up), size))

        indobj1 = [ind1.distance.value, ind1.time.value, ind1.satisfaction.value]
        indobj2 = [ind2.distance.value, ind2.time.value, ind2.satisfaction.value]
        for i, xl, xu in zip(xrange(size), low, up):
            if random.random() <= 0.5:
                # This epsilon should probably be changed for 0 since
                # floating point arithmetic in Python is safer
                if abs(indobj1[i] - indobj2[i]) > 1e-14:
                    x1 = min(indobj1[i], indobj2[i])
                    x2 = max(indobj1[i], indobj2[i])
                    rand = random.random()

                    beta = 1.0 + (2.0 * (x1 - xl) / (x2 - x1))
                    alpha = 2.0 - beta ** -(eta + 1)
                    if rand <= 1.0 / alpha:
                        beta_q = (rand * alpha) ** (1.0 / (eta + 1))
                    else:
                        beta_q = (1.0 / (2.0 - rand * alpha)) ** (1.0 / (eta + 1))

                    c1 = 0.5 * (x1 + x2 - beta_q * (x2 - x1))

                    beta = 1.0 + (2.0 * (xu - x2) / (x2 - x1))
                    alpha = 2.0 - beta ** -(eta + 1)
                    if rand <= 1.0 / alpha:
                        beta_q = (rand * alpha) ** (1.0 / (eta + 1))
                    else:
                        beta_q = (1.0 / (2.0 - rand * alpha)) ** (1.0 / (eta + 1))
                    c2 = 0.5 * (x1 + x2 + beta_q * (x2 - x1))

                    c1 = min(max(c1, xl), xu)
                    c2 = min(max(c2, xl), xu)

                    if random.random() <= 0.5:
                        indobj1[i] = c2
                        indobj2[i] = c1
                    else:
                        indobj1[i] = c1
                        indobj2[i] = c2

        return ind1, ind2

    def selNSGA2(self, individuals, k, nd='standard'):
        """Apply NSGA-II selection operator on the *individuals*. Usually, the
        size of *individuals* will be larger than *k* because any individual
        present in *individuals* will appear in the returned list at most once.
        Having the size of *individuals* equals to *k* will have no effect other
        than sorting the population according to their front rank. The
        list returned contains references to the input *individuals*. For more
        details on the NSGA-II operator see [Deb2002]_.

        :param individuals: A list of individuals to select from.
        :param k: The number of individuals to select.
        :param nd: Specify the non-dominated algorithm to use: 'standard' or 'log'.
        :returns: A list of selected individuals.

        .. [Deb2002] Deb, Pratab, Agarwal, and Meyarivan, "A fast elitist
           non-dominated sorting genetic algorithm for multi-objective
           optimization: NSGA-II", 2002.
        """
        if nd == 'standard':
            pareto_fronts = self.sortNondominated(individuals, k)
        elif nd == 'log':
            pareto_fronts = self.sortLogNondominated(individuals, k)
        else:
            raise Exception('selNSGA2: The choice of non-dominated sorting '
                            'method "{0}" is invalid.'.format(nd))

        for front in pareto_fronts:
            self.assignCrowdingDist(front)

        chosen = list(chain(*pareto_fronts[:-1]))
        k = k - len(chosen)
        if k > 0:
            sorted_front = sorted(pareto_fronts[-1], key=attrgetter("crowding_dist"), reverse=True)
            chosen.extend(sorted_front[:k])

        return chosen

    def identity(self, obj):
        """Returns directly the argument *obj*.
        """
        return obj

    def median(self, seq, key=identity):
        """Returns the median of *seq* - the numeric value separating the higher
        half of a sample from the lower half. If there is an even number of
        elements in *seq*, it returns the mean of the two middle values.
        """
        sseq = sorted(seq, key=key)
        length = len(seq)
        if length % 2 == 1:
            return key(sseq[(length - 1) // 2])
        else:
            return (key(sseq[(length - 1) // 2]) + key(sseq[length // 2])) / 2.0

    def isDominated(self, wvalues1, wvalues2):
        """Returns whether or not *wvalues1* dominates *wvalues2*.

        :param wvalues1: The weighted fitness values that would be dominated.
        :param wvalues2: The weighted fitness values of the dominant.
        :returns: :obj:`True` if wvalues2 dominates wvalues1, :obj:`False`
                  otherwise.
        """
        not_equal = False
        for self_wvalue, other_wvalue in zip(wvalues1, wvalues2):
            if self_wvalue > other_wvalue:
                return False
            elif self_wvalue < other_wvalue:
                not_equal = True
        return not_equal

    def sortLogNondominated(self,individuals, k, first_front_only=False):
        """Sort *individuals* in pareto non-dominated fronts using the Generalized
        Reduced Run-Time Complexity Non-Dominated Sorting Algorithm presented by
        Fortin et al. (2013).

        :param individuals: A list of individuals to select from.
        :returns: A list of Pareto fronts (lists), with the first list being the
                  true Pareto front.
        """
        if k == 0:
            return []

        # Separate individuals according to unique fitnesses
        unique_fits = defaultdict(list)
        for i, ind in enumerate(individuals):
            unique_fits[ind.fitness.wvalues].append(ind)

        # Launch the sorting algorithm
        obj = len(individuals[0].fitness.wvalues) - 1
        fitnesses = unique_fits.keys()
        front = dict.fromkeys(fitnesses, 0)

        # Sort the fitnesses lexicographically.
        fitnesses.sort(reverse=True)
        self.sortNDHelperA(fitnesses, obj, front)

        # Extract individuals from front list here
        nbfronts = max(front.values()) + 1
        pareto_fronts = [[] for i in range(nbfronts)]
        for fit in fitnesses:
            index = front[fit]
            pareto_fronts[index].extend(unique_fits[fit])

        # Keep only the fronts required to have k individuals.
        if not first_front_only:
            count = 0
            for i, front in enumerate(pareto_fronts):
                count += len(front)
                if count >= k:
                    return pareto_fronts[:i + 1]
            return pareto_fronts
        else:
            return pareto_fronts[0]

    def sortNDHelperA(self, fitnesses, obj, front):
        """Create a non-dominated sorting of S on the first M objectives"""
        if len(fitnesses) < 2:
            return
        elif len(fitnesses) == 2:
            # Only two individuals, compare them and adjust front number
            s1, s2 = fitnesses[0], fitnesses[1]
            if self.isDominated(s2[:obj + 1], s1[:obj + 1]):
                front[s2] = max(front[s2], front[s1] + 1)
        elif obj == 1:
            self.sweepA(fitnesses, front)
        elif len(frozenset(map(itemgetter(obj), fitnesses))) == 1:
            # All individuals for objective M are equal: go to objective M-1
            self.sortNDHelperA(fitnesses, obj - 1, front)
        else:
            # More than two individuals, split list and then apply recursion
            best, worst = self.splitA(fitnesses, obj)
            self.sortNDHelperA(best, obj, front)
            self.sortNDHelperB(best, worst, obj - 1, front)
            self.sortNDHelperA(worst, obj, front)

    def sweepA(self, fitnesses, front):
        """Update rank number associated to the fitnesses according
        to the first two objectives using a geometric sweep procedure.
        """
        stairs = [-fitnesses[0][1]]
        fstairs = [fitnesses[0]]
        for fit in fitnesses[1:]:
            idx = bisect.bisect_right(stairs, -fit[1])
            if 0 < idx <= len(stairs):
                fstair = max(fstairs[:idx], key=front.__getitem__)
                front[fit] = max(front[fit], front[fstair] + 1)
            for i, fstair in enumerate(fstairs[idx:], idx):
                if front[fstair] == front[fit]:
                    del stairs[i]
                    del fstairs[i]
                    break
            stairs.insert(idx, -fit[1])
            fstairs.insert(idx, fit)

    def splitA(self, fitnesses, obj):
        """Partition the set of fitnesses in two according to the median of
        the objective index *obj*. The values equal to the median are put in
        the set containing the least elements.
        """
        median_ = self.median(fitnesses, itemgetter(obj))
        best_a, worst_a = [], []
        best_b, worst_b = [], []

        for fit in fitnesses:
            if fit[obj] > median_:
                best_a.append(fit)
                best_b.append(fit)
            elif fit[obj] < median_:
                worst_a.append(fit)
                worst_b.append(fit)
            else:
                best_a.append(fit)
                worst_b.append(fit)

        balance_a = abs(len(best_a) - len(worst_a))
        balance_b = abs(len(best_b) - len(worst_b))

        if balance_a <= balance_b:
            return best_a, worst_a
        else:
            return best_b, worst_b

    def sortNDHelperB(self, best, worst, obj, front):
        """Assign front numbers to the solutions in H according to the solutions
        in L. The solutions in L are assumed to have correct front numbers and the
        solutions in H are not compared with each other, as this is supposed to
        happen after sortNDHelperB is called."""
        key = itemgetter(obj)
        if len(worst) == 0 or len(best) == 0:
            # One of the lists is empty: nothing to do
            return
        elif len(best) == 1 or len(worst) == 1:
            # One of the lists has one individual: compare directly
            for hi in worst:
                for li in best:
                    if self.isDominated(hi[:obj + 1], li[:obj + 1]) or hi[:obj + 1] == li[:obj + 1]:
                        front[hi] = max(front[hi], front[li] + 1)
        elif obj == 1:
            self.sweepB(best, worst, front)
        elif key(min(best, key=key)) >= key(max(worst, key=key)):
            # All individuals from L dominate H for objective M:
            # Also supports the case where every individuals in L and H
            # has the same value for the current objective
            # Skip to objective M-1
            self.sortNDHelperB(best, worst, obj - 1, front)
        elif key(max(best, key=key)) >= key(min(worst, key=key)):
            best1, best2, worst1, worst2 = self.splitB(best, worst, obj)
            self.sortNDHelperB(best1, worst1, obj, front)
            self.sortNDHelperB(best1, worst2, obj - 1, front)
            self.sortNDHelperB(best2, worst2, obj, front)

    def splitB(self, best, worst, obj):
        """Split both best individual and worst sets of fitnesses according
        to the median of objective *obj* computed on the set containing the
        most elements. The values equal to the median are attributed so as
        to balance the four resulting sets as much as possible.
        """
        median_ = self.median(best if len(best) > len(worst) else worst, itemgetter(obj))
        best1_a, best2_a, best1_b, best2_b = [], [], [], []
        for fit in best:
            if fit[obj] > median_:
                best1_a.append(fit)
                best1_b.append(fit)
            elif fit[obj] < median_:
                best2_a.append(fit)
                best2_b.append(fit)
            else:
                best1_a.append(fit)
                best2_b.append(fit)

        worst1_a, worst2_a, worst1_b, worst2_b = [], [], [], []
        for fit in worst:
            if fit[obj] > median_:
                worst1_a.append(fit)
                worst1_b.append(fit)
            elif fit[obj] < median_:
                worst2_a.append(fit)
                worst2_b.append(fit)
            else:
                worst1_a.append(fit)
                worst2_b.append(fit)

        balance_a = abs(len(best1_a) - len(best2_a) + len(worst1_a) - len(worst2_a))
        balance_b = abs(len(best1_b) - len(best2_b) + len(worst1_b) - len(worst2_b))

        if balance_a <= balance_b:
            return best1_a, best2_a, worst1_a, worst2_a
        else:
            return best1_b, best2_b, worst1_b, worst2_b

    def sweepB(self, best, worst, front):
        """Adjust the rank number of the worst fitnesses according to
        the best fitnesses on the first two objectives using a sweep
        procedure.
        """
        stairs, fstairs = [], []
        iter_best = iter(best)
        next_best = next(iter_best, False)
        for h in worst:
            while next_best and h[:2] <= next_best[:2]:
                insert = True
                for i, fstair in enumerate(fstairs):
                    if front[fstair] == front[next_best]:
                        if fstair[1] > next_best[1]:
                            insert = False
                        else:
                            del stairs[i], fstairs[i]
                        break
                if insert:
                    idx = bisect.bisect_right(stairs, -next_best[1])
                    stairs.insert(idx, -next_best[1])
                    fstairs.insert(idx, next_best)
                next_best = next(iter_best, False)

            idx = bisect.bisect_right(stairs, -h[1])
            if 0 < idx <= len(stairs):
                fstair = max(fstairs[:idx], key=front.__getitem__)
                front[h] = max(front[h], front[fstair] + 1)


    def sortNondominated(self, individuals, k, first_front_only=False):
        """Sort the first *k* *individuals* into different nondomination levels
        using the "Fast Nondominated Sorting Approach" proposed by Deb et al.,
        see [Deb2002]_. This algorithm has a time complexity of :math:`O(MN^2)`,
        where :math:`M` is the number of objectives and :math:`N` the number of
        individuals.

        :param individuals: A list of individuals to select from.
        :param k: The number of individuals to select.
        :param first_front_only: If :obj:`True` sort only the first front and
                                 exit.
        :returns: A list of Pareto fronts (lists), the first list includes
                  nondominated individuals.
        .. [Deb2002] Deb, Pratab, Agarwal, and Meyarivan, "A fast elitist
           non-dominated sorting genetic algorithm for multi-objective
           optimization: NSGA-II", 2002.
        """
        if k == 0:
            return []

        map_fit_ind = defaultdict(list)
        for ind in individuals:
            map_fit_ind[ind.fitness].append(ind)
        fits = map_fit_ind.keys()

        current_front = []
        next_front = []
        dominating_fits = defaultdict(int)
        dominated_fits = defaultdict(list)

        # Rank first Pareto front
        for i, fit_i in enumerate(individuals):
            for fit_j in individuals[i + 1:]:
                if fit_i.dominates(fit_j):
                    dominating_fits[fit_j] += 1
                    dominated_fits[fit_i].append(fit_j)
                elif fit_j.dominates(fit_i):
                    dominating_fits[fit_i] += 1
                    dominated_fits[fit_j].append(fit_i)
            if dominating_fits[fit_i] == 0:
                current_front.append(fit_i)

        fronts = [[]]
        for fit in current_front:
            fronts[-1].extend(map_fit_ind[fit.fitness])
        pareto_sorted = len(fronts[-1])

        # Rank the next front until all individuals are sorted or
        # the given number of individual are sorted.
        if not first_front_only:
            N = min(len(individuals), k)
            while pareto_sorted < N:
                fronts.append([])
                for fit_p in current_front:
                    for fit_d in dominated_fits[fit_p]:
                        dominating_fits[fit_d] -= 1
                        if dominating_fits[fit_d] == 0:
                            next_front.append(fit_d)
                            pareto_sorted += len(map_fit_ind[fit_d.fitness])
                            fronts[-1].extend(map_fit_ind[fit_d])
                current_front = next_front
                next_front = []

        return fronts

    def assignCrowdingDist(self, individuals):
        """Assign a crowding distance to each individual's fitness. The
        crowding distance can be retrieve via the :attr:`crowding_dist`
        attribute of each individual's fitness.
        """
        if len(individuals) == 0:
            return

        distances = [0.0] * len(individuals)
        crowd = [(ind.fitness, i) for i, ind in enumerate(individuals)]

        nobj = len(individuals)

        for i in xrange(nobj):
            #crowd.sort(key=lambda element: element[0][i])
            crowd.sort()
            distances[crowd[0][1]] = float("inf")
            distances[crowd[-1][1]] = float("inf")
            if crowd[-1][0] == crowd[0][0]:
                continue
            norm = nobj * float(crowd[-1][0] - crowd[0][0])
            for prev, cur, next in zip(crowd[:-2], crowd[1:-1], crowd[2:]):
                distances[cur[1]] += (next[0] - prev[0]) / norm

        for i, dist in enumerate(distances):
            individuals[i].crowding_dist = dist

    def selTournamentDCD(self, individuals, k):
        """Tournament selection based on dominance (D) between two individuals, if
        the two individuals do not interdominate the selection is made
        based on crowding distance (CD). The *individuals* sequence length has to
        be a multiple of 4. Starting from the beginning of the selected
        individuals, two consecutive individuals will be different (assuming all
        individuals in the input list are unique). Each individual from the input
        list won't be selected more than twice.

        This selection requires the individuals to have a :attr:`crowding_dist`
        attribute, which can be set by the :func:`assignCrowdingDist` function.

        :param individuals: A list of individuals to select from.
        :param k: The number of individuals to select.
        :returns: A list of selected individuals.
        """

        def tourn(ind1, ind2):
            if ind1.dominates(ind2):
                return ind1
            elif ind2.dominates(ind1):
                return ind2

            if ind1.crowding_dist < ind2.crowding_dist:
                return ind2
            elif ind1.crowding_dist > ind2.crowding_dist:
                return ind1

            if random.random() <= 0.5:
                return ind1
            return ind2

        individuals_1 = random.sample(individuals, len(individuals))
        individuals_2 = random.sample(individuals, len(individuals))
        k -= (k%4)
        chosen = []
        for i in xrange(0, k, 4):
            chosen.append(tourn(individuals_1[i], individuals_1[i + 1]))
            chosen.append(tourn(individuals_1[i + 2], individuals_1[i + 3]))
            chosen.append(tourn(individuals_2[i], individuals_2[i + 1]))
            chosen.append(tourn(individuals_2[i + 2], individuals_2[i + 3]))

        return chosen

    def generate_one_solution(self):
        nodelist = self.problem.nodelist
        i = random.randint(0,len(nodelist) - 1)
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
            i = (i + int(random.randint(0,len(nodelist))))%len(nodelist)

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

    def main(self, seed=None):
        random.seed(seed)

        NGEN = 250
        MU = 100
        CXPB = 0.9

        stats = Statistics(lambda ind: ind.fitness)
        # stats.register("avg", numpy.mean, axis=0)
        # stats.register("std", numpy.std, axis=0)
        stats.register("min", numpy.min, axis=0)
        stats.register("max", numpy.max, axis=0)

        logbook = Logbook()
        logbook.header = "gen", "evals", "std", "min", "avg", "max"

        pop = self.initRepeat(list, self.generate_one_solution, n=MU)

        for i in pop:
            i.getfitness(pop)

        # Evaluate the individuals with an invalid fitness
        #invalid_ind = [ind for ind in pop if not ind.fitness.valid]
        #fitnesses = map(self.zdt1, invalid_ind)
        #for ind, fit in zip(invalid_ind, fitnesses):
        #    ind.fitness.values = fit

        # This is just to assign the crowding distance to the individuals
        # no actual selection is done
        pop = self.selNSGA2(pop, len(pop))

        record = stats.compile(pop)
        #logbook.record(gen=0, evals=len(invalid_ind), **record)
        #print(logbook.stream)

        # Begin the generational process
        for gen in range(1, NGEN):
            # Vary the population
            offspring = self.selTournamentDCD(pop, len(pop))
            offspring = [deepcopy(ind) for ind in offspring]

            for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
                if random.random() <= CXPB:
                    self.cxSimulatedBinaryBounded(ind1, ind2)

                self.mutPolynomialBounded(ind1)
                self.mutPolynomialBounded(ind2)
                del ind1.fitness, ind2.fitness
                ind1.getfitness(pop)
                ind2.getfitness(pop)

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.valid]
            fitnesses = map(self.zdt1, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # Select the next generation population
            pop = self.selNSGA2(pop + offspring, MU)
            record = stats.compile(pop)
            logbook.record(gen=gen, evals=len(invalid_ind), **record)
            print(logbook.stream)

        #print("Final population hypervolume is %f" % hypervolume(pop, [11.0, 11.0]))

        return pop, logbook