import math, random, time, copy
from cmu_112_graphics import *
from PIL import Image, ImageTk
from renderer import Engine
from primsMaze import Maze

##### STARTPAGE.py #####
# This file contains the core functionalities
# of the start screen. It also contains two classes
# that allow for the movement of tanks on the main screen

class StartMode(Mode):
    def appStarted(mode, cVis = 7):
        points = [(-1,-1,-1),(-1,-1,1),(-1,1,1),(-1,1,-1),(1,-1,-1),(1,-1,1),(1,1,1),(1,1,-1)]
        squares = [(0,3,7,4), (3,2,6,7), (7,6,5,4), (4,5,1,0), (0,1,2,3), (2,1,5,6)]
        mode.cVis, mode.diff = cVis, 2
        mode.maze = mode.splitMaze(mode.generateMaze())
        mode.renderer = Engine(points, squares, mode.width, mode.height, mode.maze)
        mode.renderer.scale = 120

        # Created using https://www.pixilart.com/
        mode.tank = StartTank('Assets/tank.png', mode.width, mode.height, mode.width/2, mode.height/2)
        mode.initialiseEnemies()
        mode.timer = 0

        # Image sourced from https://www.subpng.com/png-cyqgdb/
        mode.settings = Image.open('Assets/settings.png').resize((50,50), Image.ANTIALIAS)
        # Image sourced from https://toppng.com/trophy-trophy-pixel-art-PNG-free-PNG-Images_197247?search-result=glass-trophy
        mode.trophy = Image.open('Assets/trophy.png').resize((50,50), Image.ANTIALIAS)

        # Positions for Buttons
        mode.settingsButton = [(mode.width-55, mode.width-5),(5,55), 's', ['gray', 'black']]
        mode.startButton = [(mode.width / 2 - 170, mode.width / 2 - 25),(4*mode.height/5, 4*mode.height/5 + 45), 'p', ['white', 'black']]
        mode.helpButton = [(mode.width / 2 + 25, mode.width / 2 + 170), (4*mode.height / 5, 4*mode.height / 5 + 45), 'h', ['white', 'black']]
        mode.leaderboardButton = [(5, 55), (5,55),'l',['gray','black']]
        mode.buttons = [mode.settingsButton, mode.startButton, mode.helpButton, mode.leaderboardButton]
        mode.isHovering = False
        mode.backWheel = ['green', 'cyan', 'yellow', 'red']
        mode.backTimer, mode.currBack = time.time(), random.choice(mode.backWheel)

    def initialiseEnemies(mode):
        mode.enemies = []
        for i in range(7):
            x, y = random.randint(0, mode.width), random.randint(0, mode.height)

            # Created using https://www.pixilart.com/
            newEnemy = StartAI('Assets/enemy.png', mode.width, mode.height, x, y)
            mode.enemies.append(newEnemy)
    
    def generateMaze(mode):
        maze = Maze(mode.cVis)
        while(not maze.generateStep()):
            pass
        return maze

    def splitMaze(mode,maze):
        newMazeList = []
        # Split vertical portion into 3 mazes one longer
        for i in range(0, maze.cVis*3, maze.cVis):
            newMazeList.append(maze.cList[i:i+maze.cVis])
        longMaze = newMazeList.pop(1)
        # Split middle portion into 4 mazes
        for i in range(0, maze.cVis*4, maze.cVis):
            splitMaze = [longMaze[j][i:i+maze.cVis] for j in range(len(longMaze))]
            newMazeList.insert(-1, splitMaze)
        return newMazeList

    def keyPressed(mode,event):
        if(event.key == "Left"):
            mode.tank.rotateAng = 1
        elif(event.key == "Right"):
            mode.tank.rotateAng = -1
        if(event.key == "Up"):
            mode.tank.doMoveForward = 1
        elif(event.key == 'Down'):
            mode.tank.doMoveForward = -1

    def keyReleased(mode, event):
        if(event.key == 'Up' or event.key == 'Down'):
            mode.tank.doMoveForward = 0
        if(event.key == "Left" or event.key == "Right"):
            mode.tank.rotateAng = 0

    def mouseMoved(mode, event):
        xDirec, yDirec = event.x - mode.tank.tCent[0], event.y - mode.tank.tCent[1]
        normal = (xDirec**2 + yDirec**2)**0.5
        if(normal!=0):
            mode.tank.canAng[0] = xDirec/normal
            mode.tank.canAng[1] = yDirec/normal

        if(not mode.isHovering):
            mode.isHovering = mode.checkWithinRange(event)
        else:
            mode.isHovering = not mode.checkWithinRange(event)

    def checkWithinRange(mode, event):
        check = False
        for button in mode.buttons:
            if(button[0][0] <= event.x <= button[0][1] and
              button[1][0] <= event.y <= button[1][1]):
                button[-1] = ['black', 'white']
                check = True
            else:
                button[-1] = ['white', 'black']
        return check

    def mousePressed(mode, event):
        result = mode.withinRange(event)
        if(result == 'p'):
            mode.app.setActiveMode(mode.app.gameMode)
            mode.app.gameMode.appStarted(mode.cVis)
            mode.app.gameMode.diff = mode.diff
        elif(result == 's'):
            mode.app.setActiveMode(mode.app.settingsMode)
            mode.app.settingsMode.cVis = mode.cVis
            mode.app.settingsMode.diff = mode.diff
        elif(result == 'h'):
            mode.app.setActiveMode(mode.app.helpMode)
        elif(result == 'l'):
            mode.app.setActiveMode(mode.app.leaderboard)

    def withinRange(mode, event):
        for button in mode.buttons:
            if(button[0][0] <= event.x <= button[0][1] and
              button[1][0] <= event.y <= button[1][1]):
                return button[-2]
        return None

    def timerFired(mode):
        mode.renderer.rotateAboutAxis([0,1,0], -1)
        mode.renderer.rotateAboutAxis([1,0,0], 1)
        if(mode.tank.doMoveForward != 0):
            mode.tank.moveForward()
        mode.tank.rotate()
        if(time.time() - mode.timer > 0.5):
            mode.moveEnemies()
            mode.timer = 0
        if(time.time() - mode.backTimer > 1):
            temp = copy.copy(mode.backWheel)
            temp.remove(mode.currBack)
            mode.currBack = random.choice(temp)
            mode.backTimer = time.time()

    def moveEnemies(mode):
        for enemy in mode.enemies:
            enemy.move()

    def drawTitle(mode, canvas):
        canvas.create_text(mode.width/2, 70, text = 'Tank Wars 3D!', font = 'Courier 45 bold')

    def drawTanks(mode, canvas):
        mode.tank.drawTank(canvas)
        for enemy in mode.enemies:
            enemy.drawTank(canvas)

    def drawButtons(mode,canvas):
        canvas.create_rectangle(mode.startButton[0][0], mode.startButton[1][0], mode.startButton[0][1], mode.startButton[1][1], fill = mode.startButton[-1][0], width = 5)
        canvas.create_text(sum(mode.startButton[0])/2, sum(mode.startButton[1])/2, text = 'Play!', font = 'Arial 30 bold italic', fill = mode.startButton[-1][1])

        canvas.create_rectangle(mode.helpButton[0][0], mode.helpButton[1][0], mode.helpButton[0][1], mode.helpButton[1][1], fill = mode.helpButton[-1][0], width = 5)
        canvas.create_text(sum(mode.helpButton[0])/2, sum(mode.helpButton[1])/2, text = 'Help', font = 'Arial 30 bold italic', fill = mode.helpButton[-1][1])

        canvas.create_rectangle(mode.settingsButton[0][0], mode.settingsButton[1][0], mode.settingsButton[0][1], mode.settingsButton[1][1], fill = mode.settingsButton[-1][0])
        img = mode.settings.resize((50,50), Image.ANTIALIAS)
        canvas.create_image(sum(mode.settingsButton[0])/2, sum(mode.settingsButton[1])/2, image = ImageTk.PhotoImage(img))
        canvas.create_rectangle(mode.leaderboardButton[0][0], mode.leaderboardButton[1][0], mode.leaderboardButton[0][1], mode.leaderboardButton[1][1], fill = mode.leaderboardButton[-1][0])
        img = mode.trophy.resize((50, 50), Image.ANTIALIAS)
        canvas.create_image(sum(mode.leaderboardButton[0])/2, sum(mode.leaderboardButton[1])/2, image = ImageTk.PhotoImage(img))

    def redrawAll(mode, canvas):
        canvas.create_rectangle(-5, -5, mode.width+5, mode.height+5, fill = mode.currBack)
        mode.renderer.render(canvas, None, [], [], [])
        mode.drawTanks(canvas)
        mode.drawTitle(canvas)
        mode.drawButtons(canvas)

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
