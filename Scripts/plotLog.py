import matplotlib.pyplot as plt
from peakutils.plot import plot as pplot
from log import Log
import os
import json
import numpy as np
from scipy.signal import savgol_filter
import peakutils


def plotLog(log):
    i=1
    plt.figure(1).set_size_inches(24,48)
    for ylabel in log.measurements:
        m = log.__dict__[ylabel]
        plt.subplot(len(log.measurements),1,i)
        i += 1
        plt.plot(log.times,m,label=ylabel)
        plt.xlabel('Time (s)')
        plt.title("magnitude for %s" % ylabel)
        plt.grid(True)
    plt.tight_layout()
    plt.show()

def plotPeaks(log, thres, min_dist):
    for m in log.measurements:
        x = np.array(log.times)
        y0 = np.array(log.__dict__[m])
        amt = 25
        y1 = savgol_filter(y0, amt, 2, mode="nearest")
        for y in [y0,y1]:
            indexes = peakutils.indexes(y, thres=thres)
            plt.figure(figsize=(10,6))
            pplot(x, y, indexes)
    plt.show()
    return len(indexes)

if __name__ == '__main__':
    folder = "Logs/"

    ct = 0

    files = os.listdir(folder)
    for i in range(len(files)):
        print(files[i])
        ct += 1
        if ct == 3:
            continue
        file = files[i]
        filepath = os.path.join(folder, file)
        with open(filepath) as f:
            data = json.load(f)
        log = Log(data)
        log.getPeaks(0.5, 5)
        print(log.getFrequency())
        plotLog(log)