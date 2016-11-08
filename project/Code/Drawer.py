from Graphics import *
import time
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
            point1_txt = Point(self.nodelist[route[i]].xcordinate-15, self.nodelist[route[i]].ycordinate+15)
            point2_txt = Point(self.nodelist[route[i + 1]].xcordinate-15, self.nodelist[route[i + 1]].ycordinate+15)
            msg1 = Text(point1_txt,self.route[i])
            msg1.draw(win)
            msg2 = Text(point2_txt, self.route[i+1])
            msg2.draw(win)
        time.sleep(3)
        message = Text(Point(150,10), self.route)
        message.draw(win)
        time.sleep(3)
        for i in range(route.__len__()-1):
            point1 = Point(self.nodelist[route[i]].xcordinate,self.nodelist[route[i]].ycordinate)
            point2 = Point(self.nodelist[route[i+1]].xcordinate,self.nodelist[route[i+1]].ycordinate)
            line1 = Line(point1,point2)
            line1.setWidth(3)
            line1.draw(win)
            time.sleep(2)
        win.getMouse()
        win.close()
        
        
    
    
