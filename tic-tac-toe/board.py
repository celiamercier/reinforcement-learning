from tupleUtils import sumTuples, subTuples, absTuple

class Board:
    def __init__(self, boardSize):
        # 0: empty
        # 1: player 1
        # 2: player 2
        self.winningMarkNumber = 3
        self.boardSize = boardSize
        self.board = [[ 0 for i in range(boardSize) ] for j in range(boardSize)]

    def set(self, player, pos):
        self.board[pos[0]][pos[1]] = player

    def isEmpty(self, pos):
        return self.board[pos[0]][pos[1]] == 0

    def isFull(self):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j] == 0:
                    return False
        return True

    def hasWon(self, player, action):
        res = self.__validateMarks(self.__browseMarks(player, action, (-1,0)), self.__browseMarks(player, action, (1,0)))
        res = res or self.__validateMarks(self.__browseMarks(player, action, (0,-1)), self.__browseMarks(player, action, (0,1)))
        res = res or self.__validateMarks(self.__browseMarks(player, action, (-1,-1)), self.__browseMarks(player, action, (1,1)))
        res = res or self.__validateMarks(self.__browseMarks(player, action, (-1,1)), self.__browseMarks(player, action, (1,-1)))
        return res

    def inBounds(self, pos):
        i, j = pos
        return i >= 0 and j >= 0 and i < self.boardSize and j < self.boardSize

    def display(self):
        # 0,1,2...
        for j in range(self.boardSize + 1):
            if j == 0:
                print(' ', end=' ')
            else:
                print(j - 1, end=' ')
        print()
        for i in range(self.boardSize):
            for j in range(self.boardSize + 1):
                # A,B,C...
                if j == 0:
                    print(chr(65 + i), end=' ')
                else:
                    self.__printCase((i, j-1))
            print()

    def __browseMarks(self, player, pos, dir):
        next = pos
        while self.board[next[0]][next[1]] == player:
            pos = next
            next = sumTuples(pos, dir)
            if not self.inBounds(next):
                break
        return pos

    def __validateMarks(self, fromPos, toPos):
        dist = absTuple(subTuples(toPos, fromPos))
        if dist[0] == 0 and dist[1] == self.winningMarkNumber - 1:
            return True
        elif dist[1] == 0 and dist[0] == self.winningMarkNumber - 1:
            return True
        elif dist[0] == self.winningMarkNumber - 1 and dist[1] == self.winningMarkNumber - 1:
            return True
        return False

    def __printCase(self, pos):
        if self.isEmpty(pos):
            print(' ', end=' ')
        elif self.board[pos[0]][pos[1]] == 1:
            print('X', end=' ')
        else:
            print('0', end=' ')
