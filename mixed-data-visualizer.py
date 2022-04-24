import argparse
import time
import brainflow
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.signal as sig
import csv
import pandas as pd
import peakutils
import os

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions
from scipy import signal
from scipy.io import wavfile

nan = math.nan
filename = "C:/Users/W10/OneDrive/Desktop/Spring 2022/crux_prompt/10-mixed-042322.csv"
#filename = "C:/Users/W10/OneDrive/Desktop/SSVEP MAT Files/MAMAM_EEG_SSVEP_Dataset_2_csvs/T006c.csv"
#filename = "C:/Users/W10/OneDrive/Desktop/SSVEP MAT Files/Subject_5/session_5Hz.csv"

file_base, file_extension = os.path.splitext(filename)
colsused = np.array([1, 2, 3, 4, 15, 16])
num_rows_to_skip = 10
custom_delimiter = ","

data = np.loadtxt(filename, delimiter=custom_delimiter if not custom_delimiter == "" else "," if file_extension ==
                  ".csv" else " ", skiprows=num_rows_to_skip, usecols=None if not isinstance(colsused, np.ndarray) else colsused)
data[:,4] = 500 * data[:,4] # labelled
data[:,5] = 500 * data[:,5] # labelled
cols = np.arange(data[0].size) if not isinstance(
    colsused, np.ndarray) else colsused

maxdat = data[:, 0].size if len(data.shape) > 1 else data.size

# window settings
leftborder = 100
rightborder = maxdat
welch_left = 0
welch_right = 90

# frequency settings
fft_type = "fft"
sampling_rate = 200

# welch settings
welch_all = True
seg = 5*sampling_rate
poverlap = 0.5

# bandpass settings
apply_bandpass = False
bandpass_left = 5
bandpass_right = 20

# extra options
legend = False
label = True
avg_plot = False

# threshold settings
label_thres = 0.3
avg_thres = 0.5

# distance settings
min_dis = 1
avg_min_dis = 0.1

# inefficient globals
max_welch = 0
avg_freq = np.zeros(maxdat)
sum_welch = np.zeros(maxdat)
welch_size = 0


def main():

    global max_welch
    global sum_freq
    global sum_welch

    fig = plt.figure()
    ax1 = fig.add_subplot(3 if avg_plot and data[0].size > 1 else 2, 1, 1)
    ax1.set_title("Time Domain")
    ax1.set_xlabel("Sample Index")
    ax1.set_ylabel("Voltage (mV)")
    for i in range(data[0].size):
        #if (apply_bandpass): # non labelled
        if (apply_bandpass and i <= 3): # labelled
            if (len(data.shape) > 1):
                newdat = data[:, i]
            else:
                newdat = data
            sos = sig.butter(3, [bandpass_left*2/sampling_rate, bandpass_right *
                                 2/sampling_rate], btype='bandpass', output='sos')
            newdat = sig.sosfilt(sos, newdat)[leftborder:rightborder]
        else:
            if (len(data.shape) > 1):
                newdat = data[leftborder:rightborder, i]
            else:
                newdat = data[leftborder:rightborder]
        index = leftborder + np.arange(newdat.size)
        ax1.plot(index, newdat)
        if (legend and data[0].size > 1):
            if ((cols.size < 12 and avg_plot == False) or (cols.size < 6 and avg_plot == True)):
                ax1.legend(cols)

    ax2 = fig.add_subplot(3 if avg_plot and data[0].size > 1 else 2, 1, 2)
    ax2.set_title("Frequency Domain using " + fft_type)
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Amplitude")
    for i in range(data[0].size):
        if (apply_bandpass):
            if (len(data.shape) > 1):
                newdat = data[:, i]
            else:
                newdat = data
            sos = sig.butter(3, [bandpass_left*2/sampling_rate, bandpass_right *
                                 2/sampling_rate], btype='bandpass', output='sos')
            newdat = sig.sosfilt(sos, newdat)[leftborder:rightborder]
        else:
            if (len(data.shape) > 1):
                newdat = data[leftborder:rightborder, i]
            else:
                newdat = data[leftborder:rightborder]

        if (fft_type == "welch"):
            welchfreq, welch_data = signal.welch(
                newdat, fs=sampling_rate, nperseg=seg if not welch_all else newdat.size, noverlap=poverlap * (seg if not welch_all else newdat.size))
        else:
            welch_data = np.abs(np.fft.fft(newdat))
            welchfreq = np.fft.fftfreq(len(welch_data), 1/sampling_rate)
            welchfreq = np.array([x for x in welchfreq if x >= 0])
            welch_data = welch_data[:welchfreq.size]

        welch_size = welch_data.size
        avg_freq = welchfreq
        left_lim = 0
        right_lim = welch_data.size
        if (not math.isnan(welch_left)):
            left_lim = math.ceil(np.where(welchfreq > welch_left)[0][0])
        if (not math.isnan(welch_right)):
            right_lim = math.ceil(np.where(welchfreq > welch_right)[0][0])
        if (max(welch_data[left_lim:right_lim]) > max_welch):
            max_welch = max(welch_data[left_lim:right_lim])
        ax2.plot(welchfreq[left_lim:right_lim], welch_data[left_lim:right_lim])
        if (legend and data[0].size > 1):
            if ((cols.size < 12 and avg_plot == False) or (cols.size < 6 and avg_plot == True)):
                ax2.legend(cols)
            else:
                max_y = max(welch_data[left_lim:right_lim])
                max_x = welchfreq[welch_data[left_lim:right_lim].argmax()]
                ax2.annotate(cols[i], (max_x, max_y), color="red",
                             verticalalignment="bottom", weight="bold")

    sum_welch = np.zeros(welch_size)

    for i in range(data[0].size):
        # inefficient code
        if (apply_bandpass):
            if (len(data.shape) > 1):
                newdat = data[:, i]
            else:
                newdat = data
            sos = sig.butter(3, [bandpass_left*2/sampling_rate, bandpass_right *
                                 2/sampling_rate], btype='bandpass', output='sos')
            newdat = sig.sosfilt(sos, newdat)[leftborder:rightborder]
        else:
            if (len(data.shape) > 1):
                newdat = data[leftborder:rightborder, i]
            else:
                newdat = data[leftborder:rightborder]

        if (fft_type == "welch"):
            welchfreq, welch_data = signal.welch(
                newdat, fs=sampling_rate, nperseg=seg if not welch_all else newdat.size, noverlap=poverlap * (seg if not welch_all else newdat.size))
        else:
            welch_data = np.abs(np.fft.fft(newdat))
            welchfreq = np.fft.fftfreq(len(welch_data), 1/sampling_rate)
            welchfreq = np.array([x for x in welchfreq if x >= 0])
            welch_data = welch_data[:welchfreq.size]

        for j in range(welch_size):
            sum_welch[j] = sum_welch[j] + welch_data[j]

        left_lim = 0
        right_lim = welch_data.size
        if (not math.isnan(welch_left)):
            left_lim = math.ceil(np.where(welchfreq > welch_left)[0][0])
        if (not math.isnan(welch_right)):
            right_lim = math.ceil(np.where(welchfreq > welch_right)[0][0])

        if (label):
            # inefficient code
            index = peakutils.indexes(welch_data[left_lim:right_lim], thres=0, min_dist=math.ceil(
                np.where(welchfreq > 2 + min_dis)[0][0] - math.ceil(np.where(welchfreq > 2)[0][0])))
            index = [x for x in index if welch_data[left_lim:right_lim]
                     [x] > label_thres * max_welch]
            #index = [x for x in index if welch_data[x] > label_thres * max_welch]
            for j, value in enumerate(index):
                ax2.plot(welchfreq[left_lim:right_lim][value],
                         welch_data[left_lim:right_lim][value], marker="o", ls="", ms=3)
                ax2.annotate("{:.2f}".format(welchfreq[left_lim:right_lim][value]), (
                    welchfreq[left_lim:right_lim][value], welch_data[left_lim:right_lim][value]), verticalalignment="top")

    if (avg_plot and data[0].size > 1):
        ax3 = fig.add_subplot(313)
        ax3.set_title("Average Frequency Domain using " + fft_type)
        ax3.set_xlabel("Frequency (Hz)")
        ax3.set_ylabel("Amplitude")
        ax3.plot(avg_freq[left_lim:right_lim],
                 sum_welch[left_lim:right_lim]/data[0].size)
        index = peakutils.indexes(sum_welch[left_lim:right_lim]/data[0].size, thres=avg_thres, min_dist=math.ceil(
            np.where(welchfreq > 2 + avg_min_dis)[0][0] - math.ceil(np.where(welchfreq > 2)[0][0])))
        if (label):
            for j, value in enumerate(index):
                ax3.plot(avg_freq[left_lim:right_lim][value], sum_welch[left_lim:right_lim]
                         [value]/data[0].size, marker="o", ls="", ms=3)
                ax3.annotate("{:.2f}".format(avg_freq[left_lim:right_lim][value]), (
                    avg_freq[left_lim:right_lim][value], sum_welch[left_lim:right_lim][value]/data[0].size), verticalalignment="top")

    plt.tight_layout(h_pad=-2)
    plt.show()


if __name__ == "__main__":
    main()
