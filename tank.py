import math
class Tank(object):
    def __init__(self, maze, cVis, currMaze):
        self.maze = maze
        self.width, self.height = 1, 1
        self.cWidth, self.cHeight = self.width / cVis, self.height / cVis
        self.cX, self.cY = self.cWidth / 2, self.cHeight / 2
        self.lenX, self.lenY = 2*self.cWidth/6, self.cHeight/4
        self.currMaze = currMaze
        self.angle = 90
        self.angVec = [0,1]
        self.calculateCorners()
        self.canAng, self.canLen = [0, 1], self.cWidth/3

    def calculateCorners(self, ret = False):
        corners = [None]*4
        angVec = [self.angVec[0] * self.lenX, self.angVec[1] * self.lenX]
        perp = [-self.angVec[1] * self.lenY, self.angVec[0] * self.lenY]
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
                        walls.add(((x,y), (x + self.cWidth, y)))
                    if(self.maze[currI+i][currJ+j].direc[1]):
                        walls.add(((x+self.cWidth,y), (x+self.cWidth,y+self.cHeight)))
                    if(self.maze[currI+i][currJ+j].direc[2]):
                        walls.add(((x,y+self.cHeight), (x + self.cWidth, y+self.cHeight)))
                    if(self.maze[currI+i][currJ+j].direc[3]):
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
        self.canAng = [x,y]

   # def adjustCanAng(self, x, y):
   #     xDirec, yDirec= x - self.cX, y - self.cY
   #     normal = (xDirec**2 + yDirec**2)**0.5
   #     if(normal!=0):
   #         self.canAng[0] = xDirec/normal
   #         self.canAng[1] = yDirec/normal
