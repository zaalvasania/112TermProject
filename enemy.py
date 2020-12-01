import random, math
from tank import Tank
class Enemy(Tank):
    def __init__(self, maze, cVis, currMaze, color):
        super().__init__(maze, cVis, currMaze, color)
        self.setCenter(self.width / 2, self.height / 2 - self.cHeight)
        self.movement = [0.01, -0.01]
        self.rotation = [5, -5]
        self.currMovement = [0, 0]
        self.hBLen = 12*self.lenX/25
        self.hBHeight = self.lenY/4
        self.isEnem = True
        self.updateHealthBar()
        self.mazeSolve = None
        self.closest = [1000, None]

    def updateHealthBar(self):
        self.hBtL = (self.cX - 6*self.lenX/5, self.cY - 8*self.lenY/5)

    def enemyMovement(self, player, currMaze):
        if(self.currMaze == currMaze):
            if(self.mazeSolve == None or random.random()<0.3):
                self.mazeSolve = self.solveMaze(self.getCurrCell(), player)
            result = self.calculateMovement()
            if(result != None):
                self.currMovement[0] = result
            #self.rotate(self.calculateRotate())
        elif(random.random() < 0.3):
            self.currMovement = [random.choice(self.movement), random.choice(self.rotation)]
        
        #if(0 not in self.currMovement):
        self.move(self.currMovement[0])
        #self.rotate(self.currMovement[1])
        self.updateHealthBar()

    
    def calculateMovement(self):
        if(self.mazeSolve == None or (len(self.mazeSolve) <=1)):
            return random.choice(self.movement)
        else:
            #print(self.mazeSolve[1])
            i, j = self.mazeSolve[1]
            destX, destY = j*self.cWidth + self.cWidth/2, i*self.cHeight + self.cHeight/2
            if(((self.cX - destX)**2 + (self.cY - destY)**2)**0.5 < self.cWidth / 4):
                self.mazeSolve.pop(0)
                return
            newAngVec = [destX - self.cX, (destY - self.cY)]
            normFac = (newAngVec[0]**2 + newAngVec[1]**2)**0.5
            newAngVec = [newAngVec[0] / normFac, (newAngVec[1] / normFac)]
            # Angle subtraction algo inspired by https://gamedev.stackexchange.com/questions/7131/how-can-i-calculate-the-angle-and-proper-turn-direction-between-two-2d-vectors
            ang1 = math.atan2(newAngVec[1], newAngVec[0])
            ang2 = math.atan2(self.angVec[1], self.angVec[0])
            angle = (ang1 - ang2) * (180 / math.pi)
            self.rotate(angle)

    
    def solveMaze(self, currCell, destination):
        solution = []
        depth = 0
        dest = destination
        def solve(currCell, depth):
            if(currCell in solution):
                #print(currCell)
                return False
            solution.append(currCell)
            if(currCell == dest): return True
        #    dist = ((currCell[0] - dest[0])**2 + (currCell[1] - dest[1])**2)**0.5
        #    if(dist < self.closest[0]):
        #        self.closest[0] = dist
        #        self.closest[1] = solution
            for drow, dcol in [(1,0), (0,1), (-1,0), (0,-1)]:
                if(self.isValid(currCell, (drow,dcol))):
                    p = solve((currCell[0] + drow, currCell[1] + dcol), depth+1)
                    if(p): return True
            solution.remove(currCell)
            return False
        if(solve(currCell, 0)):
            return solution

    def isValid(self,currCell, dMove):
        if(currCell[0] + dMove[0] < 0 or currCell[0] + dMove[0] >= len(self.maze) or
           currCell[1] + dMove[1] < 0 or currCell[1] + dMove[1] >= len(self.maze[0])):
            return False
        dire = abs(dMove[0])*(dMove[0]+1) + (dMove[1]%4)
        if(self.maze[currCell[0]][currCell[1]].direc[dire]):
            return False
        return True

    def rotate(self, amount):
        temp = self.angVec
        self.angle -= amount
        ang = self.angle * math.pi/180
        self.angVec = [-math.cos(ang), math.sin(ang)]
        if(not self.isLegal(self.calculateCorners(True))):
            self.angle += amount
            self.angVec = temp
        self.calculateCorners()

    def setCenter(self, cX, cY):
        self.cX = cX
        self.cY = cY
        self.calculateCorners()
