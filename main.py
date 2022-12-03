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
    app.board = generateGrid(6)
    app.cellSize = gameDimensions()
    app.rows = len(app.board)
    app.cols = len(app.board[0])
    app.score = 0 

    app.playerPos = [1, 1]
    app.board[app.playerPos[0]][app.playerPos[1]] = 2
    app.playerDirection = None

    app.player_cx = app.playerPos[1]*app.cellSize + app.cellSize/2
    app.player_cy = app.playerPos[0]*app.cellSize + app.cellSize/2
    app.playerDirectionSmooth = None
    app.animationProgress = 0

    app.police1 = [app.rows - 2, app.cols -2]
    app.board[app.police1[0]][app.police1[1]] = 3
    app.police1_direction = None

    app.police1_cx = app.police1[1]*app.cellSize + app.cellSize/2
    app.police1_cy = app.police1[0]*app.cellSize + app.cellSize/2
    app.police1DirectionSmooth = None

    app.police2 = [app.rows - 2, 1]
    app.board[app.police2[0]][app.police2[1]] = 3
    app.police2_direction = None

    app.police2_cx = app.police2[1]*app.cellSize + app.cellSize/2
    app.police2_cy = app.police2[0]*app.cellSize + app.cellSize/2
    app.police2DirectionSmooth = None

    app.police3 = [1, app.cols - 2]
    app.board[app.police3[0]][app.police3[1]] = 3
    app.police3_direction = None

    app.police3_cx = app.police3[1]*app.cellSize + app.cellSize/2
    app.police3_cy = app.police3[0]*app.cellSize + app.cellSize/2
    app.police3DirectionSmooth = None

    app.powerup = spawnPowerups(app) 
    app.board[app.powerup[0]][app.powerup[1]] = 4

    app.isGameOver = False
    app.timerDelay = 10

##### POWERUP SPAWN #####
def spawnPowerups(app): 
    row = random.randint(0, app.rows - 1)
    col = random.randint(0, app.cols - 1)
    if(app.board[row][col] == 0): 
        return [row, col]
    else: 
        return spawnPowerups(app)

##### DRAW FUNCTIONS #####

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
    elif(tileStatus == 4): 
        color = 'green'
    else: 
        color = 'white'
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black')

def drawScore(app, canvas): 
    canvas.create_text(app.width/2, app.cellSize/2, fill="black", 
         text= f"Score: {int(app.score//1)}", font=('Helvetica','20','bold'))
    
def drawGameOver(app, canvas): 
    canvas.create_text(app.width/2, app.height/2, fill="black", 
         text= f"Game Over", font=('Helvetica','40','bold'))

##### PLAYER DRAW FUNCTION (smooth) #####
def drawPlayerSmooth(app, canvas): 
    x0 = app.player_cx - app.cellSize/2
    y0 = app.player_cy - app.cellSize/2 
    x1 = app.player_cx + app.cellSize/2
    y1 = app.player_cy + app.cellSize/2
    canvas.create_rectangle(x0, y0, x1, y1, fill='red', outline='black')

#### UPDATE PLAYER LOCATION (smooth) #####
def movePlayerSmooth(app, direction): 
    if direction == None: 
        return None
    app.player_cx += direction[1]*2.5
    app.player_cy += direction[0]*2.5

    if not moveIsLegal(app, [0,0]): 
        app.player_cx -= direction[1]*2.5
        app.player_cy -= direction[0]*2.5

##### POLICE DRAW FUNCTIONS (smooth) #####
def drawPolice1Smooth(app, canvas): 
    x0 = app.police1_cx - app.cellSize/2
    y0 = app.police1_cy - app.cellSize/2 
    x1 = app.police1_cx + app.cellSize/2
    y1 = app.police1_cy + app.cellSize/2
    canvas.create_rectangle(x0, y0, x1, y1, fill='black', outline='black')

def drawPolice2Smooth(app, canvas): 
    x0 = app.police2_cx - app.cellSize/2
    y0 = app.police2_cy - app.cellSize/2 
    x1 = app.police2_cx + app.cellSize/2
    y1 = app.police2_cy + app.cellSize/2
    canvas.create_rectangle(x0, y0, x1, y1, fill='black', outline='black')

def drawPolice3Smooth(app, canvas): 
    x0 = app.police3_cx - app.cellSize/2
    y0 = app.police3_cy - app.cellSize/2 
    x1 = app.police3_cx + app.cellSize/2
    y1 = app.police3_cy + app.cellSize/2
    canvas.create_rectangle(x0, y0, x1, y1, fill='black', outline='black')

##### UPDATE POLICE POSITION (SMOOTH) #####
def movePolice1Smooth(app, direction): 
    if direction == None: 
        return None
    app.police1_cx += direction[1]*2
    app.police1_cy += direction[0]*2

def movePolice2Smooth(app, direction): 
    if direction == None: 
        return None
    app.police2_cx += direction[1]*2
    app.police2_cy += direction[0]*2

def movePolice3Smooth(app, direction): 
    if direction == None: 
        return None
    app.police3_cx += direction[1]*2
    app.police3_cy += direction[0]*2

def windowToGrid(app, cx, cy): # convert smooth location to grid location 
    return [((cy - app.cellSize/2)/app.cellSize), ((cx - app.cellSize/2)/app.cellSize)]

def timerFired(app):
    if app.isGameOver == False: 
        
        # player moving
        app.board[app.playerPos[0]][app.playerPos[1]] = 0
        if(windowToGrid(app, app.player_cx, app.player_cy) == app.playerPos): 
            movePlayer(app, app.playerDirection)
            app.playerDirectionSmooth = app.playerDirection

            # pick up powerup
            if app.board[app.playerPos[0]][app.playerPos[1]] == 4: 
                app.score += 100
                app.powerup = spawnPowerups(app) 
                app.board[app.powerup[0]][app.powerup[1]] = 4

            app.board[app.playerPos[0]][app.playerPos[1]] = 2
        movePlayerSmooth(app, app.playerDirectionSmooth)

        #police1 moving 
        app.board[app.police1[0]][app.police1[1]] = 0
        if(windowToGrid(app, app.police1_cx, app.police1_cy) == app.police1): 
            movePolice1(app)
            app.police1DirectionSmooth = app.police1_direction     
            app.board[app.police1[0]][app.police1[1]] = 3
        movePolice1Smooth(app, app.police1DirectionSmooth)

        #police2 moving 
        app.board[app.police2[0]][app.police2[1]] = 0
        if(windowToGrid(app, app.police2_cx, app.police2_cy) == app.police2): 
            movePolice2(app)
            app.police2DirectionSmooth = app.police2_direction     
            app.board[app.police2[0]][app.police2[1]] = 3
        movePolice2Smooth(app, app.police2DirectionSmooth)

        #police3 moving 
        app.board[app.police3[0]][app.police3[1]] = 0
        if(windowToGrid(app, app.police3_cx, app.police3_cy) == app.police3): 
            movePolice3(app)
            app.police3DirectionSmooth = app.police3_direction     
            app.board[app.police3[0]][app.police3[1]] = 3
        movePolice3Smooth(app, app.police3DirectionSmooth)

        # score 
        app.score += 0.1
        if(checkIfCaught(app)): 
            app.isGameOver = True 

##### PLAYER FUNCTIONS (unsmooth) #####
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
        == 0 or 
        app.board[app.playerPos[0]+direction[0]][app.playerPos[1]+direction[1]]
        == 4): 
        return True
    return False

##### PLAYAER CONTROLS #####

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

##### POLICE FUNCTIONS (pathfinding) #####
def policeHeuristics(app, police): # a* cost for surrounding tiles of police
    row = police[0]
    col = police[1]
    moves = {"left":[row, col-1], "right":[row, col+1], "up":[row+1, col], "down":[row-1, col]}
    heuristics = dict()

    for move in moves:  
        if(app.board[moves[move][0]][moves[move][1]] == 0): 
            heuristics[move]=(math.sqrt
                    ((moves[move][0]-app.playerPos[0])**2
                    + (moves[move][1] - app.playerPos[1])**2))

    return heuristics

def getPoliceDirection(app, police): 
    heuristics = policeHeuristics(app, police)
    if len(heuristics) == 0: # no possible moves 
        return None
    # elif isRandomZone(app, police): # within 4 tiles = random police direction
    #     possibleDirections = []
    #     for direction in heuristics: 
    #         possibleDirections.append(direction)
    #     randDirection = random.randint(0, len(possibleDirections)-1)
    #     return possibleDirections[randDirection]
    else: 
        bestHeuristic = None
        bestDirection = None
        for direction in heuristics: 
            if bestHeuristic == None: 
                bestHeuristic = heuristics[direction]
                bestDirection = direction
            elif heuristics[direction] < bestHeuristic: 
                bestHeuristic = heuristics[direction]
                bestDirection = direction
        return bestDirection #returns 'left'/'right'/'up'/'down'

def isRandomZone(app, police): #experimental random zone (not used)
    policeX = police[0]
    policeY = police[1] 
    playerX = app.playerPos[0]
    playerY = app.playerPos[1]
    if(math.sqrt((policeX - playerX)**2 + (policeY - playerY)**2) <= 4): 
        return True
    return False

##### UPDATE POLICE POSITION (UNSMOOTH) *used for pathfinding #####
def movePolice1(app): 
    direction = getPoliceDirection(app, app.police1)
    if direction == "left": 
        app.police1_direction = [0, -1]
    elif direction == "right": 
        app.police1_direction = [0, 1]
    elif direction == "up":
        app.police1_direction = [1, 0] 
    elif direction == "down": 
        app.police1_direction = [-1, 0] 
    elif direction == None: 
        app.police1_direction = [0, 0] 
    app.police1[0] += app.police1_direction[0]
    app.police1[1] += app.police1_direction[1]

def movePolice2(app): 
    direction = getPoliceDirection(app, app.police2)
    if direction == "left": 
        app.police2_direction = [0, -1]
    elif direction == "right": 
        app.police2_direction = [0, 1]
    elif direction == "up":
        app.police2_direction = [1, 0] 
    elif direction == "down": 
        app.police2_direction = [-1, 0] 
    elif direction == None: 
        app.police2_direction = [0, 0] 
    app.police2[0] += app.police2_direction[0]
    app.police2[1] += app.police2_direction[1]

def movePolice3(app): 
    direction = getPoliceDirection(app, app.police3)
    if direction == "left": 
        app.police3_direction = [0, -1]
    elif direction == "right": 
        app.police3_direction = [0, 1]
    elif direction == "up":
        app.police3_direction = [1, 0] 
    elif direction == "down": 
        app.police3_direction = [-1, 0] 
    elif direction == None: 
        app.police3_direction = [0, 0] 
    app.police3[0] += app.police3_direction[0]
    app.police3[1] += app.police3_direction[1]

##### GAME OVER #####
def checkIfCaught(app): # caught = police is less than 1 tile dist from player 
 
    #caught by police1
    if(math.sqrt((app.player_cx - app.police1_cx)**2 + (app.player_cy - 
        app.police1_cy)**2) <= app.cellSize): 
        return True 

    #caught by police2
    if(math.sqrt((app.player_cx - app.police2_cx)**2 + (app.player_cy - 
        app.police2_cy)**2) <= app.cellSize): 
        return True 

    #caught by police3
    if(math.sqrt((app.player_cx - app.police3_cx)**2 + (app.player_cy - 
        app.police3_cy)**2) <= app.cellSize): 
        return True 
    
    return False

def redrawAll(app, canvas): 
    drawBoard(app, canvas)

    drawPlayerSmooth(app, canvas)
    drawPolice1Smooth(app, canvas)
    drawPolice2Smooth(app, canvas)
    drawPolice3Smooth(app, canvas)

    drawScore(app, canvas)
    if app.isGameOver: 
        drawGameOver(app, canvas)

def playGame():
    grid = generateGrid(6)
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