from random import randint, uniform

class Player: # Abstract Player class
    def __init__(self, name):
        self.name = name
        self.history = []

    def play(self, nbSticks):
        pass

    def train(self):
        pass

    def reset(self):
        self.history.clear()

    def reward(self, reward):
        # mise a jour de la recompense
        self.history[-1] = self.history[-1][:2] + (reward,)

    def take_action(self, state, action):
        self.history.append((state, action, 0))

    def __str__(self):
        return self.name

class HumanPlayer(Player):
    def play(self, nbSticks):
        choice = None
        while True:
            choice = int(input('> How many sticks [1, 2, 3] ? '))
            if choice in [1, 2, 3]:
                break
        choice = min(choice, nbSticks)

        self.take_action(nbSticks, choice)
        return choice

class RandomPlayer(Player):
    def play(self, nbSticks):
        action = randint(1, min(nbSticks, 3))

        self.take_action(nbSticks, action)
        return action

class TrainedPlayer(Player):
    def __init__(self, name, nbSticks, epsilon, learningRate):
        Player.__init__(self, name) # super constructor
        self.lr = learningRate
        self.epsilon = epsilon

        # value function for each state, initialized with 0
        self.v = {}
        for i in range(nbSticks):
            self.v[i + 1] = 0

    def play(self, nbSticks):
        action = None
        # end of the game, no choice
        if nbSticks == 1:
            action = 1
        elif uniform(0, 1) < self.epsilon:
            # take random action (exploration)
            action = randint(1, min(nbSticks, 3))
        else:
            # take greedy action (exploitation)
            actions = {}
            for i in range(1, min(nbSticks, 3) + 1):
                if nbSticks - i > 0:
                    actions[i] = self.v[nbSticks - i]
            action = min(actions, key = lambda k: actions[k])

        self.take_action(nbSticks, action)
        return action

    def train(self):
        # update value function
        for i, (s, a, r) in enumerate(self.history[::-1]):
            if i == 0:
                self.v[s] = self.v[s] + self.lr * (r - self.v[s])
            else:
                next = len(self.history) - i
                self.v[s] = self.v[s] + self.lr * (self.v[self.history[next][0]] - self.v[s])
