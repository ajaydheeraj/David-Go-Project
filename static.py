### used to define constants that I'll use in my code

import pygame
import decimal

# just a place to store colors that I'm using
class Colors(object):
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	TAN = (210, 180, 140)
	FERNGREEN = (79, 121, 66)
	LIGHTBLUE = (0,128,255)
	index = {
		(0, 0, 0): "BLACK", 
		(255, 255, 255): "WHITE",
		(210, 180, 140): "TAN",
		(79, 121, 66): "FERNGREEN",
		(0, 128, 255): "LIGHTBLUE"
		}

# contains functions that I think might be pretty common and idk where else to put them
class Functions(object):

	# rounds with ties going away from zero, borrowed from 112 website
	@staticmethod
	def round(n):
		rounding = decimal.ROUND_HALF_UP
		return int(decimal.Decimal(n).to_integral_value(rounding=rounding))

	# again, borrowed from 112 website; used solely for testing
	@staticmethod
	def print2dList(a):

		if (a == []):
			# So we don't crash accessing a[0]
			print([])
			return
		rows = len(a)
		cols = len(a[0])

		# Helper function for print2dList.
		# This finds the maximum length of the string
		# representation of any item in the 2d list
		def maxItemLength(a):
			maxLen = 0
			rows = len(a)
			cols = len(a[0])
			for row in range(rows):
				for col in range(cols):
					maxLen = max(maxLen, len(str(a[row][col])))
			return maxLen

		fieldWidth = maxItemLength(a)
		print("[ ", end="")
		for row in range(rows):
			if (row > 0): print("\n  ", end="")
			print("[ ", end="")
			for col in range(cols):
				if (col > 0): print(", ", end="")
				# The next 2 lines print a[row][col] with the given fieldWidth
				formatSpec = "%" + str(fieldWidth) + "s"
				print(formatSpec % str(a[row][col]), end="")
			print(" ]", end="")
		print("]")
	
	# checks whether a click is within rectangular bounds
	@staticmethod
	def clickInBounds(mousePos, bounds):
		if mousePos[0] < bounds[0] or mousePos[0] > (bounds[0] + bounds[2]):
			return False
		if mousePos[1] < bounds[1] or mousePos[1] > (bounds[1] + bounds[3]):
			return False
		return True

# constants that might be necessary for the board, pieces, etc.
class GoConstants(object):
	BOARDWIDTH = 800
	BOARDHEIGHT = 600
	ROWS = 18
	COLUMNS = 18
	MARGIN = 30
	TILESIZE = 30
	BACKGROUND = Colors.FERNGREEN
	YESBOXBOUNDS = (75, 325, 100, 50)
	NOBOXBOUNDS = (375, 325, 100, 50)
	DIRECTIONS = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}