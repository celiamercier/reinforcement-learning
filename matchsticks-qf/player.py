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

    def record_action(self, state, action):
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

        self.record_action(nbSticks, choice)
        return choice

class RandomPlayer(Player):
    def play(self, nbSticks):
        action = randint(1, min(nbSticks, 3))

        self.record_action(nbSticks, action)
        return action

class TrainedPlayer(Player):
    def __init__(self, name, nbSticks, epsilon, learningRate, gamma):
        Player.__init__(self, name) # super constructor
        self.epsilon = epsilon
        self.lr = learningRate
        self.gamma = gamma

        # Q-table, initialized with 0
        self.q = {}
        for i in range(nbSticks):
            self.q[i + 1] = [0,0,0]

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
            action = self.greedy_action(nbSticks)

        self.record_action(nbSticks, action)
        return action

    def greedy_action(self, nbSticks):
        if nbSticks <= 0:
            return None

        a, maxq = (None, None)
        for i in range(0, min(nbSticks, 3)):
            if maxq is None or self.q[nbSticks][i] > maxq:
                maxq = self.q[nbSticks][i]
                a = i
        return a + 1

    def update(self, end):
        if len(self.history) == 1:
            return

        (st, at, r) = self.history[-1]; # last state
        (p_st, p_at, p_r) = self.history[-2]; # second to last state

        # update Q-table
        if end:
            qt = self.q[st][at-1]
            self.q[st][at-1] = qt + self.lr * (r - qt)
        else:
            max_at = self.greedy_action(st) # best action from the last state
            qt_max = self.q[st][max_at-1]
            p_qt = self.q[p_st][p_at-1]
            self.q[p_st][p_at-1] = p_qt + self.lr * (p_r + self.gamma * qt_max - p_qt)
