import numpy.fft as fft
from numpy import abs
import matplotlib.pyplot as plt
import json

#Note that this code is based off of code given by Lefan Zheng.
#Find the frequency of an exercise in hz
class Frequency():
    def __init__(self, log_file):
        with open(log_file, 'r') as fd:
            data = json.load(fd)
            x_accl = [item['xAccl'] for item in data]
            y_accl = [item['yAccl'] for item in data]
            z_accl = [item['zAccl'] for item in data]
            timestamp = [item['timestamp'] for item in data]

            fs = (len(timestamp) - 1) / (timestamp[-1] - timestamp[0])
            x_fft = list(abs(fft.fft(x_accl)))[:int(len(timestamp)/2)]
            y_fft = list(abs(fft.fft(y_accl)))[:int(len(timestamp)/2)]
            z_fft = list(abs(fft.fft(z_accl)))[:int(len(timestamp)/2)]
            freq = [fs/len(timestamp)*index for index in range(int(len(timestamp) /2))]
            self.x_freq = self.best_freq(x_fft, freq)
            self.y_freq = self.best_freq(y_fft, freq)
            self.z_freq = self.best_freq(z_fft, freq)
            self.freq = self.x_freq

    #removes the data where frequency is 0
    def best_freq(self, ffts, freqs):
        nffts = ffts[1:]
        mfreq = freqs[1:]
        sarr = sorted(zip(ffts, freqs), key=lambda x: x[0])
        for i in range(1, len(sarr)):
            if sarr[-i][1] != 0:
                return sarr[-i][1]

    def get_freq(self):
        return self.freq