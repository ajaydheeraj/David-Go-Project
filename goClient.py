### This is the client
### Much of this code is based on sockets manual on 112 website, by Rohan Varma and Kyle Chin

import socket
import threading
from queue import Queue

def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")

### This is the pygame mainloop, we use this to run the game
### Loop framework created by Lukas Peraza, taken from 112 website

import pygame
from boardFunctions import *
from gameData import *
from static import *
from textBoxes import *
from stones import *

class GoGame(object):

    def init(self):
        self.data = Data()

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        msg = ""
        
        if self.data.start:
            if not self.data.instructionsScreen:
                if Functions.clickInBounds((x, y), PlayButton.bounds):
                    self.data.initGame()
                    msg = "inGame otherStuff\n"
                elif Functions.clickInBounds((x, y), InstructionsButton.bounds):
                    self.data.instructionsScreen = True
                    return

        elif self.data.inGame and not self.data.instructionsScreen and self.data.otherInGame:
            # does text box stuff if there is a text box open
            if self.data.textBox != None:
                # will do different things depending on the text box (which, in
                # turn, appears when a key is pressed
                if Functions.clickInBounds((x, y), GoConstants.YESBOXBOUNDS):
                    if self.data.textBox.action == "start over":
                        msg = "restart otherStuff\n"
                        self.data.initGame()
                    elif self.data.textBox.action == "undo move":
                        msg = "undoMove otherStuff\n"
                        self.data.undoMove()
                    # the game ends when both players pass, otherwise it just
                    # passes the turn onto the next player
                    elif self.data.textBox.action == "pass the turn":
                        msg = "passTurn otherStuff\n"
                        self.data.passTurn(True)
                    elif self.data.textBox.action == "remove dead stones":
                        msg = "readyToRemove otherStuff\n"
                        self.data.textBox = None
                        self.data.removeStones = True
                elif Functions.clickInBounds((x, y), GoConstants.NOBOXBOUNDS):
                    self.data.textBox = None
            
            # in remove-stone mode, clicking on a stone removes it
            elif self.data.removeStones and self.data.otherReadyToRemoveStones:
                msg = "removeStone %d %d\n" % (x, y)
                try:
                    self.data.removeStone(x, y)
                except:
                    pass
            
            # in-game mode, clicking puts down a stone
            else:
                if not self.data.isMyTurn(): return
                self.data.lastTurnPassed = False
                try:
                    row, col = self.data.placeStone(x, y)
                    msg = "piecePlaced %d %d\n" % (x, y)  
                except:
                    self.data.placeStone(x, y)
                
        elif self.data.gameOver:
            self.data.textBox = None
            
        if self.data.instructionsScreen:
            self.data.instructionsScreen = False
            
        # send the message to other players! (Rohan's function)
        if (msg != ""):
            print("sending: ", msg)
            self.server.send(msg.encode())

    def mouseMotion(self, x, y):
        self.data.mousePos = (x, y)

    def mouseDrag(self, x, y):
        pass

    # "r" restarts the game, "u" undoes the previous move
    def keyPressed(self, keyCode, modifier):
        if self.data.start:
            pass
        elif self.data.inGame:
            if self.data.textBox == None and not self.data.removeStones:
                if keyCode == pygame.K_r:
                    self.data.textBox = TextBox("start over")
                elif keyCode == pygame.K_u and not self.data.isMyTurn():
                    self.data.textBox = TextBox("undo move")
                elif keyCode == pygame.K_p and self.data.isMyTurn():
                    self.data.textBox = TextBox("pass the turn")
                elif keyCode == pygame.K_i and self.data.textBox == None:
                    self.data.instructionsScreen = True
            elif self.data.removeStones:
                if keyCode == pygame.K_d:
                    self.data.inGame = False
                    self.data.removeStones = False
                    self.data.gameOver = True
                    self.data.getScore()
                    self.data.textBox = GameOverBox(self.data.p1score, self.data.p2score)
        elif self.data.gameOver:
            if keyCode == pygame.K_r:
                self.data.__init__()

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        # timerFired receives instructions and executes them
            while (self.serverMsg.qsize() > 0):
                msg = self.serverMsg.get(False)
                try:
                    print("received: ", msg, "\n")
                    msg = msg.split()
                    command = msg[0]
                    # print(msg)
                    
                    if command == "myIDis":
                        myPID = msg[1]
                        self.data.me = myPID
                        
                    elif command == "newPlayer":
                        newPID = msg[1]
                        self.data.other = newPID
                        
                    elif command == "inGame":
                        self.data.otherInGame = True
            
                    elif command == "piecePlaced":
                        x, y = int(msg[2]), int(msg[3])
                        self.data.placeStone(x, y)
                        
                    elif command == "restart":
                        self.data.initGame()
                        
                    elif command == "undoMove":
                        self.data.undoMove()
                        
                    elif command == "passTurn":
                        self.data.passTurn(True)
                        if isinstance(self.data.textBox, DeadStoneBox):
                            msg = "gameOver otherStuff \n"
                            print("sending: ", msg)
                            self.server.send(msg.encode())
                        
                    elif command == "gameOver":
                        self.data.playerBox.update(off=True)
                        self.data.textBox = DeadStoneBox("remove dead stones")
                        self.data.lastPlaced = None
                        
                    elif command == "readyToRemove":
                        self.data.otherReadyToRemoveStones = True
                        
                    elif command == "removeStone":
                        x, y = int(msg[2]), int(msg[3])
                        self.data.removeStone(x, y)
                    
                except:
                    print("failed")
                    
                self.serverMsg.task_done()

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
            self.data.playerBox.draw(self.screen)
            if self.data.textBox != None:
                drawTextBox(self.screen, self.data.textBox)
            elif self.data.removeStones:
                pass
            else:
                if self.data.isMyTurn:
                    drawGhost(self.screen, self.data.mousePos, self.data.board, Data.playerColors[self.data.turn])
                drawLastPlacedCircle(self.screen, self.data.lastPlaced)
                
            if not self.data.otherInGame:
                pygame.draw.rect(self.screen, Colors.BLACK, (0, 0, GoConstants.BOARDWIDTH, GoConstants.BOARDHEIGHT))
                text = pygame.font.Font(None, 36).render("Waiting for other player...", True, Colors.WHITE)
                self.screen.blit(text, (275, 100))
              
        # draws a static board with a message displaying which player won over it
        elif self.data.gameOver:
            drawBoard(self.screen)
            drawPieces(self.screen, self.data.board)
            if self.data.textBox != None:
                drawTextBox(self.screen, self.data.textBox)
         
        # creates the instructions screen on top of everything else
        if self.data.instructionsScreen:
            drawInstructions(self.screen)
        
        pygame.display.flip()
                
    # returns whether a specific key is being held
    def isKeyPressed(self, key):
        return self._keys.get(key, False)

    def __init__(self, server=None, serverMsg=None, width=GoConstants.BOARDWIDTH, height=GoConstants.BOARDHEIGHT, fps=50, title="Go"):
        self.server = server
        self.serverMsg = serverMsg
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = GoConstants.BACKGROUND
        pygame.init()

    def run(self):

        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((GoConstants.BOARDWIDTH, GoConstants.BOARDHEIGHT))
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

        pygame.quit()

def main():
    HOST = "128.237.127.38" # my IP address, you need to change this every time
    PORT = 50003
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST,PORT))
    print("connected to server")
    serverMsg = Queue(100)
    threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
    game = GoGame(server, serverMsg)
    game.run()

if __name__ == '__main__':
    main()