class Bullet(object):
    def __init__(self, center, dX, dY, currMaze, maze):
        self.center = center
        self.collideCount = 0
        self.currMaze = currMaze
        self.maze = maze
        self.cWidth, self.cHeight = 1/len(self.maze[0]), 1/len(self.maze)
        self.dx = dX*self.cWidth*0.1
        self.dy = dY*self.cHeight*0.1
        self.bulletSize = self.cWidth/12
        self.calculateCorners()

    def calculateCorners(self, ret = False):
        corners = [None]*4
        corners[0] = (self.center[0] - self.bulletSize, self.center[1] - self.bulletSize)
        corners[1] = (self.center[0] + self.bulletSize, self.center[1] - self.bulletSize)
        corners[2] = (self.center[0] + self.bulletSize, self.center[1] + self.bulletSize)
        corners[3] = (self.center[0] - self.bulletSize, self.center[1] + self.bulletSize)
        if(ret):
            return corners
        self.corners = corners

    def move(self):
        self.center[0]+=self.dx
        self.center[1]+=self.dy
        # Collision Detection
        direc = self.isLegal(self.calculateCorners(True))
        if(direc!=None):
            if(direc % 2 == 0):
                self.dy = -self.dy
                self.center[1]+=self.dy*1.5
                self.collideCount += 1
            elif(direc % 2 == 1):
                self.dx = -self.dx
                self.center[0]+=self.dx*1.5
                self.collideCount += 1
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
                        walls.add(((x,y), (x + self.cWidth, y), 0))
                    if(self.maze[currI+i][currJ+j].direc[1]):
                        walls.add(((x+self.cWidth,y), (x+self.cWidth,y+self.cHeight), 1))
                    if(self.maze[currI+i][currJ+j].direc[2]):
                        walls.add(((x,y+self.cHeight), (x + self.cWidth, y+self.cHeight), 2))
                    if(self.maze[currI+i][currJ+j].direc[3]):
                        walls.add(((x,y), (x, y+self.cHeight), 3))

        for wall in walls:
            for line in lines:
                if(self.doesIntersect(wall[:-1], line)):
                    return wall[-1]
        return None

    # Line-Line intersection algorithm based wholly upon algorithm at https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
    def doesIntersect(self, wall, line):
        p1, q1 = line
        p2, q2 = wall
        return self.intersect(p1,q1,p2,q2)

    def intersect(self, A,B,C,D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)

    def ccw(self, A,B,C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    def getCurrCell(self):
        x, y = self.center[0], self.center[1]
        row = int(y/self.cHeight)
        col = int(x/self.cWidth)
        return row, col

    def collides(self, enemy):
        distance = ((self.center[0] - enemy.cX)**2 + (self.center[1] - enemy.cY)**2)**0.5
        if(distance <= (enemy.lenX + enemy.lenY)/2):
            return True
        return False

    def collidesWithCenter(self, enemyC, minDist):
        distance = ((self.center[0] - enemyC[0])**2 + (self.center[1] -enemyC[1])**2)**0.5
        if(distance <= minDist):
            return True
        return False

