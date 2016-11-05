import sys
from Schaffer import *
from Osyczka2 import *
from Kursawe import *

sys.dont_write_bytecode = True
epsilon = 0.001

class SA(object):
    def sa(self, model, kmax=1000, emax=625):
        def find_min_max(model, n_times=200):
            """
            sets the baseline minimum energy and maximum energy
            """
            rand_point = model.any(model)
            max_e = rand_point.energy
            for _ in xrange(n_times):
                rand_point = model.any(model)
                if rand_point.energy > max_e: max_e = rand_point.energy
            return max_e

        def prob(e, en, t, emax):
            global epsilon
            if t == float(0):
                t = epsilon
            var = float(en - e) / math.fabs(emax) / t
            return math.exp(var)

        def get_neighbor(point, k, retries=50):
            p = point.copypoint()
            while retries:
                decision = random.randint(0, len(p.decisions) - 1)
                p.decisions[decision] = random.randint(int(model.decisions[decision].low),int(model.decisions[decision].high))
                if model.ok(model, p):
                    model.eval(model, p)
                    model.points.append(p)
                    return p
                else:
                    p.decisions = point.decisions
                    retries -= 1
            return point
        model.__init__()
        s = model.any(model)
        sb = s
        k = kmax
        emax = find_min_max(model)
        while k > 0 and sb.energy < emax:
            sn = get_neighbor(s, k)
            if k % 25 == 0:
                print ""
                print format(k, '12d'), ' ',
                print format(sb.energy, '12d'), ' ',
                print format(sn.energy, '12d'), ' ',
            if sn.energy > sb.energy:
                sb = sn
                display('!')
            if sn.energy > s.energy:
                s = sn
                display('+')
            elif prob(s.energy, sn.energy, float(k) / float(kmax), emax) < random.random():
                s = sn
                display('?')
            else:
                display('.')
            k -= 1
        print ""
        return sb