import plotly
import numpy as np
import scipy.io
from scipy.signal import lfilter, freqz, filtfilt, find_peaks, butter

#Plot the cardiogram in time domain
def time_plot(cardiogram, filter=False):
    mat = scipy.io.loadmat(cardiogram)
    if 'ecg' in mat:
        ecg_data =  mat['ecg']
    elif 'ecg_hfn' in mat:
        ecg_data =  mat['ecg_hfn']
    else:
        ecg_data = mat['ECG']
    ecg_data = ecg_data.astype(float)
    ecg_data = np.array(ecg_data).flatten()
    t = np.arange(0,len(ecg_data))/200

    if filter:
        fs=200.0
        pli = 60.0
        quality_factor = 30.0
        b,a = scipy.signal.iirnotch(pli, quality_factor, fs =fs)	
        ecg_data = scipy.signal.filtfilt(b,a,ecg_data)

    fig = dict({
    "data": [{"x": t,
            "y":  ecg_data}],
    "layout": {"title": {"text": "Cardiogram Plot in Time Domain"},
                "xaxis_title" : "Time (s)",
                "yaxis_title" : "Amplitud (mV)",
    }
    })
    # fig is plotly figure object and graph_div the html code for displaying the graph
    return plotly.offline.plot(fig, auto_open = False, output_type="div")

#Plot the cardiogram in time domain with the QRS points
def points_plot(cardiogram, filter=False):
    mat = scipy.io.loadmat(cardiogram)
    if 'ecg' in mat:
        ecg_data =  mat['ecg']
    elif 'ecg_hfn' in mat:
        ecg_data =  mat['ecg_hfn']
    else:
        ecg_data = mat['ECG']
    ecg_data = ecg_data.astype(float)
    ecg_data = np.array(ecg_data).flatten()
    t = np.arange(0,len(ecg_data))/200
    fs = 200.0
    pli = 60.0
    quality_factor = 30.0
    b,a = scipy.signal.iirnotch(pli, quality_factor, fs =fs)	
    ecg_data = scipy.signal.filtfilt(b,a,ecg_data)

    #Finding the QRS points:

    ecg_data2 = ecg_data/max(abs(ecg_data))
   
    # Finding the QRS points
    R, _ = find_peaks(ecg_data2, distance=150)
    S, _ = find_peaks(-ecg_data2, distance=150)
    Q, _ = find_peaks(-ecg_data2, prominence=(0.055,0.3))

    for i in range(round(len(Q)-1)):
        j=i + 1
        while j < len(Q) - 1:
            if Q[j] - Q[i] < 150:
                Q = np.delete(Q, j)
            j+=1

    fig = dict({
    "data": [
            {"name" : 'Cardiogram',
            "x": t,
            "y":  ecg_data},
             {"mode": 'markers',
            "name" : 'Q Points',
            "marker": { "color": 'rgba(144, 0, 182, 0.95)',
            "symbol": 'x',
            "size": 12,
                },
            "type" :  'scatter',
            "x": Q/fs,
            "y":  ecg_data[Q]},
            {"mode": 'markers',
            "name" : 'R Points',
            "type" :  'scatter',
            "marker": { "color": 'rgba(255, 100, 10, 0.95)',
                        "symbol": 'x',
                        "size": 12,
                        },
            "x": R/fs,
            "y":  ecg_data[R],
                },
             {"mode": 'markers',
            "name" : 'S Points',
            "type" : 'scatter',
            "marker": { "color": 'rgba(45, 255, 0, 0.95)',
            "symbol": 'x',
            "size": 12,
                },
            "x": S/fs,
            "y":  ecg_data[S]},
            ],
    "layout": {"title": {"text": "Cardiogram Plot in Time Domain"},
                "xaxis_title" : "Time (s)",
                "yaxis_title" : "Amplitud (mV)",
    }
    })
    # fig is plotly figure object and graph_div the html code for displaying the graph

    # Obtaining the hearbeat rhythm
    time_Rs = (R[1]-R[0])/fs
    heart_rate = "{:.2f}".format(60/time_Rs)

    return [plotly.offline.plot(fig, auto_open = False, output_type="div"), heart_rate]