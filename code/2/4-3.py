from __future__ import division
from swampy.TurtleWorld import *
import math

world = TurtleWorld()
bob = Turtle()
#print bob
bob.delay = 0.01

def move(t, length):
    """
    Move Turtle (t) forward (length) units without leaving a trail.
    Leaves the pen down.
    """
    pu(t)
	
    fd(t, length)
    pd(t)

def triangle(t, s, l, l2):
    """
    Draw triangle using a turtle object, with for a number of sides, and the lengths of the triangle
    """
	an = 360/s
	ang = (180 - an)/2
	for i in range (3):
		if i%2 == 0:
			fd(t, l2)
		else:
			fd(t, l)
		lt(t, 180 - ang)
	lt (t, ang)
	
#for i in range (5):
#	triangle(bob, 5, 100, 85)

#for i in range (6):
#	triangle(bob, 6, 100, 100)
	
#for i in range (7):
#	triangle(bob, 7, 100, 115)

    
def draw_polygon(t, s, l, l2):
    for i in range (s):
        triangle (t, s, l, l2)
        


draw_polygon(bob, 5, 100, 85)
move(bob, 300)
draw_polygon(bob, 6, 100, 100)
move(bob, 300)
draw_polygon(bob, 7, 100, 115)

# dump the contents of the campus to the file canvas.eps

wait_for_user()
