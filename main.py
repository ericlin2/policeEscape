import math, copy, random
from cmu_112_graphics import *


def gameDimensions():
    # These values are set to the writeup defaults
    cellSize = 40
    return cellSize

def generateGrid(size): 
    grid = []
    for row in range(size):
        tempList1 = [] 
        tempList2 = []
        tempList3 = []
        for col in range(size): 
            tempList1 += [1, 1, 0]
            tempList2 += [1, 1, 0]
            tempList3 += [0, 0, 0]
        grid.append(tempList1)
        grid.append(tempList2)
        grid.append(tempList3)
    for row in grid: 
        row.pop()
    grid.pop()

    #create borders 
    for row in grid: 
        row.insert(0, 0)
        row.insert(0, 1)
        row.append(0)
        row.append(1)

    grid.insert(0, [1] + [0]*(len(grid[0])-2) + [1])
    grid.insert(0, [1]*len(grid[0]))

    grid.append([1] + [0]*(len(grid[0])-2) + [1])
    grid.append([1]*len(grid[0]))

    return grid

def appStarted(app):
    app.board = generateGrid(5)
    app.cellSize = gameDimensions()
    app.rows = len(app.board)
    app.cols = len(app.board[0])

    app.playerPos = [1, 1]
    app.board[app.playerPos[0]][app.playerPos[1]] = 2
    app.playerDirection = None

    #app.timerDelay = 300

def drawBoard(app, canvas): 
    for row in range(app.rows): 
        for col in range(app.cols): 
            drawCell(app, canvas, row, col, app.board[row][col])

def drawCell(app, canvas, row, col, tileStatus): 
    x0 = col*app.cellSize 
    y0 = row*app.cellSize
    x1 = x0 + app.cellSize
    y1 = y0 + app.cellSize
    color = ''
    if(tileStatus == 1): #wall 
        color = 'gray'
    elif(tileStatus == 0): 
        color = 'white'
    elif(tileStatus == 2): 
        color = 'red'
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black')

def timerFired(app):
    app.board[app.playerPos[0]][app.playerPos[1]] = 0
    movePlayer(app, app.playerDirection)
    app.board[app.playerPos[0]][app.playerPos[1]] = 2

def movePlayer(app, direction): 
    if(direction == None): 
        return None
    app.playerPos[0] += direction[0]
    app.playerPos[1] += direction[1]
    if not moveIsLegal(app, [0, 0]): 
        app.playerPos[0] -= direction[0]
        app.playerPos[1] -= direction[1]
        return False
    return True

def moveIsLegal(app, direction): 
    if (app.board[app.playerPos[0]+direction[0]][app.playerPos[1]+direction[1]] 
        == 0): 
        return True
    return False
    
def keyPressed(app, event): 
    if (event.key == 'Left'):
        if moveIsLegal(app, [0, -1]): 
            app.playerDirection = [0, -1]
    elif (event.key == 'Right'): 
        if moveIsLegal(app, [0, 1]): 
            app.playerDirection = [0, 1]
    elif (event.key == 'Down'):
        if moveIsLegal(app, [1, 0]):
            app.playerDirection = [1, 0]
    elif (event.key == 'Up'): 
        if moveIsLegal(app, [-1, 0]):
            app.playerDirection = [-1, 0]

def redrawAll(app, canvas): 
    drawBoard(app, canvas)

def playGame():
    grid = generateGrid(5)
    rows = len(grid)
    cols = len(grid[0])

    cellSize = gameDimensions()
    
    height = rows * cellSize 
    width = cols * cellSize

    runApp(width=width, height=height)

def main():
    playGame()

if __name__ == '__main__':
    main()