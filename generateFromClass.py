import random, time
from primsMaze import Maze
import tkinter as tk
from cmu_112_graphics import *

def appStarted(app):
    app.cVis = 20
    app.maze = Maze(app.cVis)
    generateMaze(app)
    print("done")

def generateMaze(app):
    while(not app.maze.generateStep()):
        pass

def drawMaze(app, canvas):
    corner = (-100, -100)
    cWidth = app.width / app.cVis
    cHeight = app.height / app.cVis
    for i in range(len(app.maze.cList)):
        for j in range(len(app.maze.cList[i])):
            app.maze.cList[i][j].drawCell(canvas, corner, cWidth, cHeight)

def redrawAll(app, canvas):
    drawMaze(app, canvas)

runApp(width = 500, height = 500)
