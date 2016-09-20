from __future__ import division,print_function
import sys,re,traceback,random,string,math, numpy, time
sys.dont_write_bytecode=True

class SA(object):
    """ This class is used to encapsulate all functionality related to Simulated Annealing"""

    class Schaffer(object):
        """ This class is used to encapsulate all functionality related to schaffer model """
        lower_bound = pow(-10, 5)
        upper_bound = pow(10, 5)

        @staticmethod
        def f1(s):
            if s >= SA.Schaffer.upper_bound or s <= SA.Schaffer.lower_bound:
                raise ValueError("Illegal value of x in calculation of f1, out of bounds, value of is: " + str(s))
            f1_ret = pow(s, 2)
            return f1_ret

        @staticmethod
        def f2(s):
            if s >= SA.Schaffer.upper_bound or s <= SA.Schaffer.lower_bound:
                raise ValueError("Illegal value of x in calculation of f1, out of bounds, value of is: " + str(s))
            f2_ret = pow(s-2, 2)
            return f2_ret

    def __init__(self, kmax = 1000, seed = 1, emax = -1, s0 = 0):
        self.kmax = kmax
        random.seed(seed)
        self.s0 = s0
        self.schaffer_max, self.schaffer_min = self.__calculate_max_min(100)
        self.emax = emax

    @staticmethod
    def __calculate_max_min(iterations):
        """ Calculate the maximum and minimum of the sum of f1(s) and f2(s) over a range of random values for s """
        arr = []
        for i in xrange(iterations+1):
            # random state
            s = random.randint(SA.Schaffer.lower_bound, SA.Schaffer.upper_bound)
            sum = SA.Schaffer.f1(s) + SA.Schaffer.f2(s)
            arr.append(sum)
        return numpy.amin(arr), numpy.amax(arr)

    def p(self, e, en, ratio):
        """ This is the function p used to determine whether we jump to a '?' value """
        
        # Since we start from a high temperature and count down to 0, 
        # the ratio value needs to be small to give large 'val' for high temperatures and low 'val' for low temperatures
        ratio = 1 - ratio

        # This value is large when ratio is small
        val =  pow(math.e, ((e - en) / ratio))
        return val

    def E(self, s):
        """ This is used to compute the energy at a given state, schaffer_max and schaffer_min are computed at init """
        return ((SA.Schaffer.f1(s) + SA.Schaffer.f2(s)) - self.schaffer_min) / (self.schaffer_max - self.schaffer_min)

    def neighbor(self, s, k):
        """ This method computes the neighbor of s, for high temperatures the jump will be larger and as the temperature becomes low, jumps become smaller"""
        factor = k/self.kmax
        while True:
            s += random.randint(int(SA.Schaffer.lower_bound - s), int(SA.Schaffer.upper_bound - s)) * factor
            if s > SA.Schaffer.lower_bound and s < SA.Schaffer.upper_bound:
                break
        return s

    def minimize(self):
        """ This method is used to minimize using Schaffer, it implements algorithm explained in problem doc """
            s = self.s0
            e = self.E(s)
            sb = s
            eb = e
            k = self.kmax

            while k > 0 and e > self.emax:
                sn = self.neighbor(s, k)
                en = self.E(sn)

                if k % 25 == 0: print("\n%04d, %3.2f, " % (k, eb), end="")

                if en < eb:
                    sb = sn
                    eb = en
                    print("!", end="")
                elif en < e:
                    s = sn
                    e = en
                    print("+", end="")
                elif self.p(e, en, k/self.kmax) < random.random():
                    s = sn
                    e = en
                    print("?", end="")
                print(".", end="")
                k = k-1
            return sb, eb


if __name__ == '__main__':
    print("#########saDemo############")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    print("!!! Schaffer")

    # These are the default values of kmax, seed, emax and s0
    kmax = 1000
    seed = 1
    emax = -1
    s0 = 0

    # parameters can also be taken from user input
    if len(sys.argv) >= 2:
        kmax = int(sys.argv[1])
    if len(sys.argv) >= 3:
        seed = int(sys.argv[2])
    if len(sys.argv) >= 4:
        emax = int(sys.argv[3])
    if len(sys.argv) >= 5:
        s0 = int(sys.argv[4])

    print("kmax is: %s, seed is: %s, emax is: %s, s0 is: %s" % (kmax, seed, emax, s0))
    sa = SA(kmax, seed, emax, s0)
    sb, eb = sa.minimize()

    print("\nsb = %s" % (sb))
    print("eb = %s" % (eb))
