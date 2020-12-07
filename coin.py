import math

##### COIN.py #####
# Coin class is primarily a data structure class containing
# information about specific points although it also does implement
# basic collission detection and corner calculation for translation into
# 3D

class Coin(object):
    def __init__(self, center, currMaze, cVis):
        self.cWidth, self.cHeight = 1/cVis, 1/cVis
        self.center = [(center[0]*self.cWidth)+self.cWidth/2, (center[1]*self.cHeight) + self.cHeight/2]
        self.currMaze = currMaze
        self.angle = 0
        self.calculateCorners()

    def calculateCorners(self, ret = False):
        corners = [None]*4
        x, y = self.center[0], self.center[1]
        percent = abs(math.cos(self.angle))
        width = (self.cWidth/4)*percent
        corners[0] = (x - (width), y)
        corners[1] = (x, y - (self.cHeight/4))
        corners[2] = (x + (width), y)
        corners[3] = (x, y + (self.cHeight/4))
        self.angle+=10*math.pi/180
        if(ret):
            return corners
        self.corners = corners

    def collides(self, enemy):
        distance = ((self.center[0] - enemy.cX)**2 + (self.center[1] - enemy.cY)**2)**0.5
        if(distance <= (self.cWidth/2)):
            return True
        return False

class ReprCoin(object):
    def __init__(self, center):
        self.center = center
        self.angle = 0
        self.width, self.height = 20, 20
        self.calculateCorners()

    def calculateCorners(self):
        corners = [None]*4
        x, y = self.center[0], self.center[1]
        percent = abs(math.cos(self.angle))
        width = (self.width)*percent
        corners[0] = (x - (width), y)
        corners[1] = (x, y - (self.height))
        corners[2] = (x + (width), y)
        corners[3] = (x, y + (self.height))
        self.angle+=10*math.pi/180
        self.corners = corners
