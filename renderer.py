import math
import numpy as np
from tank import Tank

class Engine:
    def __init__(self, points, squares, width, height, maze):
        self.points = points
        self.squares = squares
        self.width, self.height = width, height
        self.viewer, self.scale = (0,  0, 10), 130
        self.maze = maze
        self.isPaused = False
        self.matrixRegister = np.identity(3)
        self.scaleX, self.scaleY = 0, 0
        self.currMazeTop = 0

    # Flatten Points based largely on description and code from http://www.quantimegroup.com/solutions/pages/Article/Article.html 
    def flattenPoints(self, point):
        x, y, z = point[0], point[1], point[2]
        constant = self.scale*abs(self.viewer[2] / (self.viewer[2] + z))
        screenX = int(self.width / 2 + (x*constant))
        screenY = int(self.height / 2 + (y*constant))
        return (screenX, screenY)

    def renderCoin(self, canvas, coin):
        square = self.squares[coin.currMaze]
        tL = self.points[square[0]]
        cWidth = [(self.points[square[3]][i] - tL[i]) for i in range(3)]
        cHeight = [(self.points[square[1]][i] - tL[i]) for i in range(3)]
        corners = []
        for x, y in coin.corners:
            corners.append([tL[a] + (cWidth[a] * x) + (cHeight[a] * y) for a in range(3)])
        for i in range(4): corners[i] = self.flattenPoints(corners[i])
        canvas.create_polygon(corners[0][0], corners[0][1], corners[1][0], corners[1][1], corners[2][0], corners[2][1], corners[3][0], corners[3][1], fill = 'yellow', outline = 'black')


    def renderTank(self, canvas, tank):
        square = self.squares[tank.currMaze]
        tL = self.points[square[0]]
        cWidth = [(self.points[square[3]][i] - tL[i]) for i in range(3)]
        cHeight = [(self.points[square[1]][i] - tL[i]) for i in range(3)]
        corners = []
        for x, y in tank.corners:
            corners.append([tL[a] + (cWidth[a] * x) + (cHeight[a] * y) for a in range(3)])
        fp = []
        tankChm = [None]*4

        # Center and bounding box of tank chamber
        center = [tL[a] + (cWidth[a] * tank.cX) + (cHeight[a] * tank.cY) for a in range(3)]
        tankChm[0] = [tL[a] + cWidth[a] * (tank.cX) + cHeight[a] * (tank.cY - 2*tank.lenY/3) for a in range(3)]
        tankChm[1] = [tL[a] + cWidth[a] * (tank.cX + 2*tank.lenY/3) + cHeight[a] * (tank.cY) for a in range(3)]
        tankChm[2] = [tL[a] + cWidth[a] * (tank.cX) + cHeight[a] * (tank.cY + 2*tank.lenY/3) for a in range(3)]
        tankChm[3] = [tL[a] + cWidth[a] * (tank.cX - 2*tank.lenY/3) + cHeight[a] * (tank.cY) for a in range(3)]

        # Flatten Points
        center = self.flattenPoints(center)
        for i in range(4): tankChm[i] = self.flattenPoints(tankChm[i])
        for corner in corners:
            fp.append(self.flattenPoints(corner))

        # Render Tank and Chamber
        canvas.create_polygon(fp[0][0], fp[0][1], fp[1][0], fp[1][1], fp[2][0], fp[2][1], fp[3][0], fp[3][1], fill = tank.color)
        canvas.create_polygon(tankChm[0][0], tankChm[0][1], tankChm[1][0], tankChm[1][1], tankChm[2][0], tankChm[2][1], tankChm[3][0], tankChm[3][1], fill = 'black')
        canvas.create_line(fp[2][0], fp[2][1], fp[3][0], fp[3][1], width = 5)

        # Render cannon and health bar
        if(type(tank) == Tank):
            self.renderPlayerCannon(tank, center, tL, cWidth, cHeight, canvas)
        else:
            xEp, yEp = (tank.angVec[0] * tank.canLen) + tank.cX, (tank.angVec[1] * tank.canLen) + tank.cY
            endpoint = [tL[a] + (cWidth[a] * xEp) + (cHeight[a] * yEp) for a in range(3)]
            endpoint = self.flattenPoints(endpoint)
            canvas.create_line(center[0], center[1], endpoint[0], endpoint[1], width = 7)

            self.makeHealthBar(tank, center, tL, cWidth, cHeight, canvas)

    def makeHealthBar(self, tank, enter, tL, cWidth, cHeight, canvas):
        hb = [None]*4
        lenBar = tank.hBLen*tank.health
        hb[0] = [tL[a] + cWidth[a] * (tank.hBtL[0]) + cHeight[a] * (tank.hBtL[1]) for a in range(3)]
        hb[1] = [tL[a] + cWidth[a] * (tank.hBtL[0] + lenBar) + cHeight[a] * (tank.hBtL[1]) for a in range(3)]
        hb[2] = [tL[a] + cWidth[a] * (tank.hBtL[0] + lenBar) + cHeight[a] * (tank.hBtL[1] + tank.hBHeight) for a in range(3)]
        hb[3] = [tL[a] + cWidth[a] * (tank.hBtL[0]) + cHeight[a] * (tank.hBtL[1] + tank.hBHeight)for a in range(3)]

        for i in range(4): hb[i] = self.flattenPoints(hb[i])
        canvas.create_polygon(hb[0][0], hb[0][1], hb[1][0], hb[1][1], hb[2][0], hb[2][1], hb[3][0], hb[3][1], width = 3, fill = 'red')

    def renderPlayerCannon(self, tank, center, tL, cWidth, cHeight, canvas):
        xDirec, yDirec = (tank.mousePosition[0] - center[0]), (tank.mousePosition[1] - center[1])
        for i in range(tank.dFace):
            (xDirec, yDirec) = (-yDirec, xDirec)
        normal = (xDirec**2 + yDirec**2)**0.5
        if(normal!=0):
            xDirec/=normal
            yDirec/=normal
        tank.setCannonAngle(xDirec, yDirec)
        epCanX, epCanY = tank.cX + (tank.canLen * xDirec), tank.cY + (tank.canLen * yDirec)
        endpoint = [tL[a] + (cWidth[a] * epCanX) + (cHeight[a] * epCanY) for a in range(3)]
        endpoint = self.flattenPoints(endpoint)
        canvas.create_line(center[0], center[1], endpoint[0], endpoint[1], width = 7)

    def renderBullet(self, canvas, bullet):
        square = self.squares[bullet.currMaze]
        tL = self.points[square[0]]
        cWidth = [(self.points[square[3]][i] - tL[i]) for i in range(3)]
        cHeight = [(self.points[square[1]][i] - tL[i]) for i in range(3)]
        corners = [None]*len(bullet.corners)
        for i in range(len(bullet.corners)):
            corners[i] = self.flattenPoints([tL[a] + (cWidth[a] * bullet.corners[i][0]) + (cHeight[a] * bullet.corners[i][1]) for a in range(3)])

        canvas.create_polygon(corners[0][0], corners[0][1], corners[1][0], corners[1][1], corners[2][0], corners[2][1], corners[3][0], corners[3][1], fill = 'blue')


    def createMaze(self, square, faceNo, canvas):
        # First index in square is tL index corner: square = (a,b,c,d)
        tL = self.points[square[0]]
        cWidth = [(self.points[square[3]][i] - tL[i]) / len(self.maze[faceNo]) for i in range(3)]
        cHeight = [(self.points[square[1]][i] - tL[i]) / len(self.maze[faceNo]) for i in range(3)]
        #print((cWidth[0]**2 + cWidth[1]**2 + cWidth[2]**2)**0.5)
        currtL = tL
        for i in range(len(self.maze[faceNo])):
            for j in range(len(self.maze[faceNo][i])):
                gridtL = [currtL[a] + (cWidth[a] * j) for a in range(3)]
                pt = [None]*3
                pt[0] = [gridtL[a] + (cWidth[a]) for a in range(3)]
                pt[1] = gridtL
                pt[2] = [gridtL[a] + (cHeight[a]) for a in range(3)]

                coords = []
                for val in pt:
                    coords.append(self.flattenPoints(val))

    #            if(i==0 and j==0):
    #                canvas.create_line(coords[1][0], coords[1][1], coords[0][0], coords[0][1], width = 5)
    #                canvas.create_line(coords[1][0], coords[1][1], coords[2][0], coords[2][1], width = 5)

                if(self.maze[faceNo][i][j].direc[0]):
                    canvas.create_line(coords[1][0], coords[1][1], coords[0][0], coords[0][1], width = 3)
                if(self.maze[faceNo][i][j].direc[3]):
                    canvas.create_line(coords[1][0], coords[1][1], coords[2][0], coords[2][1], width = 3)

            currtL = [currtL[a] + (cHeight[a]) for a in range(3)]

    def createSquares(self, points, i, canvas,textP = None, textP2 = None,):
        a, b, c, d = points[0], points[1], points[2], points[3]
        canvas.create_polygon(a[0], a[1], b[0], b[1], c[0], c[1], d[0], d[1], fill="white", outline ="gray")
        #canvas.create_text(textP[0], textP[1], text= f"{i}")
        #canvas.create_text(textP2[0], textP2[1], text = f"{i}")

    # Face sorting by avgZ and rendering face by face inspired by code and algorithmic design fromhttps://medium.com/quick-code/3d-graphics-with-the-python-standard-library-af3794d0cba
    def render(self, canvas, tank, bullets, enemies, coins):
        coord = []
        squares = []
        mazes = []

        for point in self.points:
            coord.append(self.flattenPoints(point))

        for i, square in enumerate(self.squares):
            avgZ = -((self.points[square[0]][2] + self.points[square[1]][2] + self.points[square[2]][2] + self.points[square[3]][2])/4)*10
            squares.append((square, i, avgZ))
        
        #Sort Maze List
        squares.sort(key = lambda x: x[-1])

        for i, square in enumerate(squares):
            coordList = []
            for val in square[0]:
                coordList.append(coord[val])
            self.createSquares(coordList, square[1], canvas)
            self.createMaze(square[0], square[1], canvas)
            if(tank!= None and square[1] == tank.currMaze):
                self.renderTank(canvas, tank)
            self.renderBullets(canvas, bullets, square[1])
            self.renderEnemies(canvas, enemies, square[1])
            self.renderCoins(canvas, coins, square[1])

            #self.createTriangles(square[:-1], i, canvas)

    def renderCoins(self, canvas, coins, currMaze):
        if(coins == []): return
        for coin in coins:
            if(currMaze == coin.currMaze):
                self.renderCoin(canvas, coin)

    def renderEnemies(self, canvas, enemies, currMaze):
        if(enemies == []): return
        for enemy in enemies:
            if(currMaze == enemy.currMaze):
                self.renderTank(canvas, enemy)

    def renderBullets(self, canvas, bullets, currMaze):
        if(bullets == []): return
        for bullet in bullets:
            if(currMaze == bullet.currMaze):
                self.renderBullet(canvas, bullet)

    # Debugging
    def getTextPoint(self, square, idx):
        p1, p2 = self.points[square[0]], self.points[square[idx]]
        mP = ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2, (p1[2] + p2[2])/2)
        return self.flattenPoints(mP)

    def rotateAboutAxis(self, axisVec, angle):
        angle = (angle / 360) * (180 / math.pi)
        vecMag = (axisVec[0]**2 + axisVec[1]**2+axisVec[2]**2)**0.5
        for j in range(len(axisVec)):
            axisVec[j] /= vecMag
        matrix = np.array(self.createMatrix(angle, vecMag, axisVec))
        for i, point in enumerate(self.points):
            pointList = [[point[0]],[point[1]],[point[2]]]
            result = np.dot(matrix, pointList)
            self.points[i] = (result[0,0], result[1,0], result[2,0])

        if(self.isPaused):
            self.matrixRegister = np.dot(matrix, self.matrixRegister)

    def rotateAboutAxisCalcAngle(self,rotation, direc):
        ang = 5*1.9378*direc
        self.rotateAboutAxis(rotation, ang)

    # Rotation Matrix around arbitrary axis sourced from https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
    def createMatrix(self, angle, vecMag, axisVec):
        cos_T, sin_T = math.cos(angle), math.sin(angle)
        newX, newY, newZ = [], [], []
        newX.append((cos_T + (axisVec[0]**2)*(1-cos_T)))
        newX.append((axisVec[0] * axisVec[1] * (1-cos_T) - axisVec[2] * (sin_T)))
        newX.append((axisVec[0] * axisVec[2] * (1-cos_T) + axisVec[1] * (sin_T)))

        newY.append((axisVec[1] * axisVec[2] * (1-cos_T) + axisVec[2] * (sin_T)))
        newY.append((cos_T + (axisVec[1]**2)*(1-cos_T)))
        newY.append((axisVec[1] * axisVec[2] * (1-cos_T) - axisVec[0] * (sin_T)))

        newZ.append((axisVec[2] * axisVec[0] * (1-cos_T) - axisVec[1] * (sin_T)))
        newZ.append((axisVec[2] * axisVec[1] * (1-cos_T) + axisVec[0] * (sin_T)))
        newZ.append((cos_T + (axisVec[2]**2)*(1-cos_T)))
        return [newX, newY, newZ]

    def getCoords(self, tank):
        square = self.squares[tank.currMaze]
        tL = self.points[square[0]]
        cWidth = [(self.points[square[3]][i] - tL[i]) for i in range(3)]
        cHeight = [(self.points[square[1]][i] - tL[i]) for i in range(3)]

        # Center and bounding box of tank chamber
        center = [tL[a] + (cWidth[a] * tank.cX) + (cHeight[a] * tank.cY) for a in range(3)]
        return self.flattenPoints(center)


    #def unRot(self):
    #    mat = np.linalg.inv(self.matrixRegister)
    #    axisVec = [mat[2,1] - mat[1,2], mat[0,2] - mat[2,0], mat[1,0] - mat[0,1]]
    #    vecMag = (axisVec[0]**2 + axisVec[1]**2+axisVec[2]**2)**0.5
    #    angle = math.asin(vecMag/2) 
    #    return (angle, axisVec)

    def unRotate(self):
        self.matrixRegister = np.linalg.inv(self.matrixRegister)
        for i,point in enumerate(self.points):
            pointList = [[point[0]], [point[1]], [point[2]]]
            result = np.dot(self.matrixRegister, pointList)
            self.points[i] = (result[0,0], result[1,0], result[2,0])
        self.scaleX, self.scaleY = 0, 0
        self.matrixRegister = np.identity(3)

