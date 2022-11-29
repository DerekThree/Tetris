from board import Board

board = Board()

def getBestMove():

    def getGapScore(coords):
        for coord in coords:
            (x, y) = coord
            if not (y == 19 or board.grid[(y + 1) * board.numColumns + x] or (x, y+1) in coords):
                return 0
        return 20

    def getPositionScore(coords):
        maxY = 0

        for coord in coords:
            (x, y) = coord
            if y > maxY:
                maxY = y
        return maxY * 10

    bestMove = (0, 0)
    bestMoveScore = 0

    for orientation in range(4):
        for i in range(12):
            xMove = i - 6
            moveScore = 0
            newCoords = board.predictCoordsAfterMove(orientation, xMove)
            if newCoords == None: # out of bounds
                continue
            moveScore += getGapScore(newCoords)
            moveScore += getPositionScore(newCoords)
            if moveScore > bestMoveScore:
                bestMove = (orientation, xMove)
                bestMoveScore = moveScore
    return bestMove

def main():
    while(True):
        board.move(getBestMove())

if __name__ == '__main__':
    main()
