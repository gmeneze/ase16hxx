class Objective(object):
    def __init__(self, name, value = None , do_minimize = True):
        self.name = name
        self.do_minimize = do_minimize
        self.value = value