from cmu_112_graphics import *
from renderer import Engine
from primsMaze import Maze

def appStarted(app):
    points = [(-1,-1,-1),(-1,-1,1),(-1,1,1),(-1,1,-1),(1,-1,-1),(1,-1,1),(1,1,1),(1,1,-1)]
    #triangles = [(0,1,2),(0,2,3), (2,3,7),(2,7,6), (1,2,5),(2,5,6), (0,1,4),(1,4,5), (4,5,6),(4,6,7), (3,7,4),(4,3,0)]
    squares = [(0,3,7,4), (3,2,6,7), (7,6,5,4), (4,5,1,0), (0,1,2,3), (2,1,5,6)]
    app.cVis = 7
    app.maze = splitMaze(generateMaze(app))
    app.renderer = Engine(points, squares, app.width, app.height, app.maze)
    app.mouse = [None, None]
    app.isPaused = False
    app.renderer.rotateAboutAxis([1,0,0], 1.5)
    #app.unRotate, app.rotAng, app.axis, app.currRot = False, 0, [], 0

def generateMaze(app):
    maze = Maze(app.cVis)
    while(not maze.generateStep()):
        pass
    return maze

def splitMaze(maze):
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

def keyPressed(app, event):
    if(event.key == "p"):
        app.isPaused = not app.isPaused
        if(app.renderer.isPaused):
            #app.unRotate = True
            #app.rotAng, app.axis = app.renderer.unRot()
            #app.rotAng 
            app.renderer.unRotate()
        app.renderer.isPaused = not app.renderer.isPaused


def timerFired(app):
    pass
    #if(app.unRotate):
    #app.renderer.rotateAboutAxis([1, 0, 0], 1)

def mouseDragged(app, event):
    if(not app.isPaused): return
    app.mouse.insert(0, (event.x, event.y))
    app.mouse.pop()
    if(app.mouse[0]!= None and app.mouse[1] != None):
        vecX = app.mouse[0][0] - app.mouse[1][0]
        vecY = app.mouse[0][1] - app.mouse[1][1]
        app.renderer.rotateAboutAxis([vecY, -vecX, 0], 1)

def redrawAll(app, canvas):
    app.renderer.render(canvas)

def main():
    runApp(width = 500, height = 500)

if __name__ == "__main__":
    main()
