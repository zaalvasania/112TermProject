import math
import numpy as np

class Engine:
    def __init__(self, points, triangles, width, height, maze): 
        self.points = points
        self.triangles = triangles
        self.width = width
        self.height = height
        self.viewer = (0,  0, 10)
        self.scale = 100
        self.maze = maze
        self.mazeOrder = list(range(6))
        self.isPaused = False
        self.matrixRegister = np.identity(3)

    def flattenPoints(self, point):
        x, y, z = point[0], point[1], point[2]
        constant = self.scale*abs(self.viewer[2] / (self.viewer[2] + z))
        screenX = int(self.width / 2 + (x*constant))
        screenY = int(self.height / 2 + (y*constant))
        return (screenX, screenY)

    def createMaze(self, square, faceNo, canvas):
        tL = self.points[square[0]]
        cWidth = [(self.points[square[3]][i] - self.points[square[0]][i]) / len(self.maze[faceNo]) for i in range(3)]
        cHeight = [(self.points[square[1]][i] - self.points[square[0]][i]) / len(self.maze[faceNo]) for i in range(3)]
        for i in range(len(self.maze[faceNo])):
            for j in range(len(self.maze[faceNo][i])):
                curr = [None]*4
                curr[0] = [tL[a] + (cWidth[a] * j) + (cHeight[a] * i) for a in range(3)]
                curr[1] = [tL[a] + (cWidth[a] * (j+1)) + (cHeight[a] * i) for a in range(3)]
                curr[2] = [tL[a] + (cWidth[a] * (j+1)) + (cHeight[a] * (i+1)) for a in range(3)]
                curr[3] = [tL[a] + (cWidth[a] * j) + (cHeight[a] * (i+1)) for a in range(3)]
                coords = []
                for val in curr:
                    coords.append(self.flattenPoints(val))
                
                for q in range(len(coords)):
                    if(self.maze[faceNo][i][j].direc[q]):
                        nextVal = (q+1) % len(coords)
                        canvas.create_line(coords[q][0], coords[q][1], coords[nextVal][0], coords[nextVal][1], width = 5)

    def createTriangles(self, points, textP, i, canvas):
        a, b, c, d = points[0], points[1], points[2], points[3]
        canvas.create_polygon(a[0], a[1], b[0], b[1], c[0], c[1], d[0], d[1], fill="white", outline ="gray")
        #canvas.create_text(textP[0], textP[1], text= f"{i}")

    def render(self, canvas):
        coord = []
        triangles = []
        mazes = []

        for point in self.points:
            coord.append(self.flattenPoints(point))

        for i, triangle in enumerate(self.triangles):
            avgZ = -((self.points[triangle[0]][2] + self.points[triangle[1]][2] + self.points[triangle[2]][2] + self.points[triangle[3]][2])/4)*10
            #triangles.append((coord[triangle[0]], coord[triangle[1]], coord[triangle[2]], coord[triangle[3]], avgZ))
            triangles.append((triangle, self.mazeOrder[i], avgZ))
        
        #Sort Maze List
        triangles.sort(key = lambda x: x[-1])

        for i, triangle in enumerate(triangles):
            coordList = []
            for val in triangle[0]:
                coordList.append(coord[val])
            text3DPoint = self.getTextPoint(triangle[0])
            self.createTriangles(coordList,text3DPoint, i, canvas)
            self.createMaze(triangle[0], triangle[1], canvas)

            #self.createTriangles(triangle[:-1], i, canvas)
   
    def getTextPoint(self, triangle):
        p1, p2 = self.points[triangle[0]], self.points[triangle[2]]
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

        self.matrixRegister = np.identity(3)
            

   # def rotateAboutAxi(self, axisVec, angle):
   #     angle = angle / 450 * 180 / math.pi
   #     vecMag = (axisVec[0]**2 + axisVec[1]**2+axisVec[2]**2)**0.5
   #     for j in range(len(axisVec)):
   #         axisVec[j] /= vecMag
   #     cos_T, sin_T = math.cos(angle), math.sin(angle)
   #     for i, point in enumerate(self.points):
   #         newX, newY, newZ = [], [], []
   #         newX.append(point[0] * (cos_T + (axisVec[0]**2)*(1-cos_T)))
   #         newX.append(point[1] * (axisVec[0] * axisVec[1] * (1-cos_T) - axisVec[2] * (sin_T)))
   #         newX.append(point[2] * (axisVec[0] * axisVec[2] * (1-cos_T) + axisVec[1] * (sin_T)))
#
#            newY.append(point[0] * (axisVec[1] * axisVec[2] * (1-cos_T) + axisVec[2] * (sin_T)))
#            newY.append(point[1] * (cos_T + (axisVec[1]**2)*(1-cos_T)))
#            newY.append(point[2] * (axisVec[1] * axisVec[2] * (1-cos_T) - axisVec[0] * (sin_T)))
#
#            newZ.append(point[0] * (axisVec[2] * axisVec[0] * (1-cos_T) - axisVec[1] * (sin_T)))
#            newZ.append(point[1] * (axisVec[2] * axisVec[1] * (1-cos_T) + axisVec[0] * (sin_T)))
#            newZ.append(point[2] * (cos_T + (axisVec[2]**2)*(1-cos_T)))
#            self.points[i] = (sum(newX), sum(newY), sum(newZ))

