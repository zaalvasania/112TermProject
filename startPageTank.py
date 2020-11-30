import math, random
from PIL import Image, ImageTk

class StartTank(object):
    def __init__(self, image, width, height, startX, startY):
        self.image = Image.open(image)
        self.tankAngle = 0
        self.tank_dAngle = 10
        self.tCent = [startX, startY]
        self.width, self.height = width, height
        self.canAng = [0, 1]
        self.canLen = 17
        self.normDirec = [1,0]
        self.rotateAng = 0
        self.doMoveForward = 0

    def rotate(self):
        self.tankAngle += self.rotateAng * self.tank_dAngle
        ang = self.tankAngle * math.pi/180
        self.normDirec = [math.cos(ang), -math.sin(ang)]

    def moveForward(self):
        self.tCent[0]+=self.normDirec[1]*(self.doMoveForward)*(7)
        self.tCent[1]-=self.normDirec[0]*(self.doMoveForward)*(7)
        if(self.tCent[0] < 10 or self.tCent[0] >= self.width-10 or
           self.tCent[1] < 10 or self.tCent[1] >= self.height-10):
            self.tCent[0]-=self.normDirec[1]*(self.doMoveForward)*(7)
            self.tCent[1]+=self.normDirec[0]*(self.doMoveForward)*(7)
            
    def drawTank(self,canvas):
        img = self.image.rotate(self.tankAngle)
        img = img.resize((60, 60), Image.ANTIALIAS)
        canvas.create_image(self.tCent[0], self.tCent[1], image = ImageTk.PhotoImage(img))
        canvas.create_oval(self.tCent[0] - 5, self.tCent[1] - 5, self.tCent[0] + 5, self.tCent[1] + 5, fill = 'black')
        canvas.create_line(self.tCent[0], self.tCent[1], self.tCent[0] + (self.canLen * self.canAng[0]), self.tCent[1] + (self.canLen * self.canAng[1]), width = 6)


class StartAI(StartTank):
    def move(self):
        if(random.random() < 0.1):
            L = [1, -1]
            self.rotateAng = random.choice(L)
            self.doMoveForward = random.choice(L)
        self.rotate()
        self.moveForward()
