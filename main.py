### This is the mainloop, we use this to run the game

import pygame
from boardFunctions import *
from gameData import *
from static import *


class GoGame(object):

    def init(self):
        self.data = Data()

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        self.data.placeStone(x, y)
        pygame.mixer.music.load('click_sound.wav')
        pygame.mixer.music.play()
        pygame.mixer.music.get_volume()

    def mouseMotion(self, x, y):
        self.data.mousePos = (x, y)

    def mouseDrag(self, x, y):
        pass

	# "r" restarts the game, "u" undoes the previous move
    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_r:
        	self.data.__init__()
        elif keyCode == pygame.K_u:
        	self.data.undoMove()

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    # draws the board, then the pieces, then the ghost piece that follows the mouse
    def redrawAll(self):
        drawBoard(self.screen)
        drawPieces(self.screen, self.data.board)
        drawGhost(self.screen, self.data.mousePos, self.data.board, Data.playerColors[self.data.turn])

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