import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

pitch = ["G#", "G", "F#", "F", "E", "D#", "D", "C#", "C", "B", "A#", "A"]

def percvalley (guitar):

    filename = "/tmp/percvalley.csv"
    run = "sonic-annotator -d vamp:libvamp_essentia:perculleys:perculleys " + guitar + " -w csv --csv-stdout --csv-omit-filename > /dev/null 2>&1 > " + filename
    os.system(run)
    data = pd.read_csv(filename)
    M = data.to_numpy()

    return M

def yinf0 (guitar):

    filename = "/tmp/yinf0.csv"
    run = "sonic-annotator -d vamp:pyin:yin:f0 " + guitar + " -w csv --csv-stdout --csv-omit-filename > /dev/null 2>&1 > " + filename
    os.system(run)
    data = pd.read_csv(filename)
    M = data.to_numpy()

    return M

def beatroot (guitar):

    filename = "/tmp/beatroot.csv"
    run = "sonic-annotator -d vamp:beatroot-vamp:beatroot:beats " + guitar + " -w csv --csv-stdout --csv-omit-filename > /dev/null 2>&1 > " + filename
    os.system(run)
    data = pd.read_csv(filename)
    M = data.to_numpy()
    r,c = M.shape
    ts = M[:,0]

    itv = []
    for t in range(len(ts)-1):
        itv.append(ts[t+1] - ts[t])

    os.unlink(filename)

    return ts, itv

def basschroma (guitar):

    filename = "/tmp/basschroma.csv"
    run = "sonic-annotator -d vamp:nnls-chroma:nnls-chroma:basschroma " + guitar + " -w csv --csv-stdout --csv-omit-filename > /dev/null 2>&1 > " + filename
    os.system(run)
    data = pd.read_csv(filename)
    M = data.to_numpy()
    ts = M[:,0]
    os.unlink(filename)

    T = np.transpose(M)
    T[T < np.mean(T)+np.min(T)] = 0 
    B = np.flip(T[1:,], axis=0)

    return ts, B, np.sum(B, axis=1)

def simplechord (guitar):

    filename = "/tmp/simplechord.csv"
    run = "sonic-annotator -d vamp:nnls-chroma:chordino:simplechord " + guitar + " -w csv --csv-stdout --csv-omit-filename > /dev/null 2>&1 > " + filename
    os.system(run)
    data = pd.read_csv(filename)
    M = data.to_numpy()
    os.unlink(filename)

    return M

def lengthBass(B):
    T = np.copy(B)
    T[T > np.mean(T)+np.min(T)] = 1 

    zidx = []
    for i in range(len(T)):
        z = 0
        for j in range(len(T[i])):
            if T[i][j] == 1.0:
                z=z+1
            else:
                if z > 30:
                    print (z, end = '\n')
                    zidx.append(i)

                z = 0

    T[not zidx] = 0

    plt.imshow(T)
    plt.show()

C = simplechord(sys.argv[1])
ts, itv = beatroot(sys.argv[1])

'''
ts, B, bsum = basschroma(sys.argv[1])

lengthBass(B)
'''

#P = percvalley(sys.argv[1])

yf = yinf0(sys.argv[1])

for y in yf:
    print (y[0], y[1])


'''
plt.imshow(B, interpolation='nearest')
plt.show()
'''

'''
sortBsum = list(sorted(bsum))
sortBsum.reverse()

for i in range(0,5):
    idx = list(bsum).index(sortBsum[i])
    print pitch[idx]
'''
