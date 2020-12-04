from cmu_112_graphics import *
from renderer import Engine
from primsMaze import Maze
from tank import Tank
from enemy import Enemy
from coin import *
from PIL import Image, ImageTk
import time, math, random, copy


class GameMode(Mode):
    def appStarted(mode, cVis = 7, bulTimer = 1.5, movePar = 0.015):
        points = [(-1,-1,-1),(-1,-1,1),(-1,1,1),(-1,1,-1),(1,-1,-1),(1,-1,1),(1,1,1),(1,1,-1)]
        #triangles = [(0,1,2),(0,2,3), (2,3,7),(2,7,6), (1,2,5),(2,5,6), (0,1,4),(1,4,5), (4,5,6),(4,6,7), (3,7,4),(4,3,0)]
        squares = [(0,3,7,4), (3,2,6,7), (7,6,5,4), (4,5,1,0), (0,1,2,3), (2,1,5,6)]
        mode.cVis = cVis
        mode.bulletTimerParam, mode.moveParam = bulTimer, movePar
        mode.maze = mode.splitMaze(mode.generateMaze())
        mode.renderer = Engine(points, squares, mode.width, mode.height, mode.maze)
        mode.renderer.rotateAboutAxis([1,0,0], 1)
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

        # Image sourced from http://pixelartmaker.com/art/0bdcda61357b87b
        mode.explosionImg = Image.open('Assets/explosion.png').resize((70,70), Image.ANTIALIAS)
        mode.exploded = None
        mode.explodedTimer = 0
        mode.bulletTimer = 0
        mode.timer = time.time()
        mode.countingDown = 3
        mode.diff = 2
        mode.backWheel = ['green', 'cyan', 'yellow', 'red']
        mode.backTimer, mode.currBack = time.time(), random.choice(mode.backWheel)
        mode.shootTimer = time.time()
        mode.tLCoin = ReprCoin([mode.width - 80, 30])
        mode.endGameState = 0
        mode.countTime, mode.trackTime = 0, 0

    def createCoins(mode):
        mode.coins = []
        for i in range(len(mode.maze)):
            for _ in range(2):
                a, b = random.randint(0, len(mode.maze[i])-1), random.randint(0, len(mode.maze[i][0])-1)
                mode.coins.append(Coin([a,b], i, len(mode.maze[i])))

    def createEnemies(mode, mazes, cVis, color):
        mode.enemies = []
        for i in range(len(mazes)):
            mode.enemies.append(Enemy(mazes[i], cVis, i, color, mode.moveParam))

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
            mode.renderer.isPaused = not mode.renderer.isPaused
        elif(mode.isPaused):
            if(event.key == 'r'):
                mode.appStarted()
            elif(event.key == 'Escape'):
                mode.app.setActiveMode(mode.app.startScreen)
                #mode.renderer.scale +=10
            return
        elif(event.key == 'r'):
            mode.renderer.unRotate()
        elif(event.key == 'Up'):
            mode.moveMag = 0.02
        elif(event.key == 'Down'):
            mode.moveMag = -0.02
        elif(event.key == 'Right'):
            mode.rotate = 15
        elif(event.key == 'Left'):
            mode.rotate = -15

    def mousePressed(mode, event):
        if(mode.endGameState != 0):
            result = mode.checkInRange(event)
            if(result == 0):
                if(mode.endGameState == 1):
                    mode.appStarted(cVis = mode.cVis)
                elif(mode.endGameState == 2):
                    cVis, fireRate, moveSpeed = mode.cVis, mode.bulletTimerParam, mode.moveParam
                    timeT = mode.trackTime
                    score = mode.player.score
                    arr = [3, 5, 7, 9]
                    arr.remove(cVis)
                    mode.appStarted(random.choice(arr), fireRate*0.9, moveSpeed * 1.3)
                    mode.player.score = score
                    mode.trackTime = timeT
                return
            elif(result == 1):
                mode.app.setActiveMode(mode.app.startScreen)
                return
        if(mode.isPaused): return
        if(time.time() - mode.shootTimer > 0.5):
            mode.bullets.append(mode.player.shootBullet())
            mode.shootTimer = time.time()

    def checkInRange(mode, event):
        if((mode.width / 2 - 75) <= event.x <= (mode.width / 2 + 75)):
            if((mode.height / 2 - 10) <= event.y <= (mode.height / 2 + 40)):
                return 0
            if((mode.height / 2 + 60) <= event.y <= (mode.height / 2 + 110)):
                return 1
        return 2

    def keyReleased(mode, event):
        if(event.key == 'Up' or event.key == 'Down'):
            mode.moveMag = 0
        if(event.key == 'Left' or event.key == 'Right'):
            mode.rotate = 0

    def timerFired(mode):
        mode.tLCoin.calculateCorners()
        if(mode.countingDown > 0):
            if(time.time() - mode.timer > 1):
                mode.countingDown -= 1
                mode.timer = time.time()
            return
        #if(mode.isPaused): return
        if(mode.endGameState != 0):
            mode.renderer.rotateAboutAxis([1,0,0], 1)
            mode.renderer.rotateAboutAxis([0,-1,0], 1)
            return
        if(not mode.isPaused and (time.time() - mode.countTime > 1)):
            mode.trackTime+=1
            mode.countTime = time.time()
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
        mode.checkGameOver()
        if(time.time() - mode.backTimer > 2):
            backWheel = copy.copy(mode.backWheel)
            backWheel.remove(mode.currBack)
            mode.currBack = random.choice(backWheel)
            mode.backTimer = time.time()

    def checkGameOver(mode):
        if(mode.player.health <= 0):
            mode.endGameState = 1
        elif(len(mode.coins) == 0 and len(mode.enemies) == 0):
            mode.endGameState = 2

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
                if(mode.exploded == None and temp.currMaze == mode.player.currMaze):
                    mode.exploded = mode.renderer.getCoords(temp)
                    mode.explodedTimer = time.time()
            else:
                index+=1

    def enemyMovement(mode):
        for enemy in mode.enemies:
            if((enemy.currMaze == mode.player.currMaze) and mode.isPaused):
                continue
            bullet = enemy.enemyMovement(mode.player.getCurrCell(), mode.player.currMaze, mode.diff, (mode.player.cX, mode.player.cY))
            if(bullet != None and time.time() - mode.bulletTimer > mode.bulletTimerParam):
                mode.bullets.append(bullet)
                mode.bulletTimer = time.time()

    def enemyResolve(mode):
        for enemy in mode.enemies:
            if(mode.player.currMaze == enemy.currMaze):
                enemy.resolveMaze(mode.player.getCurrCell())

    def bulletMovement(mode):
        index = 0
        while index < len(mode.bullets):
            bullet = mode.bullets[index]
            if((bullet.currMaze == mode.player.currMaze) and mode.isPaused): 
                index+=1
                continue
            bullet.move()
            if(bullet.collideCount > 5):
                mode.bullets.pop(index)
            else: index+=1

    def playerMovement(mode):
        if(mode.moveMag != 0):
            mode.player.move(mode.moveMag)
            mode.enemyResolve()
            rotation, direc = mode.player.hitEdge(mode.maze)
            if(rotation!= None):
                mode.isRotating = True
                mode.rotateAtEdge, mode.direcAtEdge, mode.count = rotation, direc, 0
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
        canvas.create_rectangle(15, 15, 300, 50, width = 3, fill = 'white')
        canvas.create_rectangle(15, 15, 15+285*(max(mode.player.health,0) / 20), 50, width = 3, fill = 'red')
       # for i in range(mode.player.health):
       #     canvas.create_image(12.5 + i*dHeart, 12.5, image = ImageTk.PhotoImage(mode.heartImg))

    def drawPaused(mode, canvas):
        canvas.create_text(mode.width/2, 8*mode.height/9, text='PAUSED', font = 'Courier 50 bold')

    def drawScore(mode, canvas):
        t1, t2, t3, t4 = mode.tLCoin.corners
        canvas.create_polygon(t1[0], t1[1], t2[0], t2[1], t3[0], t3[1], t4[0], t4[1], fill = 'yellow', outline = 'black')
        canvas.create_text(mode.width - 32, 30, text = f'{mode.player.score}', font = 'Courier 40 bold')
    
    def drawCountdown(mode, canvas):
        canvas.create_text(mode.width / 2, mode.height / 2, text = f'{mode.countingDown}', font = 'Arial 80 bold')

    def drawEndState(mode, canvas):
        if(mode.endGameState == 1):
            text = ['GAME OVER!', 'Restart', 'Menu']
        elif(mode.endGameState == 2):
            text = ['LEVEL PASSED!', 'Next Level', 'Menu']
        canvas.create_text(mode.width / 2, mode.height / 2 - 50, text = text[0], font = 'Courier 70 bold')
        
        font = 'Courier 30 bold'
        if(text[1] == 'Next Level'): font = 'Courier 20 bold'

        canvas.create_rectangle(mode.width / 2 - 75, mode.height / 2 - 10, mode.width / 2 + 75, mode.height / 2 + 40, fill = 'white', outline = 'black', width = 5)
        canvas.create_text(mode.width / 2, mode.height / 2 + 15, text = text[1], font = font)
        canvas.create_rectangle(mode.width / 2 - 75, mode.height / 2 + 60, mode.width / 2 + 75, mode.height / 2 + 110, fill = 'white', outline = 'black', width = 5)
        canvas.create_text(mode.width / 2, mode.height / 2 + 85, text = text[2], font = font)

    def drawTime(mode, canvas):
        minutes = str(mode.trackTime // 60)
        seconds = str(mode.trackTime % 60)
        if(int(seconds) < 10):
            seconds = "0" + seconds
        canvas.create_text(mode.width / 2, mode.height - 60, text = f'{minutes}:{seconds}', font = 'Courier 40 bold')

    def redrawAll(mode, canvas):
        canvas.create_rectangle(-5, -5, mode.width+5, mode.height+5, fill = mode.currBack)
        mode.drawHealth(canvas)
        mode.drawScore(canvas)
        if(mode.isPaused):
            mode.drawPaused(canvas)
        else:
            mode.drawTime(canvas)
        mode.renderer.render(canvas, mode.player, mode.bullets, mode.enemies, mode.coins)
        if(mode.exploded != None):
            canvas.create_image(mode.exploded[0], mode.exploded[1], image = ImageTk.PhotoImage(mode.explosionImg))
        if(mode.countingDown > 0):
            mode.drawCountdown(canvas)
        if(mode.endGameState != 0):
            mode.drawEndState(canvas)
        #mode.renderer.rotateAboutAxis([0,1,0],5*1.9738)
        #mode.renderer.rotateAboutAxis([1,0,0],-5*1.9738)
        #mode.renderer.renderTank(canvas, mode.player)
