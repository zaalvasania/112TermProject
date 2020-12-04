import random, math
from tank import Tank
from bullet import Bullet
class Enemy(Tank):
    def __init__(self, maze, cVis, currMaze, color, moveParam):
        super().__init__(maze, cVis, currMaze, color)
        self.setCenter(self.width / 2, self.height / 2 - self.cHeight)
        self.movement = [0.01, -0.01]
        self.rotation = [4, -4]
        self.currMovement = [0, 0]
        self.hBLen = 12*self.lenX/25
        self.hBHeight = self.lenY/4
        self.isEnem = True
        self.updateHealthBar()
        self.mazeSolve = None
        self.closest = [1000, None]
        self.health = 5
        self.moveParam = moveParam

    def updateHealthBar(self):
        self.hBtL = (self.cX - 6*self.lenX/5, self.cY - 8*self.lenY/5)

    def enemyMovement(self, player, currMaze, enemDiff, playerCent):
        if(enemDiff == 0):
            self.currMovement = self.easyMode()
        elif(enemDiff == 1):
            self.currMovement = self.mediumMode(player, currMaze)
        else:
            self.currMovement = self.hardMode(player, currMaze)
        
        res = None
        if(self.currMaze == currMaze):
            res = self.shootBullet(player,playerCent)
            if(res != None):
                self.currMovement = [0, 0]
                return res
       
        if(res == None):
            self.rotate(self.currMovement[1])
            self.move(self.currMovement[0])
            self.updateHealthBar()

    def shootBullet(self, player, playPos):
        for dAngle in [0.5*x for x in range(-10, 10, 1)]:
            angle = self.angle - dAngle
            ang = angle * math.pi/180
            angVec = [-math.cos(ang), math.sin(ang)]
            epX = self.cX + self.canLen*angVec[0]
            epY = self.cY + self.canLen*angVec[1]
            bul = Bullet([epX, epY], angVec[0], angVec[1], self.currMaze, self.maze)
            count = 0
            while(bul.collideCount < 3 and count < 10**3):
                count += 1
                bul.move()
                if(bul.collides(self)): break
                if(player == bul.getCurrCell()):
                    if(bul.collidesWithCenter(playPos, (self.lenY+self.lenX)/2)):
                        return Bullet([epX, epY], angVec[0], angVec[1], self.currMaze, self.maze)
            return None

    def easyMode(self):
        if(random.random() < 0.3):
            return [random.choice(self.movement), random.choice(self.rotation)]
        else:
            return self.currMovement

    def mediumMode(self, player, currMaze):
        if(random.random() < 0.3):
            return self.hardMode(player, currMaze)
        else:
            return self.easyMode()

    def hardMode(self, player, currMaze):
        currMovement = []
        if(self.currMaze == currMaze):
            if(self.mazeSolve == None):
                self.resolveMaze(player)
            result = self.calculateMovement()
            if(result != None):
                currMovement = result
                res = self.move(currMovement[0])
                self.move(-currMovement[0])
                if(not res):
                    currMovement = [random.choice([0.02, -0.02]), random.choice([6, -6])]
            else:
                return self.easyMode()
        else:
            self.mazeSolve = None
            return self.easyMode()

        return currMovement

    def resolveMaze(self, player):
        self.mazeSolve = self.solveMaze(self.getCurrCell(), player)
    
    def calculateMovement(self):
        if(self.mazeSolve == None or (len(self.mazeSolve) <=1)):
            if(random.random() < 0.3):
                return [random.choice(self.movement), random.choice(self.rotation)]
        else:
            i, j = self.mazeSolve[1]
            destX, destY = j*self.cWidth + self.cWidth/2, i*self.cHeight + self.cHeight/2
            if(((self.cX - destX)**2 + (self.cY - destY)**2)**0.5 < self.lenX / 2):
                self.mazeSolve.pop(0)
                return
            newAngVec = [destX - self.cX, (destY - self.cY)]
            ang1 = math.atan2(newAngVec[1], newAngVec[0])
            ang2 = math.atan2(self.angVec[1], self.angVec[0])
            angle = (ang1 - ang2) * (180 / math.pi)
            return (self.moveParam, angle)
   
    # Algorithm based wholly on the Algorithm at https://www.cs.cmu.edu/~112/notes/maze-solver.py
    def solveMaze(self, currCell, destination):
        solution = []
        depth = 0
        dest = destination
        def solve(currCell, depth):
            if(currCell in solution):
                return False
            solution.append(currCell)
            if(currCell == dest): return True
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
        #temp = self.angVec
        self.angle -= amount
        ang = self.angle * math.pi/180
        self.angVec = [-math.cos(ang), math.sin(ang)]
        #if(not self.isLegal(self.calculateCorners(True))):
        #    self.angle += amount
        #    self.angVec = temp
        self.calculateCorners()

    def setCenter(self, cX, cY):
        self.cX = cX
        self.cY = cY
        self.calculateCorners()
