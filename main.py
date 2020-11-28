from cmu_112_graphics import *
from renderer import Engine
from primsMaze import Maze
from tank import Tank
from enemy import Enemy
from PIL import Image, ImageTk
import time,math

class GameMode(Mode):
    def appStarted(mode):
        points = [(-1,-1,-1),(-1,-1,1),(-1,1,1),(-1,1,-1),(1,-1,-1),(1,-1,1),(1,1,1),(1,1,-1)]
        #triangles = [(0,1,2),(0,2,3), (2,3,7),(2,7,6), (1,2,5),(2,5,6), (0,1,4),(1,4,5), (4,5,6),(4,6,7), (3,7,4),(4,3,0)]
        squares = [(0,3,7,4), (3,2,6,7), (7,6,5,4), (4,5,1,0), (0,1,2,3), (2,1,5,6)]
        mode.cVis = 7
        mode.maze = mode.splitMaze(mode.generateMaze())
        mode.renderer = Engine(points, squares, mode.width, mode.height, mode.maze)
        mode.player = Tank(mode.maze[0], mode.cVis, 0, 'green')
        mode.mouse = [None, None]
        mode.isPaused = False
        #mode.renderer.rotateAboutAxis([1,0,0], 1.5)
        mode.rotate, mode.moveMag = 0, 0
        mode.rotateAtEdge, mode.direcAtEdge, mode.count = 0, 0, 0
        mode.isRotating = False
        mode.bullets = []
        mode.createEnemies(mode.maze, mode.cVis, 'red')
        mode.timer = 0
        #mode.unRotate, mode.rotAng, mode.axis, mode.currRot = False, 0, [], 0

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
                #mode.unRotate = True
                #mode.rotAng, mode.axis = mode.renderer.unRot()
                #mode.rotAng 
                mode.renderer.unRotate()
                mode.renderer.scale = 130
            mode.renderer.isPaused = not mode.renderer.isPaused
        elif(mode.isPaused):
            if(event.key == 'z'):
                mode.renderer.scale +=10
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
        if(mode.isPaused): return
        if(mode.isRotating):
            mode.renderer.rotateAboutAxisCalcAngle(mode.rotateAtEdge, mode.direcAtEdge/10)
            mode.count+=1
            if(mode.count == 10):
                mode.isRotating = False
            return
        mode.playerMovement()
        if(time.time() - mode.timer > 0.005):
            mode.bulletMovement()
            mode.enemyMovement()
            mode.timer = time.time()

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

    def redrawAll(mode, canvas):
        mode.renderer.render(canvas, mode.player, mode.bullets, mode.enemies)
        #mode.renderer.rotateAboutAxis([0,1,0],5*1.9738)
        #mode.renderer.rotateAboutAxis([1,0,0],-5*1.9738)
        #mode.renderer.renderTank(canvas, mode.player)

class HelpMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, 150, text='This is the help screen!', font=font)
        canvas.create_text(mode.width/2, 250, text='(Insert helpful message here)', font=font)
        canvas.create_text(mode.width/2, 350, text='Press any key to return to the game!', font=font)

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.setActiveMode(app.gameMode)
        app.timerDelay = 30

def main():
    MyModalApp(width = 500, height = 500)

if __name__ == "__main__":
    main()
