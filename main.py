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

    app.police1 = [app.rows - 2, app.cols -2]
    app.board[app.police1[0]][app.police1[1]] = 3
    app.police1_direction = None

    app.police2 = [app.rows - 2, 1]
    app.board[app.police2[0]][app.police2[1]] = 3
    app.police2_direction = None

    app.police3 = [1, app.cols - 2]
    app.board[app.police3[0]][app.police3[1]] = 3
    app.police3_direction = None

    app.powerup = spawnPowerups(app) 
    app.board[app.powerup[0]][app.powerup[1]] = 4

    app.isGameOver = False
    app.timerDelay = 300

# powerup 
def spawnPowerups(app): 
    row = random.randint(0, app.rows - 1)
    col = random.randint(0, app.cols - 1)
    if(app.board[row][col] == 0): 
        return [row, col]
    else: 
        return spawnPowerups(app)

# visualizers 
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
    elif(tileStatus == 3): 
        color = 'black'
    elif(tileStatus == 4): 
        color = 'green'
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black')

def drawScore(app, canvas): 
    canvas.create_text(app.width/2, app.cellSize/2, fill="black", 
         text= f"Score: {app.score}", font=('Helvetica','20','bold'))
    
def drawGameOver(app, canvas): 
    canvas.create_text(app.width/2, app.height/2, fill="black", 
         text= f"Game Over", font=('Helvetica','40','bold'))

# player movement 
def timerFired(app):
    if app.isGameOver == False: 
        # player moving
        app.board[app.playerPos[0]][app.playerPos[1]] = 0
        movePlayer(app, app.playerDirection)

        # pickup powerup
        if app.board[app.playerPos[0]][app.playerPos[1]] == 4: 
            app.score += 100
            app.powerup = spawnPowerups(app) 
            app.board[app.powerup[0]][app.powerup[1]] = 4
        app.board[app.playerPos[0]][app.playerPos[1]] = 2

        #police1 moving 
        app.board[app.police1[0]][app.police1[1]] = 0
        movePolice1(app)
        app.board[app.police1[0]][app.police1[1]] = 3

        #police2 moving 
        app.board[app.police2[0]][app.police2[1]] = 0
        movePolice2(app)
        app.board[app.police2[0]][app.police2[1]] = 3

        #police3 moving
        app.board[app.police3[0]][app.police3[1]] = 0
        movePolice3(app)
        app.board[app.police3[0]][app.police3[1]] = 3

        # score 
        app.score += 5
        if(checkIfCaught(app)): 
            app.isGameOver = True 
    #print(app.isGameOver)

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

# police movement 
def policeHeuristics(app, police): 
    row = police[0]
    col = police[1]
    moves = {"left":[row, col-1], "right":[row, col+1], "up":[row+1, col], "down":[row-1, col]}
    #moves = [[y, x+1], [y, x-1], [y+1, x], [y-1, x]]
    heuristics = dict()

    for move in moves:  
        #print(moves[move][0])
        #print(moves[move][1])
        #print(app.board[moves[move][0]][moves[move][1]])
        if(app.board[moves[move][0]][moves[move][1]] == 0): 
            heuristics[move]=(math.sqrt
                    ((moves[move][0]-app.playerPos[0])**2
                    + (moves[move][1] - app.playerPos[1])**2))
    
    #print(heuristics)
    return heuristics

def getPoliceDirection(app, police): 
    heuristics = policeHeuristics(app, police)
    if len(heuristics) == 0: # no possible moves 
        return None
    elif isRandomZone(app, police): # within 4 tiles = random police direction
        possibleDirections = []
        for direction in heuristics: 
            possibleDirections.append(direction)
        randDirection = random.randint(0, len(possibleDirections)-1)
        return possibleDirections[randDirection]
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
        return bestDirection

def isRandomZone(app, police): 
    policeX = police[0]
    policeY = police[1] 
    playerX = app.playerPos[0]
    playerY = app.playerPos[1]
    if(math.sqrt((policeX - playerX)**2 + (policeY - playerY)**2) <= 4): 
        return True
    return False

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

# game over 
def checkIfCaught(app): # caught = police is in a neighboring tile to player 
    row = app.playerPos[0]
    col = app.playerPos[1]
    surroundingTiles = {(row+1, col), (row-1, col), (row, col+1), (row, col-1)}
    for tile in surroundingTiles: 
        if app.board[tile[0]][tile[1]] == 3: 
            return True
    return False
    # if(abs(app.playerPos[0] - app.police1[0]) <= 1 and 
    #     abs(app.playerPos[1] - app.police1[1]) <= 1): 
    #     return True 
    #return False

def redrawAll(app, canvas): 
    drawBoard(app, canvas)
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