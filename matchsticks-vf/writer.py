from player import TrainedPlayer
from datetime import datetime

class Writer:
    def __init__(self):
        filename = "debug-" + datetime.strftime(datetime.now(), "%y%m%d-%H%M%S") + ".log"
        self.file = open(filename, "w")

    def beginGame(self, idx, p1, p2):
        strings = []
        strings.append(f'\n=== Game n°{idx} ===\n')
        strings += self.__getValueFunctionAsStr(p1, p2)
        self.file.writelines(strings)

    def endGame(self, p1, p2):
        strings = []

        # game history
        n = max(len(p1.history), len(p2.history))
        for i in range(n):
            if (i < len(p1.history)):
                strings.append(f'{p1}: {p1.history[i]}\n')
            if (i < len(p2.history)):
                strings.append(f'{p2}: {p2.history[i]}\n')

        # train
        strings += self.__getValueFunctionAsStr(p1, p2)

        self.file.writelines(strings)

    def __getValueFunctionAsStr(self, p1, p2):
        str = []
        if type(p1) is TrainedPlayer:
            str.append(f'{p1} value function: {p1.v}\n')
        if type(p2) is TrainedPlayer:
            str.append(f'{p2} value function: {p2.v}\n')
        return str

    def close(self):
        self.file.close()
