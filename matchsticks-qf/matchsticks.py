from game import Game, ConfigKey
from plot import plot
from player import *
from pprint import PrettyPrinter
from writer import Writer
import sys

def train(nbSticks, nbGames, plotQFunction, players, debugMode = False):
    writer = Writer() if debugMode else None
    game = Game(nbSticks, players, { ConfigKey.TRAIN: True, ConfigKey.DEBUG: debugMode })

    # stats for trained players
    qFunctionStats = {}
    for p in (p for p in players if type(p) is TrainedPlayer):
        qFunctionStats[p] = dict((i, ([], [], [])) for i in range(1, nbSticks + 1))

    print("\nTraining...")
    for i in range(0, nbGames):
        if writer:
            writer.beginGame(i, game.players[0], game.players[1])

        game.start() # play a game

        if writer:
            writer.endGame(game.players[0], game.players[1])

        # update stats
        for p in qFunctionStats:
            for s,q in p.q.items():
                qFunctionStats[p][s][0].append(q[0])
                qFunctionStats[p][s][1].append(q[1])
                qFunctionStats[p][s][2].append(q[2])

        # decrease exploration over time
        if i % 10 == 0:
            for p in players:
                p.epsilon = max(p.epsilon * 0.996, 0.05)

        game.reset()

    if writer:
        writer.close()

    for p in (p for p in players if type(p) is TrainedPlayer):
        print(f'\n=== Value function of {p}: ===')
        PrettyPrinter().pprint(p.q)

        if plotQFunction:
            plot(qFunctionStats[p])

def test(nbSticks, nbGames, players):
    game = Game(nbSticks, players)
    for p in players:
        p.epsilon = 0

    winrates = { players[0]: 0, players[1]: 0 } # stats
    for i in range(0, nbGames):
        winner = game.start()
        winrates[winner] += 1
        game.reset()

    # display winrates
    print(f'\n------------------------------------')
    winrates = dict(map(lambda pw : (pw[0], pw[1] / nbGames), winrates.items()))
    for p,w in winrates.items():
        print(f'player {p}, winrate: {w}')
    print(f'------------------------------------')

def play(nbSticks, trainedPlayer):
    game = Game(nbSticks, [trainedPlayer, HumanPlayer('humanPlayer')], { ConfigKey.LOG: True })
    trainedPlayer.epsilon = 0 # greedy

    game.start()

def askUserConfiguration():
    nbSticks = ask(f'How many sticks (12) ? > ', 12, int)
    trainSize = ask(f'How many train iterations (10000) ? > ', 10000, int)
    testSize = ask(f'How many test iterations (1000) ? > ', 1000, int)
    e = ask(f'Epsilon (0.99) ? > ', 0.99, float)
    lr = ask(f'Leaning Rate (0.01) ? > ', 0.01, float)
    g = ask(f'Gamma (0.8) ? > ', 0.8, float)
    plotValueFunction = ask(f'Plot value function (y|n) ? > ', False, bool)
    return (nbSticks, trainSize, testSize, e, lr, g, plotValueFunction)

def ask(question, defaultValue, f):
    s = input(question)
    if s:
        return f(s.strip().lower())
    return defaultValue

def bool(s):
    if s == 'y':
        return True
    else:
        return False

# ================================
#   main program
# ================================

debugMode = True if len(sys.argv) > 1 and sys.argv[1].strip().lower() == "debug" else False

(nbSticks, trainSize, testSize, e, lr, g, plotQFunction) = askUserConfiguration()

trainedPlayer1 = TrainedPlayer('trainedPlayer1', nbSticks, e, lr, g)
trainedPlayer2 = TrainedPlayer('trainedPlayer2', nbSticks, e, lr, g)
randomPlayer = RandomPlayer('randomPlayer')

# Train IA
train(nbSticks, trainSize, plotQFunction, [trainedPlayer1, trainedPlayer2], debugMode)

# Test IA against other player
test(nbSticks, testSize, [trainedPlayer1, randomPlayer])

# Test IA against human
while True:
    play(nbSticks, trainedPlayer1)
