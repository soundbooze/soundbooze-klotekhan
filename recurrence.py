import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from pyts.image import RecurrencePlot
from sklearn.preprocessing import MinMaxScaler

def sonicannotator (guitar, feature):

    filename = "/tmp/melband.csv"
    run = "sonic-annotator -d " + feature + " " + guitar + " -w csv --csv-stdout > /dev/null 2>&1 > " + filename
    os.system(run)
    data = pd.read_csv(filename)
    M = data.to_numpy() # .values
    ts = M[:,1]
    return ts, np.flip(np.transpose(M), axis=0)

ts, M = sonicannotator(sys.argv[1], "vamp:libvamp_essentia:essentia_MelBands:essentia_MelBands")

Z = M[15:24:,0:]

melsum = MinMaxScaler(feature_range=(0, 1)).fit_transform(np.array(np.sum(Z, axis=0)).reshape(-1,1))
melsum = np.transpose(melsum)
melsum = melsum[0]

plt.subplot(311)
plt.imshow(M)
plt.subplot(312)
plt.imshow(Z)
plt.subplot(313)
plt.bar(range(len(melsum)), melsum)

rp = RecurrencePlot(dimension=2, time_delay=1,
                    threshold='percentage_points',
                    percentage=20)

X_rp = rp.fit_transform(Z)

plt.figure(figsize=(4, 4))
plt.imshow(X_rp[0], cmap='binary', origin='lower')
plt.title('Recurrence Plot', fontsize=10)
plt.show()
