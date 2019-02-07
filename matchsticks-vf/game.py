from player import *
from random import seed, random, shuffle
from enum import Enum

class ConfigKey(Enum):
    TRAIN = 'train'
    LOG = 'log'
    DEBUG = 'debug'

class Game:
    def __init__(self, nbSticks, players, config = {ConfigKey.TRAIN: False, ConfigKey.LOG: False, ConfigKey.DEBUG: False}):
        self.config = config
        self.nbMaxSticks = nbSticks
        self.nbSticks = nbSticks
        self.players = players

        if self.config.get(ConfigKey.DEBUG):
            seed(12345)

        shuffle(self.players)

    def reset(self):
        self.nbSticks = self.nbMaxSticks
        shuffle(self.players)
        for p in self.players:
            p.reset()

    def start(self):
        turn = 0
        p1 = self.players[0]
        p2 = self.players[1]

        self.__print('\n==== Game started ====')
        while self.nbSticks > 0:
            self.__display()

            r = self.__move(self.__getCurrentPlayer(turn, p1, p2))
            if r != 0: # current player lost
                self.__getOpponentPlayer(turn, p1, p2).reward(r * -1)

            turn += 1

        # end of the game
        winner = self.__getCurrentPlayer(turn, p1, p2)
        self.__print(f'\n{winner} wins !')

        # train players
        self.__train()

        return winner

    def __move(self, player):
        action = player.play(self.nbSticks)
        self.nbSticks -= action

        # associated reward
        r = 0
        if self.nbSticks <= 0:
            r = -1
        player.reward(r)
        return r

    def __train(self):
        if self.config.get(ConfigKey.TRAIN):
            for p in self.players:
                p.train()

    def __display(self):
        if self.config.get(ConfigKey.LOG):
            for i in range(self.nbSticks):
                print('|', end=' ')
            print(f' ({self.nbSticks})')
            print()

    def __print(self, str):
        if self.config.get(ConfigKey.LOG):
            print(str)

    def __getCurrentPlayer(self, turn, p1, p2):
        return p1 if turn % 2 == 0 else p2

    def __getOpponentPlayer(self, turn, p1, p2):
        return p2 if turn % 2 == 0 else p1
