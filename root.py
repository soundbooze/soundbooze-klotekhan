import os
import vamp
import librosa
import numpy as np

# db threshold -> stop drum 

def beatRootDetection():
    result = [] 
    JACK_CAPTURE = "/usr/local/bin/jack_capture"
    CAPTURE_DURATION = 1
    PLAYBACK_WAV = "playback.wav"
    os.system("(" + str(JACK_CAPTURE) + " -d " + str(CAPTURE_DURATION) + " -f wav " + str(PLAYBACK_WAV) + " > /dev/null 2>&1)")
    audio, sr = librosa.load(PLAYBACK_WAV, sr=44100, mono=False)
    data = vamp.collect(audio, sr, "beatroot-vamp:beatroot")
    ts = data['list']

    for i, tarr in enumerate(ts):
        t = tarr['timestamp'] 
        result.append(t)

    return result

def writeFile(s):
    BEATTXT = "/tmp/beat.txt"
    file = open(BEATTXT, "w")
    file.write(s)
    file.close()

while [ True ]:
    beat = beatRootDetection()

    subs = []
    for i, b in enumerate(beat):
        if (i < len(beat) - 1):
            sub =  beat[i+1] - beat[i]
            subs.append(sub)
            writeFile(str(sub))
            print (sub)
