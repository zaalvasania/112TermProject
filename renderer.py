import math
import numpy as np
from PIL import Image, ImageTk

class Engine:
    def __init__(self, points, squares, width, height, maze, imagePath): 
        self.points = points
        self.squares = squares
        self.width, self.height = width, height
        self.viewer, self.scale = (0,  0, 10), 130
        self.maze = maze
        self.isPaused = False
        self.matrixRegister = np.identity(3)
        self.img = Image.open(imagePath)
        self.scaleX, self.scaleY = 0, 0
        self.trackTankCenter = False
        #self.visibleMaze = self.maze[0]

    def flattenPoints(self, point):
        x, y, z = point[0], point[1], point[2]
        constant = self.scale*abs(self.viewer[2] / (self.viewer[2] + z))
        screenX = int(self.width / 2 + (x*constant))
        screenY = int(self.height / 2 + (y*constant))
        return (screenX, screenY)

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
        self.trackTankCenter = (center[0],center[1])
        for i in range(4): tankChm[i] = self.flattenPoints(tankChm[i])
        for corner in corners:
            fp.append(self.flattenPoints(corner))

        #canvas.create_oval(fp[2][0]-2, fp[2][1]-2, fp[2][0]+2, fp[2][1]+2, fill = 'blue')
        canvas.create_polygon(fp[0][0], fp[0][1], fp[1][0], fp[1][1], fp[2][0], fp[2][1], fp[3][0], fp[3][1], fill = 'green')
        #canvas.create_oval(center[0] - 6, center[1] - 6, center[0] + 6, center[1] + 6, fill = 'black')
        canvas.create_polygon(tankChm[0][0], tankChm[0][1], tankChm[1][0], tankChm[1][1], tankChm[2][0], tankChm[2][1], tankChm[3][0], tankChm[3][1], fill = 'black')
        # Render cannon
        xDirec, yDirec = tank.canAng[0] - center[0], tank.canAng[1] - center[1]
        normal = (xDirec**2 + yDirec**2)**0.5
        if(normal!=0):
            xDirec/=normal
            yDirec/=normal
        epCanX, epCanY = tank.cX + (tank.canLen * xDirec), tank.cY + (tank.canLen * yDirec)
        endpoint = [tL[a] + (cWidth[a] * epCanX) + (cHeight[a] * epCanY) for a in range(3)]
        endpoint = self.flattenPoints(endpoint)
        canvas.create_line(center[0], center[1], endpoint[0], endpoint[1], width = 7)

   # def renderTank(self, canvas, tank):
   #     square = self.squares[tank.currMaze]
   #     tL = self.points[square[0]]
   #     cWidth = [(self.points[square[3]][i] - tL[i]) for i in range(3)]
   #     cHeight = [(self.points[square[1]][i] - tL[i]) for i in range(3)]
   #     tankCenter = [tL[a] + (cWidth[a] * tank.cX) + (cHeight[a] * tank.cY) for a in range(3)]
   #     screenX, screenY = self.flattenPoints(tankCenter)
   #     scaleX, scaleY = max(int(40*math.cos(self.scaleX)), 1), max(int(40*math.cos(self.scaleY)), 1)
   #     img = self.img.resize((scaleX, scaleY), Image.ANTIALIAS)
   #     canvas.create_image(screenX, screenY, image = ImageTk.PhotoImage(img))
   #     #pass

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

                if(i==0 and j==0):
                    canvas.create_line(coords[1][0], coords[1][1], coords[0][0], coords[0][1], width = 5)
                    canvas.create_line(coords[1][0], coords[1][1], coords[2][0], coords[2][1], width = 5)

                if(self.maze[faceNo][i][j].direc[0]):
                    canvas.create_line(coords[1][0], coords[1][1], coords[0][0], coords[0][1], width = 1)
                if(self.maze[faceNo][i][j].direc[3]):
                    canvas.create_line(coords[1][0], coords[1][1], coords[2][0], coords[2][1], width = 1)

            currtL = [currtL[a] + (cHeight[a]) for a in range(3)]

    def createSquares(self, points, textP, i, textP2, canvas):
        a, b, c, d = points[0], points[1], points[2], points[3]
        canvas.create_polygon(a[0], a[1], b[0], b[1], c[0], c[1], d[0], d[1], fill="white", outline ="gray")
        canvas.create_text(textP[0], textP[1], text= f"{i}")
        canvas.create_text(textP2[0], textP2[1], text = f"{i}")

    def render(self, canvas, tank):
        coord = []
        squares = []
        mazes = []

        for point in self.points:
            coord.append(self.flattenPoints(point))

        for i, square in enumerate(self.squares):
            avgZ = -((self.points[square[0]][2] + self.points[square[1]][2] + self.points[square[2]][2] + self.points[square[3]][2])/4)*10
            #squares.append((coord[square[0]], coord[square[1]], coord[square[2]], coord[square[3]], avgZ))
            squares.append((square, i, avgZ))
        
        #Sort Maze List
        squares.sort(key = lambda x: x[-1])
        #self.visibleMaze = squares[-1][:-1]
        #print(self.visibleMaze)

        for i, square in enumerate(squares):
            coordList = []
            for val in square[0]:
                coordList.append(coord[val])
            text3DPoint = self.getTextPoint(square[0], 1)
            text3DPoint2 = self.getTextPoint(square[0], 2)
            self.createSquares(coordList,text3DPoint, square[1], text3DPoint2, canvas)
            self.createMaze(square[0], square[1], canvas)
            if(square[1] == tank.currMaze):
                self.renderTank(canvas, tank)
            #self.createTriangles(square[:-1], i, canvas)
   
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

    def rotateAboutAxisCalcAngle(self,rotation):
        ang = 0
        trackCenter= abs(self.trackTankCenter[0]) < abs(self.trackTankCenter[1])
        if(trackCenter):
            ang = -5*1.9378
        else:
            ang = 5*1.9378
        for i in range(len(rotation)):
            rotation[i] = int(rotation[i])
        print(rotation)
        print(self.trackTankCenter)
        self.rotateAboutAxis(rotation, ang)

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


    def unRot(self):
        mat = np.linalg.inv(self.matrixRegister)
        axisVec = [mat[2,1] - mat[1,2], mat[0,2] - mat[2,0], mat[1,0] - mat[0,1]]
        vecMag = (axisVec[0]**2 + axisVec[1]**2+axisVec[2]**2)**0.5
        angle = math.asin(vecMag/2) 
        return (angle, axisVec)

    def unRotate(self):
        self.matrixRegister = np.linalg.inv(self.matrixRegister)
        for i,point in enumerate(self.points):
            pointList = [[point[0]], [point[1]], [point[2]]]
            result = np.dot(self.matrixRegister, pointList)
            self.points[i] = (result[0,0], result[1,0], result[2,0])
        self.scaleX, self.scaleY = 0, 0
        self.matrixRegister = np.identity(3)

