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

    def __init__(self, kmax = 100, seed = 1, emax = -1, s0 = 0):
        self.kmax = kmax
        random.seed(seed)
        self.s0 = s0
        self.schaffer_max, self.schaffer_min = self.__calculate_max_min(100)
        self.emax = emax

    @staticmethod
    def __calculate_max_min(iterations):
        arr = []
        for i in xrange(iterations+1):
            # random state
            s = random.randint(SA.Schaffer.lower_bound, SA.Schaffer.upper_bound)
            sum = SA.Schaffer.f1(s) + SA.Schaffer.f2(s)
            arr.append(sum)
        return numpy.amin(arr), numpy.amax(arr)

    def p(self, e, en, ratio):
        ratio = 1 - ratio
        val =  pow(math.e, ((e - en) / ratio))
        return val

    def E(self, s):
        return ((SA.Schaffer.f1(s) + SA.Schaffer.f2(s)) - self.schaffer_min) / (self.schaffer_max - self.schaffer_min)

    def neighbor(self, s, k):
        factor = k/self.kmax
        while True:
            s += random.randint(SA.Schaffer.lower_bound, SA.Schaffer.upper_bound) * factor
            if s > SA.Schaffer.lower_bound and s < SA.Schaffer.upper_bound:
                break
        return s

    def minimize(self):
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

    sa = SA(1000,100,-1,3000)
    sb, eb = sa.minimize()

    print("\nsb = %s" % (sb))
    print("eb = %s" % (eb))
