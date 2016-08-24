from swampy.TurtleWorld import *
import math

world = TurtleWorld()
bob = Turtle()
print bob


def arc(t, r, angle):
    arc_length = 2 * math.pi * r * angle / 360
    n = int(arc_length / 3) + 1
    step_length = arc_length / n
    step_angle = float(angle) / n
    
    for i in range(n):
        fd(t, step_length)
        lt(t, step_angle)
	
arc(bob, 50, 50)
arc(bob, 50, 220)

wait_for_user()
