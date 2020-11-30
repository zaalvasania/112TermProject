from cmu_112_graphics import *
from renderer import Engine
from primsMaze import Maze
from tank import Tank
from enemy import Enemy
from coin import Coin
from PIL import Image, ImageTk
import time, math, random
from startPageTank import StartTank, StartAI

class GameMode(Mode):
    def appStarted(mode, cVis = 7):
        points = [(-1,-1,-1),(-1,-1,1),(-1,1,1),(-1,1,-1),(1,-1,-1),(1,-1,1),(1,1,1),(1,1,-1)]
        #triangles = [(0,1,2),(0,2,3), (2,3,7),(2,7,6), (1,2,5),(2,5,6), (0,1,4),(1,4,5), (4,5,6),(4,6,7), (3,7,4),(4,3,0)]
        squares = [(0,3,7,4), (3,2,6,7), (7,6,5,4), (4,5,1,0), (0,1,2,3), (2,1,5,6)]
        mode.cVis = cVis
        mode.maze = mode.splitMaze(mode.generateMaze())
        mode.renderer = Engine(points, squares, mode.width, mode.height, mode.maze)
        mode.player = Tank(mode.maze[0], mode.cVis, 0, 'green')
        mode.mouse = [None, None]
        mode.isPaused = False
        mode.rotate, mode.moveMag = 0, 0
        mode.rotateAtEdge, mode.direcAtEdge, mode.count = 0, 0, 0
        mode.isRotating = False
        mode.bullets = []
        mode.createEnemies(mode.maze, mode.cVis, 'red')
        mode.createCoins()
        # Image sourced from https://kahum.itch.io/hilo-rojo
        mode.heartImg = Image.open('Assets/heart.png').resize((50,50), Image.ANTIALIAS)

        # Image sourced from http://pixelartmaker.com/art/0bdcda61357b87b
        mode.explosionImg = Image.open('Assets/explosion.png').resize((70,70), Image.ANTIALIAS)
        mode.exploded = None
        mode.explodedTimer = 0
        mode.timer = time.time()
        mode.countingDown = 3

    def createCoins(mode):
        mode.coins = []
        for i in range(len(mode.maze)):
            for _ in range(2):
                a, b = random.randint(0, len(mode.maze[i])-1), random.randint(0, len(mode.maze[i][0])-1)
                mode.coins.append(Coin([a,b], i, len(mode.maze[i])))

    def createEnemies(mode, mazes, cVis, color):
        mode.enemies = []
        for i in range(len(mazes)):
            mode.enemies.append(Enemy(mazes[i], cVis, i, color))

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

        for mazeList in newMazeList:
            for i in range(len(mazeList[0])):
                mazeList[0][i].direc[0] = True
                mazeList[-1][i].direc[2] = True

            for i in range(len(mazeList)):
                mazeList[i][0].direc[-1] = True
                mazeList[i][-1].direc[1] = True

        return newMazeList

    def keyPressed(mode, event):
        if(event.key == 'h'):
            mode.app.setActiveMode(mode.app.helpMode)
        if(event.key == "p"):
            mode.isPaused = not mode.isPaused
            if(mode.renderer.isPaused):
                mode.renderer.unRotate()
                mode.renderer.scale = 130
            mode.renderer.isPaused = not mode.renderer.isPaused
        elif(mode.isPaused):
            if(event.key == 'r'):
                mode.appStarted()
                #mode.renderer.scale +=10
            return
        elif(event.key == 'Up'):
            mode.moveMag = 0.02
        elif(event.key == 'Down'):
            mode.moveMag = -0.02
        elif(event.key == 'Right'):
            mode.rotate = 15
        elif(event.key == 'Left'):
            mode.rotate = -15

    def mousePressed(mode, event):
        if(mode.isPaused): return
        mode.bullets.append(mode.player.shootBullet())

    def keyReleased(mode, event):
        if(event.key == 'Up' or event.key == 'Down'):
            mode.moveMag = 0
        if(event.key == 'Left' or event.key == 'Right'):
            mode.rotate = 0

    def timerFired(mode):
        if(mode.countingDown > 0):
            if(time.time() - mode.timer > 1):
                mode.countingDown -= 1
                mode.timer = time.time()
            return
        if(mode.isPaused): return
        if(time.time() - mode.explodedTimer < 0.3):
            return
        else:
            mode.exploded = None

        if(mode.isRotating):
            mode.renderer.rotateAboutAxisCalcAngle(mode.rotateAtEdge, mode.direcAtEdge/10)
            mode.count+=1
            if(mode.count == 10):
                mode.isRotating = False
            return
        mode.playerMovement()
        mode.bulletMovement()
        mode.enemyMovement()
        mode.bulletCollision()
        mode.coinUpdate()

    def coinUpdate(mode):
        index = 0
        while(index < len(mode.coins)):
            mode.coins[index].calculateCorners()
            if(mode.coins[index].currMaze == mode.player.currMaze):
                if(mode.coins[index].collides(mode.player)):
                    mode.coins.pop(index)
                    mode.player.score += 1
                    continue
            index+=1

    def bulletCollision(mode):
        index = 0
        while(index < len(mode.bullets)):
            bullet = mode.bullets[index]
            if(bullet.currMaze == mode.player.currMaze):
                if(bullet.collides(mode.player)):
                    mode.player.health -= 1
                    mode.bullets.pop(index)
                    continue
            flag = False
            for i in range(len(mode.enemies)):
                if(mode.enemies[i].currMaze == bullet.currMaze):
                    if(bullet.collides(mode.enemies[i])):
                        mode.enemies[i].health-=1
                        mode.bullets.pop(index)
                        flag = True
                        break
            if(not flag):
                index+=1

        index = 0
        while(index < len(mode.enemies)):
            if(mode.enemies[index].health==0):
                temp = mode.enemies.pop(index)
                mode.player.score+=2
                if(mode.exploded == None):
                    mode.exploded = mode.renderer.getCoords(temp)
                    mode.explodedTimer = time.time()
            else:
                index+=1

    def enemyMovement(mode):
        for enemy in mode.enemies:
            enemy.enemyMovement()

    def bulletMovement(mode):
        index = 0
        while index < len(mode.bullets):
            bullet = mode.bullets[index]
            bullet.move()
            if(bullet.collideCount > 5):
                mode.bullets.pop(index)
            else: index+=1

    def playerMovement(mode):
        if(mode.moveMag != 0):
            mode.player.move(mode.moveMag)
            rotation, direc = mode.player.hitEdge(mode.maze)
            if(rotation!= None):
                mode.isRotating = True
                mode.rotateAtEdge, mode.direcAtEdge, mode.count = rotation, direc, 0
                    #mode.renderer.rotateAboutAxisCalcAngle(rotation, direc)
        if(mode.rotate != 0):
            mode.player.rotate(mode.rotate)

    def mouseMoved(mode, event):
        if(mode.isPaused): return
        mode.player.adjustCanAng(event.x, event.y)
    
    def mouseDragged(mode, event):
        if(not mode.isPaused): return
        mode.mouse.insert(0, (event.x, event.y))
        mode.mouse.pop()
        if(mode.mouse[0]!= None and mode.mouse[1] != None):
            vecX = mode.mouse[0][0] - mode.mouse[1][0]
            vecY = mode.mouse[0][1] - mode.mouse[1][1]
            mode.renderer.rotateAboutAxis([vecY, -vecX, 0], 1)

    def drawHealth(mode, canvas):
        dHeart = 50
        for i in range(mode.player.health):
            canvas.create_image(25 + i*dHeart, 25, image = ImageTk.PhotoImage(mode.heartImg))

    def drawPaused(mode, canvas):
        canvas.create_text(mode.width/2, 8*mode.height/9, text='PAUSED', font = 'Arial 40 bold')

    def drawScore(mode, canvas):
        canvas.create_text(mode.width-10, 10, text = f'Score: {mode.player.score}', anchor = 'ne', font = 'Arial 20 bold')
    
    def drawCountdown(mode, canvas):
        canvas.create_text(mode.width / 2, mode.height / 2, text = f'{mode.countingDown}', font = 'Arial 80 bold')

    def redrawAll(mode, canvas):
        mode.drawHealth(canvas)
        mode.drawScore(canvas)
        if(mode.isPaused):
            mode.drawPaused(canvas)
        mode.renderer.render(canvas, mode.player, mode.bullets, mode.enemies, mode.coins)
        if(mode.exploded != None):
            canvas.create_image(mode.exploded[0], mode.exploded[1], image = ImageTk.PhotoImage(mode.explosionImg))
        if(mode.countingDown > 0):
            mode.drawCountdown(canvas)
        #mode.renderer.rotateAboutAxis([0,1,0],5*1.9738)
        #mode.renderer.rotateAboutAxis([1,0,0],-5*1.9738)
        #mode.renderer.renderTank(canvas, mode.player)

###############################################################################################

class HelpMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, 150, text='This is the help screen!', font=font)
        canvas.create_text(mode.width/2, 250, text='(Insert helpful message here)', font=font)
        canvas.create_text(mode.width/2, 350, text='Press any key to return to the game!', font=font)

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)
        mode.app.gameMode.appStarted(cVis = 5)

###############################################################################################

class StartMode(Mode):
    def appStarted(mode):
        points = [(-1,-1,-1),(-1,-1,1),(-1,1,1),(-1,1,-1),(1,-1,-1),(1,-1,1),(1,1,1),(1,1,-1)]
        #triangles = [(0,1,2),(0,2,3), (2,3,7),(2,7,6), (1,2,5),(2,5,6), (0,1,4),(1,4,5), (4,5,6),(4,6,7), (3,7,4),(4,3,0)]
        squares = [(0,3,7,4), (3,2,6,7), (7,6,5,4), (4,5,1,0), (0,1,2,3), (2,1,5,6)]
        mode.cVis = 7
        mode.maze = mode.splitMaze(mode.generateMaze())
        mode.renderer = Engine(points, squares, mode.width, mode.height, mode.maze)
        mode.renderer.scale = 80

        # Created using https://www.pixilart.com/
        mode.tank = StartTank('Assets/tank.png', mode.width, mode.height, mode.width/2, mode.height/2)
        mode.initialiseEnemies()
        mode.timer = 0

        # Image sourced from https://www.subpng.com/png-cyqgdb/
        mode.settings = Image.open('Assets/settings.png').resize((50,50), Image.ANTIALIAS)

        # Positions for Buttons
        mode.settingsButton = [(mode.width-55, mode.width-5),(5,55), 's', ['gray', 'black']]
        mode.startButton = [(mode.width / 2 - 170, mode.width / 2 - 25),(4*mode.height/5, 4*mode.height/5 + 45), 'p', ['gray', 'black']]
        mode.helpButton = [(mode.width / 2 + 25, mode.width / 2 + 170), (4*mode.height / 5, 4*mode.height / 5 + 45), 'h', ['gray', 'black']]
        mode.buttons = [mode.settingsButton, mode.startButton, mode.helpButton]
        mode.isHovering = False


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
                button[-1] = ['black', 'gray']
                check = True
            else:
                button[-1] = ['gray', 'black']
        return check

    def mousePressed(mode, event):
        result = mode.withinRange(event)
        if(result == 'p'):
            mode.app.setActiveMode(mode.app.gameMode)
        elif(result == 's'):
            return
            mode.app.setActiveMode(mode.app.settingsMode)
        elif(result == 'h'):
            mode.app.setActiveMode(mode.app.helpMode)

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

    def moveEnemies(mode):
        for enemy in mode.enemies:
            enemy.move()

    def drawTitle(mode, canvas):
        canvas.create_text(mode.width/2, 70, text = 'Tank Wars 3D!', font = 'Arial 38 bold italic')

    def drawTanks(mode, canvas):
        mode.tank.drawTank(canvas)
        for enemy in mode.enemies:
            enemy.drawTank(canvas)

    def drawButtons(mode,canvas):
        canvas.create_rectangle(mode.startButton[0][0], mode.startButton[1][0], mode.startButton[0][1], mode.startButton[1][1], fill = mode.startButton[-1][0])
        canvas.create_text(sum(mode.startButton[0])/2, sum(mode.startButton[1])/2, text = 'Play!', font = 'Arial 30 bold italic', fill = mode.startButton[-1][1])

        canvas.create_rectangle(mode.helpButton[0][0], mode.helpButton[1][0], mode.helpButton[0][1], mode.helpButton[1][1], fill = mode.helpButton[-1][0])
        canvas.create_text(sum(mode.helpButton[0])/2, sum(mode.helpButton[1])/2, text = 'Help', font = 'Arial 30 bold italic', fill = mode.helpButton[-1][1])

        canvas.create_rectangle(mode.settingsButton[0][0], mode.settingsButton[1][0], mode.settingsButton[0][1], mode.settingsButton[1][1], fill = mode.settingsButton[-1][0])
        img = mode.settings.resize((50,50), Image.ANTIALIAS)
        canvas.create_image(sum(mode.settingsButton[0])/2, sum(mode.settingsButton[1])/2, image = ImageTk.PhotoImage(img))

    def redrawAll(mode, canvas):
        mode.renderer.render(canvas, None, [], [], [])
        mode.drawTanks(canvas)
        mode.drawTitle(canvas)
        mode.drawButtons(canvas)

# Modal App Structure sourced from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
class MyModalApp(ModalApp):
    def appStarted(app):
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.startScreen = StartMode()
        #app.setActiveMode(app.gameMode)
        app.setActiveMode(app.startScreen)
        app.timerDelay = 30
    
def main():
    MyModalApp(width = 500, height = 500)

if __name__ == "__main__":
    main()
