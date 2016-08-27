from swampy.TurtleWorld import *
import math

world = TurtleWorld()
bob = Turtle()
bob.delay = 0.001

def arc(t, r, angle):
    """
    draw arc using the turtle with a raius and for an angle measure
    """
    arc_length = 2 * math.pi * r * angle / 360
    n = int(arc_length / 3) + 1
    step_length = arc_length / n
    step_angle = float(angle) / n
    
    for i in range(n):
        fd(t, step_length)
        lt(t, step_angle)
	

def draw_flower(rad, ang, f, petl):
    """
    Draw the flower with the radius, angle, overlap factor and number of petals
    """
    rang = 180 - ang
    for i in range (petl):
        arc(bob, rad, ang)
        lt(bob, rang)
        arc(bob, rad, ang)
        lt(bob, rang + (ang/f))
    lt(bob, -bob.get_heading())

def move(t, length):
    """
    Move Turtle (t) forward (length) units without leaving a trail.
    Leaves the pen down.
    """
    pu(t)	
    fd(t, length)
    pd(t)
	
draw_flower(75, 50, 1, 7)
move(bob, 300)
draw_flower(50, 70, 2, 10)
#lt(bob, -bob.get_heading())
move(bob, 300)
draw_flower(150, 20, 1, 18)
wait_for_user()
