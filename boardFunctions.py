### These functions are for drawing the board

import pygame
import math
from static import *
from gameData import *

# for drawing the board
def drawBoard(screen):
    ts = GoConstants.TILESIZE
    margin = GoConstants.MARGIN

    # makes the grid
    for row in range(GoConstants.ROWS):
        for col in range(GoConstants.COLUMNS):
            pygame.draw.rect(screen, Colors.TAN, (margin + col * ts, margin + row * ts, ts, ts))
            pygame.draw.rect(screen, Colors.BLACK, (margin + col * ts, margin + row * ts, ts, ts), 2)

    # makes the dots on the grid
    dotMargin = margin + 3 * ts
    dotDistance = 6 * ts
    for i in range(3):
        for j in range(3):
            centerX = dotMargin + i * dotDistance
            centerY = dotMargin + j * dotDistance
            pygame.draw.circle(screen, Colors.BLACK, (centerX, centerY), 5)

# draws each piece one by one
def drawPieces(screen, board):
    for row in board:
        for corner in row:
            try:
                corner.draw(screen)
            except:
                pass
                
# draws a blue circle showing which piece was last placed
def drawLastPlacedCircle(screen, location):
    if location == None:
        return
    x = GoConstants.MARGIN + location[1] * GoConstants.TILESIZE
    y = GoConstants.MARGIN + location [0] * GoConstants.TILESIZE
    pygame.draw.circle(screen, Colors.LIGHTBLUE, (x, y), Stone.radius, 2)

# draws the ghost piece that follows the mouse, helps the player know where he's clicking
def drawGhost(screen, coords, board, color):
    row, col = Data.closestCorner(coords)
    ghost = Stone(row, col, color)
    ghost.lastPlaced = False
    try:
        check = (math.sqrt(row), math.sqrt(col)) # makes sure it doesn't display for negative rows and columns
        if board[row][col] == None:
            ghost.draw(screen)
    except:
        pass
        
# draws the textbox upon keypressed trigger
def drawTextBox(screen, textBox):
    textBox.draw(screen)
    
# draws the background in the start screen
def drawStartBG(screen):
    image = pygame.image.load("goBG.png")
    background = pygame.transform.scale(image, (GoConstants.BOARDWIDTH, GoConstants.BOARDHEIGHT))
    screen.blit(background, (0, 0))