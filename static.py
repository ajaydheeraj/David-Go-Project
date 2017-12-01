### used to define constants that we'll use in our code

import pygame
import decimal


# just a place to store colors that we're using
class Colors(object):
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	TAN = (210, 180, 140)
	FERNGREEN = (79, 121, 66)
	BORDER = (0,128,255)
	index = {
		(0, 0, 0): "Black", 
		(255, 255, 255): "White",
		(210, 180, 140): "Tan",
		(79, 121, 66): "FernGreen",
		(0,128,255): "BORDER"
		}

# contains functions that I think might be pretty common and idk where else to put them
class Functions(object):

	# this function straight up stolen from 112 class
	# rounds with ties going away from zero
	@staticmethod
	def round(n):
		rounding = decimal.ROUND_HALF_UP
		return int(decimal.Decimal(n).to_integral_value(rounding=rounding))

	# again, ripped from 112; used solely for testing
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

# constants we might need for the board, pieces, etc.
class GoConstants(object):
	BOARDWIDTH = 600
	BOARDHEIGHT = 600
	ROWS = 18
	COLUMNS = 18
	MARGIN = 30
	TILESIZE = 30
	BACKGROUND = Colors.FERNGREEN