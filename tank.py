import math
from bullet import Bullet

class RotateDirection(object):
    arrayDirections = [[(3,0), (2,0), (1,0), (4,0)],
                       [(0,2), (2,1), (5,0), (4,3)],
                       [(0,3), (3,1), (5,3), (1,3)],
                       [(0,0), (4,1), (5,2), (2,3)],
                       [(0,1), (1,1), (5,1), (3,3)],
                       [(1,2), (2,2), (3,2), (4,2)]]

    @staticmethod
    def getVec(direction):
        if(direction == 0):
            return ([1,0,0], 1)
        if(direction == 1):
            return ([0,1,0], -1)
        if(direction == 2):
            return ([1,0,0], -1)
        if(direction == 3):
            return ([0,1,0], 1)

    @staticmethod
    def getNewLocation(currMaze, direction, coords, cVis):
        tup = RotateDirection.arrayDirections[currMaze][direction]
        newMaze = tup[0]
        x, y = coords
        for i in range(tup[1]):
            (x, y) = (-y-1, x)
        if(y < 0):
            y = cVis + y
        if(x < 0):
            x = cVis + x
        if(tup[1] == 1):
            return newMaze, (x,y), 3
        if(tup[1] == 3):
            return newMaze, (x,y), 1

        return newMaze, (x,y), tup[1]

class Tank(object):
    def __init__(self, maze, cVis, currMaze, color):
        self.maze = maze
        self.color = color
        self.width, self.height = 1, 1
        self.cWidth, self.cHeight = self.width / cVis, self.height / cVis
        self.cX, self.cY = self.cWidth / 2, self.cHeight / 2
        self.lenY, self.lenX = 2*self.cWidth/6, self.cHeight/4
        self.currMaze = currMaze
        self.angle = 90
        self.angVec = [0,1]
        self.calculateCorners()
        # Exclusively for Player
        self.mousePosition, self.canLen = [0, 1], self.cWidth/3
        self.mazeFacing, self.dFace = 0, 0
        self.canAng = [0, 1]
        # Test
        self.health = 5
        self.score = 0
        self.isEnem = False

    def calculateCorners(self, ret = False):
        corners = [None]*4
        angVec = [self.angVec[0] * self.lenY, self.angVec[1] * self.lenY]
        perp = [-self.angVec[1] * self.lenX, self.angVec[0] * self.lenX]
        corners[0] = (self.cX - perp[0] + angVec[0], self.cY - perp[1] + angVec[1])
        corners[1] = (self.cX + perp[0] + angVec[0], self.cY + perp[1] + angVec[1])
        corners[2] = (self.cX + perp[0] - angVec[0], self.cY + perp[1] - angVec[1])
        corners[3] = (self.cX - perp[0] - angVec[0], self.cY - perp[1] - angVec[1])
        if(ret):
            return corners
        else:
            self.corners = corners

    def move(self, amount):
        self.cX+=self.angVec[0]*amount
        self.cY+=self.angVec[1]*amount
        if(not self.isLegal(self.calculateCorners(True))):
            self.cX-=self.angVec[0]*amount
            self.cY-=self.angVec[1]*amount
        self.calculateCorners()

    def isLegal(self, corners):
        lines = set()
        for i in range(len(corners)):
            currC, nextC = corners[i], corners[(i+1)%len(corners)]
            lines.add((currC, nextC))
        currI, currJ = self.getCurrCell()
        walls = set()
        rows, cols = len(self.maze), len(self.maze[0])
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if(currI + i < 0 or currI + i >= rows or
                   currJ + j < 0 or currJ + j >= cols):
                    continue
                else:
                    x = (currJ+j) * self.cWidth
                    y = (currI+i) * self.cHeight
                    if(self.maze[currI+i][currJ+j].direc[0]):
                        if(self.isEnem or (not self.isEnem and (currI+i!=0))):
                            walls.add(((x,y), (x + self.cWidth, y)))
                    if(self.maze[currI+i][currJ+j].direc[1]):
                        if(self.isEnem or (not self.isEnem and (currJ+j!=len(self.maze[0])-1))):
                            walls.add(((x+self.cWidth,y), (x+self.cWidth,y+self.cHeight)))
                    if(self.maze[currI+i][currJ+j].direc[2]):
                        if(self.isEnem or (not self.isEnem and (currI+i!=len(self.maze)-1))):
                            walls.add(((x,y+self.cHeight), (x + self.cWidth, y+self.cHeight)))
                    if(self.maze[currI+i][currJ+j].direc[3]):
                        if(self.isEnem or (not self.isEnem and (currJ+j!=0))):
                            walls.add(((x,y), (x, y+self.cHeight)))

        for wall in walls:
            for line in lines:
                if(self.doesIntersect(wall, line)):
                    return False
        return True

    def doesIntersect(self, wall, line):
        p1, q1 = line
        p2, q2 = wall
        return self.intersect(p1,q1,p2,q2)

    def intersect(self, A,B,C,D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)

    def ccw(self, A,B,C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    def getCurrCell(self):
        x, y = self.cX, self.cY
        row = int(y/self.cHeight)
        col = int(x/self.cWidth)
        return row, col

    def rotate(self, amount):
        self.angle -=amount
        ang = self.angle * math.pi/180
        self.angVec = [-math.cos(ang), math.sin(ang)]
        self.calculateCorners()

    def adjustCanAng(self, x, y):
        self.mousePosition = [x,y]

    def setCannonAngle(self, x, y):
        self.canAng = [x, y]

    def shootBullet(self):
        epX = self.cX + self.canLen*self.canAng[0]
        epY = self.cY + self.canLen*self.canAng[1]
        self.bulletCenter = [epX, epY]
        return Bullet([epX, epY], self.canAng[0], self.canAng[1], self.currMaze, self.maze)

    def hitEdge(self, maze):
        corners = self.corners
        lines = set()
        for i in range(len(corners)):
            currC, nextC = corners[i], corners[(i+1)%len(corners)]
            lines.add((currC, nextC))
        currI, currJ = self.getCurrCell()
        walls = []
        newLocation = []
        rows, cols = len(self.maze), len(self.maze[0])
        x = (currJ) * self.cWidth
        y = (currI) * self.cHeight
        #print(x, y)
        if(currI == 0):
            walls.append(((x,y+self.cHeight/12), (x + self.cWidth, y+self.cHeight/12), 0))
            newLocation.append((0, cols- currJ - 1))
        if(currJ == cols-1):
            walls.append(((x+11*self.cWidth/12,y), (x+11*self.cWidth/12,y+self.cHeight), 1))
            newLocation.append((0, rows - currI-1))
        if(currI == rows-1):
            walls.append(((x,y+11*self.cHeight/12), (x + self.cWidth, y+11*self.cHeight/12), 2))
            newLocation.append((0, currJ))
        if(currJ == 0):
            walls.append(((x+self.cWidth/12,y), (x+self.cWidth/12, y+self.cHeight), 3))
            newLocation.append((0, currI))

        for i, wall in enumerate(walls):
            for line in lines:
                if(self.doesIntersect(wall[:2], line)):
                    partOfScreen = (((self.mazeFacing + wall[-1]) % 4) + 2) % 4
                    m, coords, partOfNewMaze = RotateDirection.getNewLocation(self.currMaze, wall[-1], newLocation[i], len(self.maze))
                    mF = ((4-partOfNewMaze)+partOfScreen)%4
                    self.dFace = (self.mazeFacing-mF + self.dFace)%4
                    self.mazeFacing = mF

                    self.currMaze = m
                    self.cY, self.cX = (coords[0]*self.cHeight) + (self.cHeight/2), coords[1]*self.cWidth + (self.cWidth/2)
                    self.maze = maze[m]
                    self.calculateCorners()
                    #print(wall[-1], newLocation[i])
                    # Calculate rotation axis and direction
                    result = (partOfScreen + 2)%4
                    if(result == 1):
                        return RotateDirection.getVec(3)
                    if(result == 3):
                        return RotateDirection.getVec(1)
                    return RotateDirection.getVec(result)
        return None, None
