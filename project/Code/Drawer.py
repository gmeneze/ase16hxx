from graphics import *
class Drawer(object):
    def __init__(self):
        self.window_height = 1400
        self.window_length = 1400
        #self.nodelist = nodelist
        #self.route = route
        
    def draw_path(self, nodelist, route):
        self.nodelist = nodelist
        self.route = route
        win = GraphWin('TSP', self.window_length, self.window_height)
        for i in range(route.__len__()-1):
            point1 = Point(self.nodelist[route[i]].xcordinate,self.nodelist[route[i]].ycordinate)
            point2 = Point(self.nodelist[route[i+1]].xcordinate,self.nodelist[route[i+1]].ycordinate)
            line1 = Line(point1, point2) 
            line1.setWidth(3)
            line1.draw(win)
        win.getMouse()
        win.close()
        
        
    
    