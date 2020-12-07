##### CELLTEMPLATE.py #####
# This file contains the cell datastructure

class Cell:
    def __init__(self, i, j):
        self.i, self.j = i, j
        self.visited = False
        # N - 0, E - 1, S - 2, W - 3
        self.direc = [True]*4
