### This is the mainloop, we use this to run the game

import pygame
from boardFunctions import *
from gameData import *
from static import *
from textBoxes import *


class GoGame(object):

    def init(self):
        self.data = Data()

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        if self.data.start:
            if Functions.clickInBounds((x, y), PlayButton.bounds):
                self.data.start = False
                self.data.inGame = True
        elif self.data.inGame:
            
            # does text box stuff if there is a text box open
            if self.data.textBox != None:
                if Functions.clickInBounds((x, y), GoConstants.YESBOXBOUNDS):
                    if self.data.textBox.action == "start over":
                        self.data.board = self.data.initBoard()
                    elif self.data.textBox.action == "undo move":
                        self.data.undoMove()
                    elif self.data.textBox.action == "pass the turn":
                        self.data.passTurn()
                    self.data.textBox = None
                elif Functions.clickInBounds((x, y), GoConstants.NOBOXBOUNDS):
                    self.data.textBox = None
            
            else:
                self.data.placeStone(x, y)

    def mouseMotion(self, x, y):
        self.data.mousePos = (x, y)

    def mouseDrag(self, x, y):
        pass

    # "r" restarts the game, "u" undoes the previous move
    def keyPressed(self, keyCode, modifier):
        if self.data.start:
            pass
        elif self.data.inGame:
            if self.data.textBox == None:
                if keyCode == pygame.K_r:
                    self.data.textBox = TextBox("start over")
                elif keyCode == pygame.K_u:
                    self.data.textBox = TextBox("undo move")
                elif keyCode == pygame.K_p:
                    self.data.textBox = TextBox("pass the turn")

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    # draws the board, then the pieces, then the ghost piece that follows the mouse
    def redrawAll(self):
        # draws the start screen
        if self.data.start:
            drawStartBG(self.screen)
            for button in self.data.startButtons:
                button.draw(self.screen)
                
        # draws the game screen, board, pieces, etc
        elif self.data.inGame:
            drawBoard(self.screen)
            drawPieces(self.screen, self.data.board)
            if self.data.textBox == None:
                drawGhost(self.screen, self.data.mousePos, self.data.board, Data.playerColors[self.data.turn])
            else:
                drawTextBox(self.screen, self.data.textBox)

    # returns whether a specific key is being held
    def isKeyPressed(self, key):
        return self._keys.get(key, False)

    def __init__(self, width=GoConstants.BOARDWIDTH, height=GoConstants.BOARDHEIGHT, fps=50, title="Go"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = GoConstants.BACKGROUND
        pygame.init()

    def run(self):

        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        self.screen.fill(self.bgColor)
        self.redrawAll()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            self.screen.fill(self.bgColor)
            self.redrawAll()
            pygame.display.flip()

        pygame.quit()

def main():
    game = GoGame()
    game.run()

if __name__ == '__main__':
    main()