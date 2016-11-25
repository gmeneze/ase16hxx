class Node(object):
    def __init__(self, id, x, y, duration=0, latestReach=0, satisfaction=0, earliestReach=0, quantity=0):
        self.id = id
        self.xcordinate = x
        self.ycordinate = y
        self.quantity = quantity
        self.satisfaction = satisfaction
        self.earliestReach = earliestReach
        self.latestReach = latestReach
        self.duration = duration
        