from cmu_112_graphics import *
from gameMode import GameMode
from startPage import StartMode
from gameOver import *

class HelpMode(Mode):

    def appStarted(mode):
        # Created using https://www.pixilart.com/
        mode.backImage = Image.open('Assets/back.png').resize((70,70), Image.ANTIALIAS)

    def redrawAll(mode, canvas):
        font = 'Courier 24 bold'

        canvas.create_text(mode.width/2, 50, text='How to Play!', font='Courier 40 bold')
        #canvas.create_rectangle(mode.width/8-15, 85, 7*mode.width/8 - 15, 275, fill = 'black')
        canvas.create_rectangle(mode.width/8, 95, 7*mode.width/8, 270, fill = '', outline = 'black')
        # Play Mode
        canvas.create_text(mode.width/2, 110, text='Movement - Arrow Keys', font=font)
        canvas.create_text(mode.width/2, 180, text='Shooting - Mouse Clicks', font=font)
        canvas.create_text(mode.width/2, 250, text='Pause - P', font=font)
        canvas.create_text(mode.width/8 + 20, 120, text = 'P', font = 'Courier 40 bold', fill = 'red')
        canvas.create_text(mode.width/8 + 20, 160, text = 'L', font = 'Courier 40 bold', fill = 'green')
        canvas.create_text(mode.width/8 + 20, 200, text = 'A', font = 'Courier 40 bold', fill = 'blue')
        canvas.create_text(mode.width/8 + 20, 240, text = 'Y', font = 'Courier 40 bold', fill = 'darkorange')

        canvas.create_text(mode.width - mode.width/8 - 20, 120, text = 'M', font = 'Courier 40 bold', fill = 'red')
        canvas.create_text(mode.width - (mode.width/8 + 20), 160, text = 'O', font = 'Courier 40 bold', fill = 'green')
        canvas.create_text(mode.width - (mode.width/8 + 20), 200, text = 'D', font = 'Courier 40 bold', fill = 'blue')
        canvas.create_text(mode.width - (mode.width/8 + 20), 240, text = 'E', font = 'Courier 40 bold', fill = 'darkorange')
        #canvas.create_text(mode.width/2, 300, text='Restart - R', font = font)
        #canvas.create_text(mode.width/2, 350, text='Exit to Main Menu - Esc', font = font)

        font = 'Courier 22 bold'
        canvas.create_rectangle(mode.width/8, 290, 7*mode.width/8, 500, fill = '', outline = 'black')
        canvas.create_text(mode.width/2, 320, text ='Rotation - Click and Drag', font=font)
        canvas.create_text(mode.width/2, 370, text ='Unpause - P', font=font)
        canvas.create_text(mode.width/2, 420, text ='Restart - R', font=font)
        canvas.create_text(mode.width/2, 460, text ='Exit to Main Menu - Esc', font=font)
        canvas.create_text(mode.width/8 + 20, 310, text = 'P', font = 'Courier 40 bold', fill = 'red')
        canvas.create_text(mode.width/8 + 20, 350, text = 'A', font = 'Courier 40 bold', fill = 'green')
        canvas.create_text(mode.width/8 + 20, 390, text = 'U', font = 'Courier 40 bold', fill = 'blue')
        canvas.create_text(mode.width/8 + 20, 430, text = 'S', font = 'Courier 40 bold', fill = 'darkorange')
        canvas.create_text(mode.width/8 + 20, 470, text = 'E', font = 'Courier 40 bold', fill = 'red')

        canvas.create_text(mode.width - mode.width/8 - 20, 330, text = 'M', font = 'Courier 40 bold', fill = 'red')
        canvas.create_text(mode.width - (mode.width/8 + 20), 370, text = 'O', font = 'Courier 40 bold', fill = 'green')
        canvas.create_text(mode.width - (mode.width/8 + 20), 410, text = 'D', font = 'Courier 40 bold', fill = 'blue')
        canvas.create_text(mode.width - (mode.width/8 + 20), 450, text = 'E', font = 'Courier 40 bold', fill = 'darkorange')

        canvas.create_image(mode.width/2, 535, image = ImageTk.PhotoImage(mode.backImage))

    def mousePressed(mode, event):
        if(mode.width/2 - 35 <= event.x <= mode.width/2 + 35 and
           535 - 35 <= event.y <= 535+35):
            mode.app.setActiveMode(mode.app.startScreen)

class SettingsMode(Mode):
    def appStarted(mode):
        mode.topButtons = (mode.width / 6, mode.height / 3)
        mode.botButtons = (mode.width / 6, 2*mode.height / 3)
        mode.botButWidth, mode.topButWidth = 2*mode.width / 9, mode.width / 6
        mode.word = ['Easy', 'Medium', 'Hard']
        mode.cVis = 7
        mode.diff = 0
        mode.color = ['gray', 'black']
        # Image sourced from http://pixelartmaker.com/art/d176c44ae0d9ffd
        mode.backImage = Image.open('Assets/back.png').resize((50,50), Image.ANTIALIAS)
        # Created using https://www.pixilart.com/
        mode.tankImage = Image.open('Assets/hugeTank.png').resize((300, 300), Image.ANTIALIAS)
        mode.mouse = [mode.width / 2, mode.height / 2]

    def drawButtons(mode, canvas):
        canvas.create_text(mode.width/2, 40, text = 'Settings', font = 'Arial 40 bold')
        canvas.create_text(mode.width/2, mode.topButtons[1] - 30, text = 'Maze Size', font = 'Arial 25 bold')
        canvas.create_text(mode.width/2, mode.botButtons[1] - 30, text = 'AI Difficulty', font = 'Arial 25 bold')
        
        start = 3
        for i in range(4):
            j = 0
            if(mode.cVis == start):
                j = 1
            tlX, tlY = mode.topButtons[0] + i*mode.topButWidth, mode.topButtons[1]
            brX, brY = mode.topButtons[0] + (i+1)*mode.topButWidth, mode.topButtons[1] + 40
            canvas.create_rectangle(tlX, tlY, brX, brY, fill = mode.color[j], outline = 'black')
            canvas.create_text((tlX + brX)/2, (tlY + brY)/2, text = start, font = 'Arial 25 bold', fill = mode.color[(j+1)%2])
            start+=2

        for i in range(3):
            j = 0
            if(mode.diff == i):
                j=1
            tlX, tlY = mode.botButtons[0] + i*mode.botButWidth, mode.botButtons[1]
            brX, brY = mode.botButtons[0] + (i+1)*mode.botButWidth, mode.botButtons[1] + 40
            canvas.create_rectangle(tlX, tlY, brX, brY, fill = mode.color[j], outline = 'black')
            canvas.create_text((tlX + brX)/2, (tlY + brY)/2, text = mode.word[i], font = 'Arial 20 bold', fill = mode.color[(j+1)%2])

        canvas.create_image(30, 30, image = ImageTk.PhotoImage(mode.backImage))

    def mousePressed(mode, event):
        mode.withinRange(event)
        if(5<= event.x<= 55 and 5<= event.y<= 55):
            mode.app.setActiveMode(mode.app.startScreen)
            mode.app.startScreen.appStarted(mode.cVis)
            mode.app.startScreen.diff = mode.diff

    def mouseMoved(mode, event):
        mode.mouse = [event.x, event.y]

    def withinRange(mode, event):
        start = 3
        for i in range(4):
            tlX, tlY = mode.topButtons[0] + i*mode.topButWidth, mode.topButtons[1]
            brX, brY = mode.topButtons[0] + (i+1)*mode.topButWidth, mode.topButtons[1] + 40
            if(tlX <= event.x <= brX and tlY <= event.y <= brY):
                mode.cVis = start
                return
            start+=2

        for i in range(3):
            tlX, tlY = mode.botButtons[0] + i*mode.botButWidth, mode.botButtons[1]
            brX, brY = mode.botButtons[0] + (i+1)*mode.botButWidth, mode.botButtons[1] + 40
            if(tlX <= event.x <= brX and tlY <= event.y <= brY):
                mode.diff = i
                return

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


    def redrawAll(mode, canvas):
        mode.drawEdgeTanks(canvas)
        mode.drawButtons(canvas)

# Modal App Structure sourced from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
class MyModalApp(ModalApp):
    def appStarted(app):
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.settingsMode = SettingsMode()
        app.startScreen = StartMode()
        app.gameOver = GameOverScreen()
        app.leaderboard = ScoreScreen()
        app.setActiveMode(app.startScreen)
        app.timerDelay = 30
    
def main():
    MyModalApp(width = 600, height = 600)

if __name__ == "__main__":
    main()
