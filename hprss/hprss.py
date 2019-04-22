import numpy as np
import matplotlib.pyplot as plt

import sys
import librosa
import librosa.display

from scipy.signal import find_peaks

y, sr = librosa.load(sys.argv[1], sr=48000)

D = librosa.stft(y)

rp = np.max(np.abs(D))
_ , D_percussive = librosa.decompose.hpss(D, margin=32)

sumperc = np.abs(np.sum(D_percussive, axis=0))

#print len(y), D_percussive.shape, sr

peaks, _ = find_peaks(sumperc, height=0)
percPeaks = sumperc[peaks]
#mnpercPeaks = percPeaks[percPeaks > np.mean(percPeaks)]
'''
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)
print beat_times, tempo
'''

'''
tsumperc = []

for i in range(len(sumperc)):
    z = 0
    for j in range(len(percPeaks)):
        if sumperc[i] == percPeaks[j]:
            z = sumperc[i]

    tsumperc.append(z)
'''

plt.subplot(311)
librosa.display.specshow(librosa.amplitude_to_db(np.abs(D_percussive), ref=rp), y_axis='linear')
plt.title('Percussive')
plt.yticks([]), plt.ylabel('')
plt.tight_layout()

plt.subplot(312)
plt.plot(sumperc)
plt.plot(peaks, sumperc[peaks], "x")
plt.plot(np.zeros_like(sumperc), "--", color="gray")

plt.subplot(313)
plt.bar(range(len(sumperc)), sumperc)

plt.show()
