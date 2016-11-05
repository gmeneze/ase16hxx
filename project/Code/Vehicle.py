class Vehicle(object):
    def __init__(self,v_id,capacity=0,speed=0,mileage=0,x=0,y=0):
        self.v_id = v_id
        self.route = []
        self.capacity = capacity
        self.speed = speed
        self.mileage = mileage
        self.x = x 
        self.y = y