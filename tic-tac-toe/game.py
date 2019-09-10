from board import Board
from player import *
from random import seed, random, shuffle
from enum import Enum

class ConfigKey(Enum):
    TRAIN = 'train'
    LOG = 'log'
    DEBUG = 'debug'

class Game:
    def __init__(self, boardSize, players, config = {ConfigKey.TRAIN: False, ConfigKey.LOG: False, ConfigKey.DEBUG: False}):
        self.config = config
        self.players = players
        self.board = Board(boardSize)

        if self.config.get(ConfigKey.DEBUG):
            seed(12345)

        shuffle(self.players)

    def start(self):
        turn = 0
        p1 = self.players[0]
        p2 = self.players[1]

        self.__print('\n==== Game started ====')
        while (True):
            self.board.display()

            player = self.__getCurrentPlayer(turn, p1, p2)
            move = player.play(self.board)
            self.board.set(turn + 1, move)
            if (self.__isFinished(turn + 1, move)):
                break

            turn = (turn + 1) % 2

        self.board.display()
        winner = self.__getCurrentPlayer(turn, p1, p2)
        self.__print(f'\n{winner} wins !')

    def __isFinished(self, player, action):
        return self.board.isFull() or self.board.hasWon(player, action)

    def __display(self):
        if self.config.get(ConfigKey.LOG):
            self.board.display()

    def __print(self, str):
        if self.config.get(ConfigKey.LOG):
            print(str)

    def __getCurrentPlayer(self, turn, p1, p2):
        return p1 if turn % 2 == 0 else p2

    def __getOpponentPlayer(self, turn, p1, p2):
        return p2 if turn % 2 == 0 else p1
