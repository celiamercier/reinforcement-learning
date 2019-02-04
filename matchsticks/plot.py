from math import ceil
import matplotlib.pyplot as plt
import matplotlib
import colorsys

def plot(values, f = (lambda k,v: True)):
    cols = 4
    rows = ceil(len(values) / cols)

    i = 1
    for s,q in values.items():
        if f(s, q):
            plt.subplot(rows, cols, i, title = f'State {s}')
            __subplot(q)
        i += 1
        
    plt.show()

def __subplot(values):
    # compute x values
    x = range(0, len(values[0]))

    # plot y values
    plt.plot(x, values[0], label = 'a1')
    plt.plot(x, values[1], label = 'a2')
    plt.plot(x, values[2], label = 'a3')
    plt.legend()

def __colors(n):
    colors = []
    hStep = 1 / n
    for i in range(0, n):
        if i == 0:
            colors.append((0, 0.5, 1))
        else:
            colors.append((colors[i - 1][0] + hStep, 0.5, 1))
    return __convertToRGB(colors)

def __convertToRGB(colors):
    rgbColors = []
    for hls in colors:
        rgb = colorsys.hls_to_rgb(*hls)
        rgbColors.append(rgb)
    return rgbColors

def __filter(d, f):
    r = {}
    for k, v in d.items():
        if f(k,v):
            r[k] = v
    return r
