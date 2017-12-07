### These functions are for drawing the board

import pygame
import math
from static import *
from gameData import *
from stones import *

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
    
# shows the game's instructions
def drawInstructions(screen):
    pygame.draw.rect(screen, Colors.WHITE, (0, 0, GoConstants.BOARDWIDTH, GoConstants.BOARDHEIGHT))
    pygame.draw.rect(screen, Colors.BLACK, (0, 0, GoConstants.BOARDWIDTH, GoConstants.BOARDHEIGHT), 15)
    text1 = pygame.font.Font(None, 50).render("INSTRUCTIONS", True, (0, 0, 0))
    text2 = pygame.font.Font(None, 42).render("Click PLAY to begin!", True, (0, 0, 0))
    text3 = pygame.font.Font(None, 36).render("While in-game, click on a corner to play a piece", True, (0, 0, 0))
    text4 = pygame.font.Font(None, 36).render("Press 'u' to undo a move", True, (0, 0, 0))
    text5 = pygame.font.Font(None, 36).render("Press 'p' to pass your turn", True, (0, 0, 0))
    text6 = pygame.font.Font(None, 36).render("Press 'r' to reset the game", True, (0, 0, 0))
    text7 = pygame.font.Font(None, 36).render("Press 'i' to pull up these instructions again", True, (0, 0, 0))
    text8 = pygame.font.Font(None, 36).render("The game ends when both players pass turns", True, (0, 0, 0))
    text9 = pygame.font.Font(None, 28).render("(Click anywhere to exit)", True, (0, 0, 0))
    
    screen.blit(text1, (175, 25))
    screen.blit(text2, (25, 125))
    screen.blit(text3, (25, 200))
    screen.blit(text4, (25, 250))
    screen.blit(text5, (25, 300))
    screen.blit(text6, (25, 350))
    screen.blit(text7, (25, 400))
    screen.blit(text8, (25, 450))
    screen.blit(text9, (175, 550))