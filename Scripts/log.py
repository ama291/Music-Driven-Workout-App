import numpy.fft as fft
from numpy import abs
import json

class Log(object):
    def __init__(self, log_file, data=False):
        #note if data is false, we extract from log_file location, else we assume log_file is data
        if (not data):
            with open(log_file, 'r') as fd:
                data = json.load(fd)
        else:
            data = log_file
        x_accl = [item['xAccl'] for item in data]
        y_accl = [item['yAccl'] for item in data]
        z_accl = [item['zAccl'] for item in data]
        timestamp = [item['timestamp'] for item in data]

        fs = (len(timestamp) - 1) / (timestamp[-1] - timestamp[0])
        x_fft = list(abs(fft.fft(x_accl)))[:int(len(timestamp)/2)]
        y_fft = list(abs(fft.fft(y_accl)))[:int(len(timestamp)/2)]
        z_fft = list(abs(fft.fft(z_accl)))[:int(len(timestamp)/2)]
        freq = [fs/len(timestamp)*index for index in range(int(len(timestamp) /2))]
        self.xFreq = self.bestFrequency(x_fft, freq)
        self.yFreq = self.bestFrequency(y_fft, freq)
        self.zFreq = self.bestFrequency(z_fft, freq)
        self.freq = self.xFreq

    #removes the data where frequency is 0
    def bestFrequency(self, ffts, freqs):
        sarr = sorted(zip(ffts, freqs), key=lambda x: x[0])
        for i in range(1, len(sarr)):
            if sarr[-i][1] != 0:
                return sarr[-i][1]

    def getFrequency(self):
        return self.freq
