import os
import time
import rtmidi
import random
import threading
from scipy.signal import find_peaks, argrelextrema

from erb import *

def InitMIDI():
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("virtual")

    return midiout

def LoadERB(guitar):
    ts, E = erb(guitar)
    S,h,i = getSleep(ts, E)
    return S,h,i

def LoadSC(guitar):
    ts, S = spectralcontrast(guitar)
    return ts,S

def FindPeaks(i):
    peaks, _ = find_peaks(i, height=0)
    return peaks

def Argrelextrema(ts):
    indexes = argrelextrema(
        np.array(ts),
        comparator=np.greater,order=2
    )
    return indexes[0]

def Histogram(i):
    h, v = np.histogram(i, density=True)
    return h, v

def MidiNote(midiout, note, ts):
    on = [0x90, note, random.randint(110, 125)]
    off = [0x80, note, 0]
    #time.sleep(ts)
    midiout.send_message(on)
    time.sleep(ts)
    midiout.send_message(off)
    time.sleep(ts)

def kickThread(m, i, ts, t):

    for z in i:
        if z == t:
            MidiNote(m, 36, t)

def snareThread(m, i, ts, t):
    snare = [38, 40]

    for z in i:
        if z == t:
            MidiNote(m, random.sample(snare ,k=1)[0], t)

def hihatThread(m, i, ts, t):
    hihat = [42, 44, 46, 48]

    for z in i:
        if z == t:
            MidiNote(m, random.sample(hihat ,k=1)[0], t)

def tomThread(m, i, ts, t):
    tom = [41, 43, 45, 47]

    for z in i:
        if z == t:
            MidiNote(m, random.sample(tom ,k=1)[0], t)

def DrumBot(m, i, peaks):

    ts = []
    for p in peaks:
        ts.append(i[p])

    '''
    ap = Argrelextrema(ts)

    ts = []
    for p in ap:
        ts.append(i[p])
    '''

    sortedTs = sorted(ts)

    # paramSearch, len(sync), smoothing ts

    '''
    t1 = sortedTs[len(sortedTs)-3]
    t2 = sortedTs[len(sortedTs)-18]
    t3 = sortedTs[len(sortedTs)-22]
    '''
    #os.system('paplay --volume 57444 ' + sys.argv[1] + '&')

    pjatUrut = 18

    for z in range(len(i)/pjatUrut):

        t1 = sortedTs[len(sortedTs)-random.randint(1,6)]
        t2 = sortedTs[len(sortedTs)-random.randint(7,11)]
        t3 = sortedTs[len(sortedTs)-random.randint(22,31)]
        t4 = sortedTs[len(sortedTs)-random.randint(13,18)]

        tkick = threading.Thread(target=kickThread, args=(m, i, ts, t1))
        tsnare = threading.Thread(target=snareThread, args=(m, i, ts, t2))
        thihat = threading.Thread(target=hihatThread, args=(m, i, ts, t3))
        ttom = threading.Thread(target=tomThread, args=(m, i, ts, t4/(random.randint(1,2))))

        tkick.start()
        tsnare.start()
        thihat.start()
        #ttom.start()

        tkick.join()
        tsnare.join()
        thihat.join()
        #ttom.join()

if __name__ == "__main__":

    m = InitMIDI()
    S,h,i = LoadERB(sys.argv[1])
    tsc, SC = LoadSC(sys.argv[1])

    t = threading.Thread(target=plot, args=(S,h,i,))
    t.start()

    h, v = Histogram(i)

    e = FindPeaks(i)

    DrumBot(m, i, e)

    del m
