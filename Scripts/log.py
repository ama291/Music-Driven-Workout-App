import json
import os
import matplotlib.pyplot as plt
import peakutils
from peakutils.plot import plot as pplot
import numpy as np
from scipy.signal import savgol_filter

class Log:
    measurements = ["xAccl", "yAccl", "zAccl"]
    def __init__(self, data):
        time0 = data[0]["timestamp"]
        self.times = []
        self.xAccl = []
        self.yAccl = []
        self.zAccl = []
        for measurement in data:
            self.times.append(measurement["timestamp"] - time0)
            self.xAccl.append(measurement["xAccl"])
            self.yAccl.append(measurement["yAccl"])
            self.zAccl.append(measurement["zAccl"])

    def plot(self):
        i=1
        plt.figure(1).set_size_inches(24,48)
        for ylabel in self.measurements:
            m = self.__dict__[ylabel]
            plt.subplot(len(self.measurements),1,i)
            i += 1
            plt.plot(self.times,m,label=ylabel)
            plt.xlabel('Time (s)')
            plt.title("magnitude for %s" % ylabel)
            plt.grid(True)
        plt.tight_layout()
        plt.show()

    def getPeaks(self, thres, min_dist):
        print("--")
        for m in self.measurements:
            x = np.array(self.times)
            y0 = np.array(self.__dict__[m])
            amt = 25
            y1 = savgol_filter(y0, amt, 2, mode="nearest")
            y2 = savgol_filter(y0, amt, 2, mode="mirror")
            y3 = savgol_filter(y0, amt, 2, mode="constant")
            y4 = savgol_filter(y0, amt, 2, mode="wrap")
            for y in [y0,y1,y2,y3,y4]:
                indexes = peakutils.indexes(y, thres=thres)
                print(len(indexes))
                plt.figure(figsize=(10,6))
                pplot(x, y, indexes)
            plt.show()


if __name__ == '__main__':
    folder = "Logs/"

    ct = 0

    files = os.listdir(folder)
    for i in range(len(files)):
        ct += 1
        if ct != 2:
            continue
        file = files[i]
        filepath = os.path.join(folder, file)
        with open(filepath) as f:
            data = json.load(f)
        log = Log(data)
        log.getPeaks(0.5, 5)
