import json
import os
import matplotlib.pyplot as plt

class Log:
    measurements = ["xAccl", "yAccl", "zAccl"]
    def __init__(self, data):
        self.times = []
        self.xAccl = []
        self.yAccl = []
        self.zAccl = []
        for measurement in data:
            self.times.append(measurement["timestamp"])
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


if __name__ == '__main__':
    folder = "Logs/"

    for file in os.listdir(folder):
        filepath = os.path.join(folder, file)
        with open(filepath) as f:
            data = json.load(f)
        log = Log(data)
        log.plot()