class Node(object):
    def __init__(self, id, x, y, quantity=0, demand=0, earliestReach=0, latestReach=0, duration=0):
        self.id = id
        self.xcordinate = x
        self.ycordinate = y
        self.quantity = quantity
        self.demand = demand
        self.earliestReach = earliestReach
        self.latestReach = latestReach
        self.duration = duration
        