from cmu_112_graphics import *
from gameMode import GameMode
from startPage import StartMode

class HelpMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, 150, text='This is the help screen!', font=font)
        canvas.create_text(mode.width/2, 250, text='(Insert helpful message here)', font=font)
        canvas.create_text(mode.width/2, 350, text='Press any key to return to the game!', font=font)

    def keyPressed(mode, event):
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

    def drawButtons(mode, canvas):
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

        canvas.create_rectangle(5, 5, 55, 55, fill = 'gray')
        canvas.create_text(30, 30, text = '<-', font = 'Arial 20 bold')
            

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
        #app.setActiveMode(app.gameMode)
        app.setActiveMode(app.startScreen)
        app.timerDelay = 30
    
def main():
    MyModalApp(width = 500, height = 500)

if __name__ == "__main__":
    main()
