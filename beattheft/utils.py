import os
import time
import hashlib
import essentia.standard as es
import numpy as np

def rootFinder(fs):

    rootMajor = []
    rootMinor = []
    maxDominant = 2
    dominant2 = []

    uniq_f = 0.00
    for s in majorScale: 
        inters = np.intersect1d(s, fs)
        dominant2.append(len(inters)+uniq_f)
        uniq_f = uniq_f + 0.01

    maj_sortar = sorted(dominant2, reverse=True)

    rootMajor.append(pitchMajor[dominant2.index(maj_sortar[0])])
    rootMajor.append(pitchMajor[dominant2.index(maj_sortar[1])])

    rootMinor.append(pitchMinor[dominant2.index(maj_sortar[0])])
    rootMinor.append(pitchMinor[dominant2.index(maj_sortar[1])])

    return rootMajor, rootMinor 

def loadAudioFile(f, sr):

    return es.MonoLoader(filename=f, downmix = 'mix', sampleRate = sr)

def genTempFile():

    mk = time.mktime(time.gmtime())
    md5 = hashlib.md5(str(mk))
    tempfile = "/tmp/" + md5.hexdigest()
    if (os.path.exists(tempfile)):
        os.unlink(tmpfile)

    return tempfile

def recordJack (ms):

  jack_capture = "/usr/local/bin/jack_capture_ms"
  filename = genTempFile()
  os.system(jack_capture + ' -d ' + ms + filename + ' > /dev/null 2>&1')

  return filename
