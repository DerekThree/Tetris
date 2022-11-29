import pyautogui
import sys
import time

class Board:
    blockWidth = 26
    numColumns = 10
    numRows = 20
    grid = [False] * ((numRows+1) * numColumns) # +1 row, prevent out of bounds
    origin = (0, 0)
    nextPieceNumber = 0
    activePieceNumber = 0

    def findOrigin(self):
        orientPic = 'orient.PNG'
        orientXOffset = 18
        orientYOffset = 45

        origin  = pyautogui.locateOnScreen(orientPic, grayscale=True)
        if origin == None:
            print('Open https://tetris.com/play-tetris')
            print('Press PLAY')
            print('Run main.py')
            sys.exit()

        (x, y, width, height)= origin
        return (x + orientXOffset, y + orientYOffset)

    def findActivePieceNumber(self):
        pieceNumbersByColor = {
            (143, 195, 205): 0,
            (205, 197, 143): 1,
            (189, 143, 205): 2,
            (205, 143, 143): 3,
            (143, 205, 156): 4,
            (205, 177, 143): 5,
            (143, 170, 205): 6,
        }

        for y in range(self.numRows):
            for x in range(self.numColumns):
                xPixel = self.origin[0] + (x * self.blockWidth)
                yPixel = self.origin[1] + (y * self.blockWidth)
                color = pyautogui.pixel(xPixel, yPixel)
                if (color != (0, 0, 0)):
                    return pieceNumbersByColor[color]
        print('Error in getActivePieceNumber')

    def findNextPieceNumber(self):
        xOffset = 375
        yOffset = 90
        pieceNumbersByColor = {
            (0, 114, 127) : 0,
            (149, 142, 67): 1,
            (134, 67, 149): 2,
            (149, 67, 67) : 3,
            (67, 149, 92) : 4,
            (149, 123, 67): 5,
            (67, 112, 149): 6,
        }

        color = pyautogui.pixel(self.origin[0] + xOffset, self.origin[1] + yOffset)
        if color not in pieceNumbersByColor:
            print('Exitting...') # Game Over
            sys.exit()
        return pieceNumbersByColor[color]

    def unpause(self):
        xOffset = 127
        yOffset = 190

        (xOrigin, yOrigin) = self.origin
        pyautogui.click(xOrigin+xOffset, yOrigin+yOffset)
        time.sleep(3)

    def __init__(self):
        pyautogui.PAUSE = 0
        self.origin = self.findOrigin()
        self.unpause()
        self.nextPieceNumber = self.findNextPieceNumber()
        self.activePieceNumber = self.findActivePieceNumber()
        pyautogui.PAUSE = .035

    def move(self, move):
        def clearCompletedLines():
            for y in range(self.numRows):
                 if isLineFilled(y):
                     for index in range((y * self.numColumns) - 1, 0, -1):
                         self.grid[index + self.numColumns] = self.grid[index]

        def isLineFilled(y):
            for x in range(10):
                if not self.grid[y * self.numColumns + x]:
                    return False
            return True

        (orientation, xMove) = move

        # send keystrokes
        for i in range(orientation):
            pyautogui.press('up')
        if (xMove > 0):
            for i in range(xMove):
                pyautogui.press('right')
        else:
            for i in range(-xMove):
                pyautogui.press('left')
        pyautogui.press('space')

        # update grid with new blocks
        newCoords = self.predictCoordsAfterMove(orientation, xMove)
        for coord in newCoords:
            (x, y) = coord
            self.grid[y * self.numColumns + x] = True
        clearCompletedLines()

        # wait for the next piece
        for i in range(16):
            if not self.findNextPieceNumber() == self.nextPieceNumber:
                break
                time.sleep(.01)

        self.activePieceNumber = self.nextPieceNumber
        self.nextPieceNumber = self.findNextPieceNumber()

    def predictCoordsAfterMove(self, orientation, xMove):
        # coordArray[pieceType][orientation][blockNumber]
        numOrientations = 4
        numPiecetypes = 7
        coordArray = [[None for i in range(numOrientations)] for j in range(numPiecetypes)]
        coordArray[0][0] = [(3, 1), (4, 1), (5, 1), (6, 1)]
        coordArray[0][1] = [(5, 0), (5, 1), (5, 2), (5, 3)]
        coordArray[0][2] = [(3, 0), (4, 0), (5, 0), (6, 0)]
        coordArray[0][3] = [(4, 0), (4, 1), (4, 2), (4, 3)]
        coordArray[1][0] = [(4, 0), (5, 0), (4, 1), (5, 1)]
        coordArray[1][1] = [(4, 0), (5, 0), (4, 1), (5, 1)]
        coordArray[1][2] = [(4, 0), (5, 0), (4, 1), (5, 1)]
        coordArray[1][3] = [(4, 0), (5, 0), (4, 1), (5, 1)]
        coordArray[2][0] = [(4, 0), (3, 1), (4, 1), (5, 1)]
        coordArray[2][1] = [(4, 0), (4, 1), (5, 1), (4, 2)]
        coordArray[2][2] = [(3, 1), (4, 1), (5, 1), (4, 2)]
        coordArray[2][3] = [(4, 0), (3, 1), (4, 1), (4, 2)]
        coordArray[3][0] = [(3, 0), (4, 0), (4, 1), (5, 1)]
        coordArray[3][1] = [(5, 0), (4, 1), (5, 1), (4, 2)]
        coordArray[3][2] = [(3, 1), (4, 1), (4, 2), (5, 2)]
        coordArray[3][3] = [(5, 1), (4, 2), (5, 2), (4, 3)]
        coordArray[4][0] = [(4, 0), (5, 0), (3, 1), (4, 1)]
        coordArray[4][1] = [(4, 0), (4, 1), (5, 1), (5, 2)]
        coordArray[4][2] = [(4, 1), (5, 1), (3, 2), (4, 2)]
        coordArray[4][3] = [(3, 0), (3, 1), (4, 1), (4, 2)]
        coordArray[5][0] = [(5, 0), (3, 1), (4, 1), (5, 1)]
        coordArray[5][1] = [(4, 0), (4, 1), (4, 2), (5, 2)]
        coordArray[5][2] = [(3, 1), (4, 1), (5, 1), (3, 2)]
        coordArray[5][3] = [(3, 0), (4, 0), (4, 1), (4, 2)]
        coordArray[6][0] = [(3, 0), (3, 1), (4, 1), (5, 1)]
        coordArray[6][1] = [(4, 0), (5, 0), (4, 1), (4, 2)]
        coordArray[6][2] = [(3, 0), (4, 0), (5, 0), (5, 1)]
        coordArray[6][3] = [(4, 0), (4, 1), (4, 2), (3, 2)]

        # move oriented piece horizontally
        coords = coordArray[self.activePieceNumber][orientation]
        for i in range(4):
            (x, y) = coords[i]
            if x + xMove > 9 or x + xMove < 0:
                return None
            coords[i] = (x + xMove, y)

        # find shortest distance from piece block down to existing block or floor
        minDistance = self.numRows
        for coord in coords:
            (x, y) = coord
            blockPresent = False
            blockYPos = 0
            for blockYPos in range(self.numRows):
                if self.grid[(blockYPos + 1) * self.numColumns + x]:
                    break
            minDistance = min([minDistance, blockYPos - y])

        # add shortest distance to y coords
        for i in range(4):
            (x, y) = coords[i]
            coords[i] = (x, y + minDistance)
        return coords
