from Graphics import *
class Drawer(object):
    def __init__(self):
        self.window_height = 700
        self.window_length = 700
        #self.nodelist = nodelist
        #self.route = route
        
    def draw_path(self, nodelist, route):
        self.nodelist = nodelist
        self.route = route
        win = GraphWin('TSP', self.window_length, self.window_height)
        for i in range(route.__len__()-1):
            point1 = Point(self.nodelist[route[i]].xcordinate,self.nodelist[route[i]].ycordinate)
            point2 = Point(self.nodelist[route[i+1]].xcordinate,self.nodelist[route[i+1]].ycordinate)
            circle1 = Circle(point1,5)
            circle1.setFill("red")
            circle1.draw(win)
            circle2 = Circle(point2, 5)
            circle2.setFill("red")
            circle2.draw(win)
	        #circle1 = Circle(point1,5)
    	    #circle1.setFill("yellow")
    	    #circle1.draw(win)
	        #circle2 = Circle(point2,5)
            #circle2.setFill("yellow")
            #circle2.draw(win)
            line1 = Line(point1,point2) 
            line1.setWidth(3)
            line1.draw(win)
        win.getMouse()
        win.close()
        
        
    
    
