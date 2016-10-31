from Schaffer import *
from Osyczka2 import *
from Kursawe import *
from SA import *
from Maxwalksat import *
import sys

sys.dont_write_bytecode = True

sa = SA()
mws = Maxwalksat()

for model in [Schaffer, Osyczka2, Kursawe]:
    for optimizer in [sa.sa, mws.mws]:
        print ""
        sys.stdout.flush()
        print(optimizer)
        print(model)
        print optimizer(model())
