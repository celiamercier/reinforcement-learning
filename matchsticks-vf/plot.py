import matplotlib.pyplot as plt
import matplotlib
import colorsys

def plot(values, f = (lambda k,v: True)):
    i = 1
    for p,v in values.items():
        plt.subplot(1, len(values), i)
        __subplot(v, f)
        i += 1

    plt.xlabel('Time')
    plt.ylabel('Value function')
    plt.title('Value function over time')
    plt.legend()
    plt.show()

def __subplot(values, f = (lambda k,v: True)):
    # compute x values
    x = []
    for y in values.values():
        x = range(0, len(y))
        break

    # colors
    filteredValues = dict((v for v in values.items() if f(v[0], v[1])))
    colors = __colors(len(filteredValues))

    # plot y values with given color
    i = 0
    for label, y in filteredValues.items():
        plt.plot(x, y, color = colors[i], label = label)
        i += 1

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
