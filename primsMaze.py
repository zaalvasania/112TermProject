import random 
from cellTemplate import Cell

# Algorithm created independently based on description at http://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm

class Maze:
    def __init__(self, visCells):
        self.cVis = visCells
        # Cube template
        #self.cList = [[None]*self.cVis for _ in range(self.cVis)]
        self.createCube()
        self.initialiseCellList(False)
        self.createFrontierList()
        self.isOver, self.currFront = None, None

    def createCube(self):
        self.cList = [[None]*self.cVis for _ in range(3*self.cVis)]
        for i in range(self.cVis, 2*self.cVis):
            self.cList[i].extend([None]*3*self.cVis)

    def initialiseCellList(self, switch):
        for i in range(len(self.cList)):
            for j in range(len(self.cList[i])):
                if(not switch):
                    self.cList[i][j] = Cell(i, j)
                if(i==0 or len(self.cList[i-1])!=len(self.cList[i])):
                    self.cList[i][j].direc[0] = switch
                if(j==0):
                    self.cList[i][j].direc[3] = switch
                if(i == len(self.cList)-1 or len(self.cList[i+1])!=len(self.cList[i])):
                    self.cList[i][j].direc[2] = switch
                if(j == len(self.cList[i]) - 1):
                    self.cList[i][j].direc[1] = switch

    def createFrontierList(self):
        i= random.randint(0, len(self.cList)-1)
        j = random.randint(0, len(self.cList[i])-1)
        self.cList[i][j].visited = True
        self.frontList = self.getFrontier(i, j)

    def generateStep(self):
        if(len(self.frontList) > 0):
            currFront = random.choice(self.frontList)
            self.currFront = currFront
            self.carvePath(currFront)
            while(currFront in self.frontList):
                self.frontList.remove(currFront)
            self.frontList.extend(self.getFrontier(currFront.i, currFront.j))
            return False
        else:
            self.currFront = self.cList[0][0]
            self.isOver = True
            self.initialiseCellList(True)
            return True

    def getFrontier(self, i, j):
        frontList = []
        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if(bool(a) ^ bool(b)):
                    newI, newJ = i + a, j + b
                    if(newI < 0 or newI >= len(self.cList) or
                       newJ < 0 or newJ >= len(self.cList[newI])):
                        continue
                    elif(not self.cList[newI][newJ].visited):
                        frontList.append(self.cList[newI][newJ])
        return frontList

    def carvePath(self, currFront):
        currFront.visited = True
        adj, orient = self.partOfMaze(currFront)
        currFront.direc[orient] = False
        adj.direc[(2 + orient) % 4] = False

    def partOfMaze(self, currFront):
        visited = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if(bool(i) ^ bool(j)):
                    newI, newJ = i + currFront.i, j + currFront.j
                    if(newI < 0 or newI >= len(self.cList) or
                       newJ < 0 or newJ >= len(self.cList[newI])):
                        continue
                    elif(self.cList[newI][newJ].visited):
                        visited.append((self.cList[newI][newJ], i, j))

        randCell, i, j = random.choice(visited)
        direc = abs(i)*(i+1) + (j % 4)
        return (randCell, direc)
