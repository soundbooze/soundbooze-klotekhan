import numpy as np
import threading
from scipy.signal import find_peaks, argrelextrema
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

from erb import *

if __name__ == "__main__":

    ts, i = beatroot(sys.argv[1])
    #S,h,i = LoadWAV(sys.argv[1])
    
    #threshold = 0.02

    #i = np.array(i)

    '''
    for z in range(len(i)):
        if i[z] < np.mean(i):
            i[z] = 0
    '''

    #plt.bar(range(len(i)), i)
    #plt.show()

    '''
    result = seasonal_decompose(i, freq=20)
    result.plot()
    plt.show()

    print result.seasonal
    '''

    '''
    peaks = FindPeaks(i)

    ts = []
    for p in peaks:
        ts.append(i[p])

    # https://github.com/MonsieurV/py-findpeaks
    indexes = argrelextrema(
        np.array(ts),
        comparator=np.greater,order=2
    )

    idxPeaks = []
    for z in indexes[0]:
        idxPeaks.append(i[z])
    '''

    '''
    print ts
    print indexes[0]
    '''

    '''
    print 'Q Interval'

    arr = i
    q1 = np.quantile(arr, .25)
    q2 = np.quantile(arr, .50)
    q3 = np.quantile(arr, .75)

    print q1, q2, q3

    print 'Q TS'

    arr = ts
    q1 = np.quantile(arr, .25)
    q2 = np.quantile(arr, .50)
    q3 = np.quantile(arr, .75)

    print q1, q2, q3
    '''

    '''
    print indexes[0]

    print 'Q Idx'

    arr = idxPeaks
    q1 = np.quantile(arr, .25)
    q2 = np.quantile(arr, .50)
    q3 = np.quantile(arr, .75)

    print q1, q2, q3
    '''
