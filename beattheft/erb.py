import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from sklearn.preprocessing import MinMaxScaler

from utils import *

def erb (guitar):

    filename = genTempFile()
    run = "sonic-annotator -d vamp:libvamp_essentia:essentia_ERBBands:essentia_ERBBands " + guitar + " -w csv --csv-stdout > /dev/null 2>&1 > " + filename
    os.system(run)
    data = pd.read_csv(filename)
    M = data.to_numpy() # .values
    r,c = M.shape
    ts = M[:,1] #column
    ERB = (M[:r, 2:c]) 
    os.unlink(filename)

    return ts,ERB 

def beatroot (guitar):

    filename = genTempFile()
    run = "sonic-annotator -d vamp:beatroot-vamp:beatroot:beats " + guitar + " -w csv --csv-stdout > /dev/null 2>&1 > " + filename
    os.system(run)
    data = pd.read_csv(filename)
    M = data.to_numpy() # .values
    r,c = M.shape
    ts = M[:,1] #column

    itv = []
    for t in range(len(ts)-1):
        itv.append(ts[t+1] - ts[t])

    os.unlink(filename)

    return ts, itv

def spectralcontrast (guitar):

    filename = genTempFile()
    run = "sonic-annotator -d vamp:libvamp_essentia:SpectralContrast_17:spectralcontrast " + guitar + " -w csv --csv-stdout > /dev/null 2>&1 > " + filename
    os.system(run)
    data = pd.read_csv(filename)
    M = data.to_numpy() # .values
    r,c = M.shape
    ts = M[:,1] #column
    SC = (M[:r, 2:c]) 
    os.unlink(filename)

    return ts,SC

def getSleep(ts, E):

    summy = []
    r, c = E.shape
    for i in range(r):
      row = E[i,:]
      sumrow = np.sum(row)
      summy.append(sumrow)

    peaks, _ = find_peaks(summy, height=0)

    hpeaks = ts[peaks]

    itvPeaks = []
    for i in range(len(hpeaks)-1):
        itvPeaks.append(hpeaks[i+1]-hpeaks[i])

    return summy, hpeaks, itvPeaks

def plot(s, h, i):

    i = np.array(i)

    threshold = 0.02

    thrsh = []
    for z in i:
        if z > np.mean(i) and z < np.max(i) - threshold:
            thrsh.append(z)

    h, v = np.histogram(i, density=True)

    scaled = MinMaxScaler(feature_range=(0, 1)).fit_transform(np.array(i).reshape(-1,1))

    plt.subplot(611)
    plt.title('Threshold')
    plt.plot(thrsh)
    plt.subplot(612)
    plt.title('Interval')
    plt.plot(i)
    plt.subplot(613)
    plt.title('Bar Interval')
    plt.bar(range(len(i)), i)
    plt.subplot(614)
    plt.title('Histogram')
    plt.hist(i)
    plt.subplot(615)
    plt.title('Value Histogram')
    plt.bar(range(len(v)), v)
    plt.subplot(616)
    plt.title('Scaled Interval')
    plt.plot(scaled[scaled > 0.3])
    plt.show()
