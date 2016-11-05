from __future__ import division,print_function
import sys,re,traceback,random, string,math, numpy, time, copy
sys.dont_write_bytecode=True

class MaxWalkStat(object):
    """ This class is used to encapsulate all functionality related to Simulated Annealing"""
    max = 0
    min = 0
    seed = 0

    class Osyczka2(object):
        """ This class is used to encapsulate all functionality related to Simulated Annealing"""
        def __init__(self, x1, x2, x3, x4, x5, x6):
            self.x1 = x1
            self.x2 = x2
            self.x3 = x3
            self.x4 = x4
            self.x5 = x5
            self.x6 = x6

        def __repr__(self):
            sb = []
            return " \n x1:" + str(self.x1) + " \n x2:" + str(self.x2) + " \n x3:" + str(self.x3) + " \n x4:" + str(self.x4) + " \n x5:" + str(self.x5) + " \n x6:" + str(self.x6)

        def constraints(self):
            g1 = 0 <= self.x1 + self.x2 - 2
            g2 = 0 <= 6 - self.x1 - self.x2
            g3 = 0 <= 2 - self.x2 + self.x1
            g4 = 0 <= 2 - self.x1 + 3 * self.x2
            g5 = 0 <= 4 - (self.x3 - 3) ** 2 - self.x4
            g6 = 0 <= (self.x5 - 3) ** 3 + self.x6 - 4
            return g1 and g2 and g3 and g4 and g5 and g6

        def f1(self):
            return -(25 * (self.x1 - 2)**2 + (self.x2 - 2)**2 + (self.x3 - 1)**2 * (self.x4 - 4)**2 + (self.x5 - 1)**2)

        def f2(self):
            return self.x1**2 + self.x2**2 + self.x3**2 + self.x4**2 + self.x5**2 + self.x6**2

    @staticmethod
    def calculate_max_min(iterations, seed = 0):
        MaxWalkStat.seed = seed
        random.seed(MaxWalkStat.seed)
        arr = []
        for i in xrange(iterations+1):
            temp_solution = MaxWalkStat.Osyczka2(random.randint(0, 10), random.randint(0, 10), random.randint(1,5), random.randint(0,6), random.randint(1,5), random.randint(0, 10))
            # random state
            sum = temp_solution.f1() + temp_solution.f2()
            arr.append(sum)       
        MaxWalkStat.max, MaxWalkStat.min = numpy.amin(arr), numpy.amax(arr)

    @staticmethod
    def E(solution):
        """ This is used to compute the energy at a given state, schaffer_max and schaffer_min are computed at init """
        return ((solution.f1() + solution.f2()) - MaxWalkStat.min) / (MaxWalkStat.max - MaxWalkStat.min)

    @staticmethod
    def minimize(max_retries, max_changes):
        for i in xrange(1, max_retries+1):
            temp_solution = MaxWalkStat.Osyczka2(random.randint(0, 10), random.randint(0, 10), random.randint(1,5), random.randint(0,6), random.randint(1,5), random.randint(0, 10))
            
            # Threshold based on max_retries = 100, max_changes = 100 and seed = 0
            MaxWalkStat.threshold = 0.068868980963 
            for j in xrange(1, max_changes+1):
                if MaxWalkStat.E(temp_solution) < MaxWalkStat.threshold:
                    # if best solution is found
                    return {'status':True, 'solution':temp_solution}

                c = random.randint(1,6)

                if 0.5 < random.random():
                    # local search
                    while True:
                        if c == 1:
                            temp_solution.x1 = random.randint(0, 10)
                        elif c == 2:
                            temp_solution.x2 = random.randint(0, 10)
                        elif c == 3:
                            temp_solution.x3 = random.randint(1,5)
                        elif c == 4:
                            temp_solution.x4 = random.randint(0,6)
                        elif c == 5:
                            temp_solution.x5 = random.randint(1,5)
                        else:
                            temp_solution.x6 = random.randint(0,10)

                    if temp_solution.constraints():
                        break
                else:
                    # global search
                    while True:
                        new_solution = MaxWalkStat.Osyczka2(random.randint(0, 10), random.randint(0, 10), random.randint(1,5), random.randint(0,6), random.randint(1,5), random.randint(0, 10))
                        if new_solution.constraints():
                            if MaxWalkStat.E(new_solution) < MaxWalkStat.E(temp_solution):
                                temp_solution = copy.deepcopy(new_solution)
                                break

            # if no best solution is found after retries
            return {'status' : False, 'solution' : temp_solution}


if __name__ == '__main__':
    seed = 1
    max_retries = 10**3
    max_changes = 10**3
    if len(sys.argv) >= 2:
        seed = int(sys.argv[1])
    if len(sys.argv) >= 3:
        max_retries = int(sys.argv[2])
    if len(sys.argv) >= 4:
        max_changes = int(sys.argv[3])

    MaxWalkStat.calculate_max_min(max_retries, seed)
    result = MaxWalkStat.minimize(max_retries, max_changes)
    print("seed: %s \nsolution: %s \nThreshold : %s \nMin Energy: %s" %(MaxWalkStat.seed, result['solution'], MaxWalkStat.threshold, MaxWalkStat.E(result['solution'])))
