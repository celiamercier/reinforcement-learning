from game import Game, ConfigKey
from player import *

boardSize = 3
game = Game(boardSize, [HumanPlayer('humanPlayer'), RandomPlayer('randomPlayer')], { ConfigKey.LOG: True })
game.start()
