from random import randint

class Player: # Abstract Player class
    def __init__(self, name):
        self.name = name
        self.history = []

    def play(self, board):
        pass

    def train(self):
        pass

    def reset(self):
        self.history.clear()

    def reward(self, reward):
        # mise a jour de la recompense
        self.history[-1] = self.history[-1][:2] + (reward,)

    def record_action(self, state, action):
        self.history.append((state, action, 0))

    def __str__(self):
        return self.name

class HumanPlayer(Player):
    def play(self, board):
        while True:
            result = input('> Which position (ex: A0) ? ')
            pos = (ord(result[0]) - 65, int(result[1:]))
            if board.inBounds(pos) and board.isEmpty(pos):
                return pos

        #self.record_action(nbSticks, choice)
        return (None, None)

class RandomPlayer(Player):
    def play(self, board):
        while True:
            pos = (randint(0, board.boardSize - 1), randint(0, board.boardSize - 1))
            if board.isEmpty(pos):
                return pos

        #self.record_action(boardSize, action)
        return (None, None)
