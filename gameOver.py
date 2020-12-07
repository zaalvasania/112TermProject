import math
from cmu_112_graphics import *

class GameOverScreen(Mode):
    def appStarted(mode, stage = 0, score = 0, time = 0):
        mode.stage = stage
        mode.coins = score
        mode.time = time
        mode.overallScore = mode.calculateOverallScore()
        mode.backImage = Image.open('Assets/back.png').resize((70,70), Image.ANTIALIAS)
        # Created using https://www.pixilart.com/
        mode.tankImage = Image.open('Assets/hugeTank.png').resize((300, 300), Image.ANTIALIAS)
        mode.mouse = [mode.width / 2, mode.height / 2]
        mode.playerName = "Player 1"
        mode.flag = False

    def calculateOverallScore(mode):
        if(mode.stage == 0):
            return int(mode.coins*50/12)
        avgTime = mode.time / mode.stage
        score = (mode.stage * 40) + ((mode.coins/((mode.stage+1)*12)) * 50) + (100*math.exp(-avgTime))
        return int(math.ceil(score))

    def mouseMoved(mode, event):
        mode.mouse = [event.x, event.y]

    def drawEdgeTanks(mode, canvas):
        img = mode.tankImage.rotate(225)
        canvas.create_image(30, 30, image = ImageTk.PhotoImage(img))
        img = mode.tankImage.rotate(135)
        canvas.create_image(mode.width - 30, 30, image = ImageTk.PhotoImage(img))
        img = mode.tankImage.rotate(45)
        canvas.create_image(mode.width - 30, mode.height - 30, image = ImageTk.PhotoImage(img))
        img = mode.tankImage.rotate(315)
        canvas.create_image(30, mode.height - 30, image = ImageTk.PhotoImage(img))
        for centX, centY in [(30,30), (mode.width-30, 30), (mode.width-30, mode.height-30), (30, mode.height-30)]:
            vec = [mode.mouse[0] - centX, mode.mouse[1] - centY]
            mag = (vec[0]**2 + vec[1]**2)**0.5
            if(mag != 0):
                vecScaled = [vec[0]/mag, vec[1]/mag]
            else:
                vecScaled = [vec[0]/0.01, vec[1]/0.01]
            canvas.create_line(centX, centY, centX+100*vecScaled[0], centY+100*vecScaled[1], width = 20)

    def keyPressed(mode, event):
        if(event.key == 'Delete'):
            mode.playerName = mode.playerName[:-1]
        elif(event.key == ','): return
        elif(event.key.isalnum() and len(event.key)==1):
            mode.playerName+=event.key
        elif(event.key == 'Space'):
            mode.playerName+=' '

    def mousePressed(mode, event):
        if(5<= event.x<= 75 and 5<= event.y<= 75):
            mode.writeScores()
            mode.app.setActiveMode(mode.app.startScreen)
        if(mode.width / 2 - 100 <= event.x <= mode.width / 2 + 100 and
          2*mode.height/3 <= event.y <= 2*mode.height / 3 + 40):
            mode.writeScores()
            mode.app.setActiveMode(mode.app.leaderboard)
            mode.app.leaderboard.appStarted()

    def writeScores(mode):
        try:
            f = open('Scores.txt', 'x')
            f.close()
        except: pass
        appendValue = f'{mode.playerName},{mode.overallScore}\n'
        with open("Scores.txt",'a',encoding = 'utf-8') as f:
            f.write(appendValue)

    def createNameText(mode, canvas):
        canvas.create_text(mode.width / 2, mode.height / 3, text = 'Game Stats for:', font='Courier 25 bold', anchor = 'e')
        minutes = str(mode.time // 60)
        seconds = str(mode.time % 60)
        if(int(seconds) < 10):
            seconds = "0" + seconds
        canvas.create_text(mode.width / 2, 5*mode.height / 12+10, text = f'Stages Complete: {mode.stage}\nTotal Score: {mode.coins}\nTotal Game Time: {minutes}:{seconds}', font = 'Courier 19 bold')
        canvas.create_text(mode.width / 2 + 20, mode.height / 3, text = f'{mode.playerName}', font = 'Courier 25 bold', anchor = 'w')
        canvas.create_text(mode.width / 2, mode.height / 2 + 50, text = f'OVERALL SCORE:{mode.overallScore}', font = 'Courier 35 bold')
        canvas.create_rectangle(mode.width / 2 - 100, 2*mode.height / 3, mode.width / 2 + 100, 2*mode.height / 3 + 40, fill = 'gray', outline = 'black')
        canvas.create_text(mode.width / 2, 2*mode.height / 3 + 20, text = 'LEADERBOARD', font = 'Courier 25 bold', fill = 'maroon')

    def redrawAll(mode, canvas):
        canvas.create_text(mode.width / 2, mode.height / 10, text = 'GAME OVER!', font = 'Courier 40 bold')
        mode.createNameText(canvas)
        mode.drawEdgeTanks(canvas)
        canvas.create_image(40, 40, image = ImageTk.PhotoImage(mode.backImage))

class ScoreScreen(Mode):
    def appStarted(mode):
        mode.buttonPositions = []
        mode.data = []

        try:
            f = open('Scores.txt', 'r')
            text = []
            for line in f:
                text.append(line)
            f.close()
            mode.organiseData(text)
        except: pass
        mode.backImage = Image.open('Assets/back.png').resize((70,70), Image.ANTIALIAS)
        # Created using https://www.pixilart.com/
        mode.tankImage = Image.open('Assets/hugeTank.png').resize((300, 300), Image.ANTIALIAS)
        mode.mouse = [mode.width / 2, mode.height / 2]

    def organiseData(mode, text):
        for data in text:
            temp = data.split(',')
            temp[1] = int(temp[1])
            mode.data.append(temp)
        mode.data.sort(key = lambda x: x[-1])
        mode.data = mode.data[:10][::-1]

    def mouseMoved(mode, event):
        mode.mouse = [event.x, event.y]

    def mousePressed(mode, event):
        if(5<= event.x<= 75 and 5<= event.y<= 75):
            #mode.writeScores()
            mode.app.setActiveMode(mode.app.startScreen)

    def drawEdgeTanks(mode, canvas):
        img = mode.tankImage.rotate(225)
        canvas.create_image(30, 30, image = ImageTk.PhotoImage(img))
        img = mode.tankImage.rotate(135)
        canvas.create_image(mode.width - 30, 30, image = ImageTk.PhotoImage(img))
        img = mode.tankImage.rotate(45)
        canvas.create_image(mode.width - 30, mode.height - 30, image = ImageTk.PhotoImage(img))
        img = mode.tankImage.rotate(315)
        canvas.create_image(30, mode.height - 30, image = ImageTk.PhotoImage(img))
        for centX, centY in [(30,30), (mode.width-30, 30), (mode.width-30, mode.height-30), (30, mode.height-30)]:
            vec = [mode.mouse[0] - centX, mode.mouse[1] - centY]
            mag = (vec[0]**2 + vec[1]**2)**0.5
            if(mag != 0):
                vecScaled = [vec[0]/mag, vec[1]/mag]
            else:
                vecScaled = [vec[0]/0.01, vec[1]/0.01]
            canvas.create_line(centX, centY, centX+100*vecScaled[0], centY+100*vecScaled[1], width = 20)

    def drawLeaderboard(mode, canvas):
        gap = 40
        for i in range(10):
            y = (gap*i) + mode.height / 4 - 20
            canvas.create_text(mode.width / 3 - 30, y, text = f'#{i+1}', font='Courier 25 bold', fill='blue')
            if(i<len(mode.data)):
                canvas.create_text(mode.width / 3, y, text=f'{mode.data[i][0]}', font='Courier 22 bold', anchor = 'w')
                canvas.create_text(mode.width / 3 + 200, y, text=f'{mode.data[i][1]}', font = 'Courier 22 bold', anchor = 'w', fill='red')


    def redrawAll(mode, canvas):
        canvas.create_text(mode.width / 2, mode.height / 10, text = 'LEADERBOARD', font = 'Courier 40 bold')
        mode.drawEdgeTanks(canvas)
        mode.drawLeaderboard(canvas)
        canvas.create_image(40, 40, image = ImageTk.PhotoImage(mode.backImage))
