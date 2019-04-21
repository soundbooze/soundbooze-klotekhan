import os
import sys
import numpy as np
import pandas as pd

import time
import rtmidi
import random
import threading
from scipy import signal
from scipy.signal import find_peaks

from sklearn.preprocessing import MinMaxScaler

import matplotlib.pyplot as plt

def InitMIDI():
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("virtual")

    return midiout

def MidiNote(midiout, note, ts):
    on = [0x90, note, random.randint(110, 125)]
    off = [0x80, note, 0]
    time.sleep(ts)
    midiout.send_message(on)
    midiout.send_message(off)

def kickThread(m, t):
    MidiNote(m, 36, t)

def snareThread(m, t):
    snare = [38, 40]
    MidiNote(m, random.sample(snare ,k=1)[0], t)

def hihatThread(m, t):
    hihat = [42, 44, 46, 48]
    MidiNote(m, random.sample(hihat ,k=1)[0], t)

def GrooveBot(itv, ms):

    os.system('paplay --volume 53444 ' + sys.argv[1] + '&')

    for z in range(len(itv)):

        t1 = threading.Thread(target=kickThread, args=(m, ms*random.randint(1,2)))
        t2 = threading.Thread(target=snareThread, args=(m, ms))
        t3 = threading.Thread(target=hihatThread, args=(m, ms))
        t4 = threading.Thread(target=kickThread, args=(m, ms/random.randint(1,4)))
        t5 = threading.Thread(target=kickThread, args=(m, ms/random.randint(1,4)))
        t6 = threading.Thread(target=snareThread, args=(m, ms))
        t7 = threading.Thread(target=hihatThread, args=(m, ms))

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start() 
        t7.start() 

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()

def beatroot (guitar):

    filename = "/tmp/beatroot.csv"
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

def barkcoeff (guitar):

    filename = "/tmp/barkcoeff.csv"
    run = "sonic-annotator -d vamp:vamp-libxtract:bark_coefficients:bark_coefficients " + guitar + " -w csv --csv-stdout > /dev/null 2>&1 > " + filename
    os.system(run)
    data = pd.read_csv(filename)
    M = data.to_numpy() # .values

    kick = []
    snare = []

    for i in range(len(M)):
        for j in range(2,5):
            if j == 2:
                kick.append(M[i][j])
            elif j == 4:
                snare.append(M[i][j])

    os.unlink(filename)

    return M, M[:,1], kick, snare

def barksum (M):    

    bsum = []

    for i in range(len(M)):
        s = 0
        for j in range(2,5):
            s = s + M[i][j]

        bsum.append(s)

    return bsum

def barkpeak (k, s):

    pk, _ = find_peaks(k, height=0)
    ps, _ = find_peaks(s, height=0)

    K = []
    S = []

    for i in pk:
        K.append(k[i])

    for i in ps:
        S.append(s[i])

    return K, S

def barkplot (k, s, K, S, bsum):

    plt.subplot(321)
    plt.plot(k)

    plt.subplot(322)
    plt.plot(s)

    Kscaled = MinMaxScaler(feature_range=(-1, 1)).fit_transform(np.array(K).reshape(-1,1))
    Sscaled = MinMaxScaler(feature_range=(-1, 1)).fit_transform(np.array(S).reshape(-1,1))

    plt.subplot(323)
    #plt.plot(signal.resample(K, 20))
    plt.plot(np.heaviside(Kscaled, 0.5))

    plt.subplot(324)
    #plt.plot(signal.resample(S, 20))
    plt.plot(np.heaviside(Sscaled, 0.5))

    plt.subplot(325)
    plt.plot(signal.resample(bsum, 20))

    plt.subplot(326)
    b = np.array(bsum)
    th = b[b > np.mean(b)]
    plt.plot(signal.resample(th, 20))

    plt.show()

def minsleep (itv):
    return np.min(itv)

def maxoccurence (itv):
    unique_elements, counts_elements = np.unique(itv, return_counts=True)
    na = np.asarray((unique_elements, counts_elements))
    maxv = na[0][np.argmax(na[1])]
    return maxv

def getBeat(filename):
    ts, itv = beatroot(filename)
    mx = maxoccurence(itv)
    ms = minsleep(itv)
    return ts, itv, mx, ms

if __name__ == "__main__":

    m = InitMIDI()

    ts, itv, mx, ms = getBeat(sys.argv[1])
    M, bts, k,s = barkcoeff(sys.argv[1])
    bsum = barksum(M)
    K,S = barkpeak(k, s)
    barkplot(k, s, K, S, bsum)

    GrooveBot(itv, mx)

    del m
