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
            pygame.draw.rect(screen, Colors.TAN, (margin + row * ts, margin + col * ts, ts, ts))
            pygame.draw.rect(screen, Colors.BLACK, (margin + row * ts, margin + col * ts, ts, ts), 2)

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
    lastCorner = None
    for row in board:
        for corner in row:
            if corner != None:
                lastCorner = corner
                corner.draw(screen)
    if (lastCorner != None):
        lastCorner.drawLast(screen)


# draws the ghost piece that follows the mouse, helps the player know where he's clicking
def drawGhost(screen, coords, board, color):
	row, col = Data.closestCorner(coords)
	ghost = Stone(row, col, color)
	try:
		check = (math.sqrt(row), math.sqrt(col)) # makes sure it doesn't display for negative rows and columns
		if board[row][col] == None:
			ghost.draw(screen)
	except:
		pass