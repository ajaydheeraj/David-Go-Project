### This will hold game data

import pygame
import copy
from static import *

# game data is stored here
class Data(object):
	playerColors = {1: Colors.BLACK, 2: Colors.WHITE}

	# initializes data
	def __init__(self):
		self.board = self.initBoard()
		self.oldBoard = copy.deepcopy(self.board)
		self.turn = 1
		self.mousePos = (0, 0)
		self.gameOver = False

	# creates a 19x19 board of "Nones"
	@staticmethod
	def initBoard():
		board = []
		for i in range(GoConstants.COLUMNS+1):
			row = []
			for j in range(GoConstants.ROWS+1):
				row.append(None)
			board.append(row)
		return board

	# adds a stone to the board based on where the player clicked
	def placeStone(self, x, y):
		row, col = self.closestCorner(x, y)
		if row < 0 or col < 0 or row > GoConstants.ROWS or col > GoConstants.COLUMNS:
			return "Not on board!"
		
		if self.turn == 1:
			color = Colors.BLACK
		elif self.turn == 2:
			color = Colors.WHITE
		if self.board[row][col] == None:
			self.oldBoard = copy.deepcopy(self.board)
			self.board[row][col] = Stone(row, col, color)
			self.updateBoard()
			
			self.passTurn()

	# your closestCorner function, just moved to a different place and slightly modified to return row and col
	@staticmethod
	def closestCorner(*args):
		# the case if a tuple of coordinates is inputted instead of an x and a y
		if len(args) == 1:
			args = args[0]

		(x, y) = args
		row = Functions.round((y - GoConstants.MARGIN) / GoConstants.TILESIZE)
		col = Functions.round((x - GoConstants.MARGIN) / GoConstants.TILESIZE)
		return row, col

	# changes from player 1 to player 2
	def passTurn(self):
		self.turn = 3 - self.turn
		for row in self.board:
			for corner in row:
				if corner != None:
					corner.wasChecked = False

	# updates the board (removes any pieces that have been captured)
	def updateBoard(self):
		for row in self.board:
			for corner in row:
				if corner != None and corner.color == self.playerColors[3 - self.turn]: # only check the other players' pieces
					self.board = corner.updatePiece(self.board)

	# if a player presses "u", they will get their turn back
	def undoMove(self):
		if self.board == self.oldBoard:
			return
		self.board = self.oldBoard
		self.passTurn()

# the stone object
class Stone(object):
	radius = 13

	def __init__(self, row, column, color):
		self.row = row
		self.col = column
		self.color = color
		self.center = self.getCenter()
		self.wasChecked = False

	# this was just used for debugging purposes
	def __repr__(self):
		color = Colors.index[self.color]
		return color + "stone on (%d, %d)" % (self.col, self.row)

	# gets the center of the piece from the row and the column
	def getCenter(self):
		centerX = GoConstants.MARGIN + self.col * GoConstants.TILESIZE
		centerY = GoConstants.MARGIN + self.row * GoConstants.TILESIZE

		return (centerX, centerY)

	# tells python how to draw the piece
	def draw(self, screen):
		pygame.draw.circle(screen, self.color, self.center, self.radius)

	# checks if the piece should be removed
	def updatePiece(self, board):
		# if the piece has been checked, go back
		if self.wasChecked:
			return board

		group = [(self.row, self.col)]

		# recursively checks if the group that the piece is in is surrounded
		def checkIfSurrounded(color, board, coords, fromDirection=None):
			isSurrounded = True
			(row, col) = coords
			
			# first, it checks if the piece is on the top edge. If it is, it leaves isSurrounded as is and passes
			# then, if one corner up from this piece is an empty space, then it is not surrounded
			# otherwise, if it is a piece of the same color, it needs to recurse and check the next one
			# lastly, if it is a piece of the opposite color, it leaves isSurrounded as is and passes, similar to the edge
			# all of the directions work this way; it never checks the directions from which it came (because that would be stupid)
			if fromDirection != "Up":
				if row - 1 >= 0:
					check = board[row-1][col]
					if check == None:
						isSurrounded = False
					elif check.color == color and (check.row, check.col) not in group:
						group.append((check.row, check.col))
						isSurrounded = checkIfSurrounded(color, board, (row-1, col), "Down")

			if fromDirection != "Down" and isSurrounded:
				if row + 1 <= GoConstants.ROWS:
					check = board[row+1][col]
					if check == None:
						isSurrounded = False
					elif check.color == color and (check.row, check.col) not in group:
						group.append((check.row, check.col))
						isSurrounded = checkIfSurrounded(color, board, (row+1, col), "UP")

			if fromDirection != "Left" and isSurrounded:
				if col - 1 >= 0:
					check = board[row][col-1]
					if check == None:
						isSurrounded = False
					elif check.color == color and (check.row, check.col) not in group:
						group.append((check.row, check.col))
						isSurrounded = checkIfSurrounded(color, board, (row, col-1), "Right")

			if fromDirection != "Right" and isSurrounded:
				if col + 1 <= GoConstants.COLUMNS:
					check = board[row][col+1]
					if check == None:
						isSurrounded = False
					elif check.color == color and (check.row, check.col) not in group:
						group.append((check.row, check.col))
						isSurrounded = checkIfSurrounded(color, board, (row, col+1), "Left")

			return isSurrounded

		# checks if the stone (and the group that it's in) is surrounded, and acts accordingly
		if checkIfSurrounded(self.color, board, (self.row, self.col)):
			# if they're surrounded, they get removed
			for coords in group:
				board[coords[0]][coords[1]] = None
		else: # otherwise, they get marked as checked for the turn
			for coords in group:
				stone = board[coords[0]][coords[1]]
				stone.wasChecked = True

		return board