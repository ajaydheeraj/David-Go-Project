### Stores the stone object and its functions

from static import *

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