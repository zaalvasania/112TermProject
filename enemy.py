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

    def updateHealthBar(self):
        self.hBtL = (self.cX - 6*self.lenX/5, self.cY - 8*self.lenY/5)

    def enemyMovement(self):
        if(random.random() < 0.3):
            self.currMovement = [random.choice(self.movement), random.choice(self.rotation)]

        if(0 not in self.currMovement):
            self.move(self.currMovement[0])
            self.rotate(self.currMovement[1])
            self.updateHealthBar()

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
