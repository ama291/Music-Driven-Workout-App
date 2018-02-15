import json
import os
import peakutils
import numpy as np
from scipy.signal import savgol_filter

class Log(object):
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

    def getPeaks(self, thres, min_dist):
        for m in self.measurements:
            x = np.array(self.times)
            y0 = np.array(self.__dict__[m])
            amt = 25
            y1 = savgol_filter(y0, amt, 2, mode="nearest")
            for y in [y0,y1]:
                indexes = peakutils.indexes(y, thres=thres)
        return len(indexes)

    def getTraughs(self, thres, min_dist):
        for m in self.measurements:
            x = np.array(self.times)
            y0 = np.array([-x for x in np.array(self.__dict__[m])])
            amt = 25
            y1 = savgol_filter(y0, amt, 2, mode="nearest")
            for y in [y0,y1]:
                indexes = peakutils.indexes(y, thres=thres)
        return len(indexes)

    def getFrequency(self):
        return 60 * self.getPeaks(.5, 5) / max(self.times) 

def LogFromFile(filepath):
    with open(filepath) as f:
        data = json.load(f)
    log = Log(data)
    return log

if __name__ == '__main__':
    folder = "Logs/"

    ct = 0

    files = os.listdir(folder)
    for i in range(len(files)):
        ct += 1
        if ct != 2:
            pass#continue
        file = files[i]
        filepath = os.path.join(folder, file)
        with open(filepath) as f:
            data = json.load(f)
        log = Log(data)
        log.getPeaks(0.5, 5)
        print(log.getFrequency())
