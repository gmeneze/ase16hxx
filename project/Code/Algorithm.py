class Algorithm(object):
    def __init__(self, id, name, iterations = 0, currentSolution = [], bestSolution = [], bestFitness = 0, description = ""):
        self.id = id
        self.name = name
        self.iterations = iterations
        self.currentSolution = currentSolution
        self.bestSolution = bestSolution
        self.bestFitness = bestFitness
        self.description = description
        
        