from cmu_112_graphics import *
from gameMode import GameMode
from startPage import StartMode

class HelpMode(Mode):

    def appStarted(mode):
        mode.backImage = Image.open('Assets/back.png').resize((70,70), Image.ANTIALIAS)

    def redrawAll(mode, canvas):
        font = 'Arial 30 bold'

        canvas.create_rectangle(mode.width/8-15, 105, 7*mode.width/8 - 15, 365, fill = 'black')
        canvas.create_rectangle(mode.width/8, 120, 7*mode.width/8, 380, fill = 'gray')
        canvas.create_text(mode.width/2, 50, text='How to Play!', font='Arial 40 bold')
        canvas.create_text(mode.width/2+3, 53, text='How to Play!', font='Arial 40 bold')
        canvas.create_text(mode.width/2, 150, text='Movement - Arrow Keys', font=font)
        canvas.create_text(mode.width/2, 200, text='Shooting - Mouse Clicks', font=font)
        canvas.create_text(mode.width/2, 250, text='Pause - P', font=font)
        canvas.create_text(mode.width/2, 300, text='Restart - R', font = font)
        canvas.create_text(mode.width/2, 350, text='Exit to Main Menu - Esc', font = font)

        canvas.create_image(mode.width/2, 425, image = ImageTk.PhotoImage(mode.backImage))

    def mousePressed(mode, event):
        if(mode.width/2 - 35 <= event.x <= mode.width/2 + 35 and
           390 <= event.y <= 460):
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

    def redrawAll(mode, canvas):
        mode.drawButtons(canvas)

# Modal App Structure sourced from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
class MyModalApp(ModalApp):
    def appStarted(app):
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.settingsMode = SettingsMode()
        app.startScreen = StartMode()
        app.setActiveMode(app.startScreen)
        app.timerDelay = 30
    
def main():
    MyModalApp(width = 500, height = 500)

if __name__ == "__main__":
    main()
