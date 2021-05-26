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
from scipy import signal
from matplotlib.animation import FuncAnimation
from csv import writer

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

nan = math.nan

# board settings
board_id = BoardIds.SYNTHETIC_BOARD.value
#board_id = BoardIds.GANGLION_BOARD.value
serial_port = 'COM3'
mac_address = '12345'

# columns used
colsused = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])

# plot settings
display_interval = 1000
leftbord = nan
rightbord = nan
welch_left = nan
welch_right = nan

# frequency settings
fft_type = "welch"
sampling_rate = BoardShim.get_sampling_rate(board_id)

# welch settings
welch_all = True
per_data_seg = 0.2
poverlap = 0.5

# bandpass settings
apply_bandpass = False
bandpass_left = 3
bandpass_right = 30

# extra options
legend = True
label = True
avg_plot = True
create_csv = True
output_file = "C:/Users/W10/OneDrive/Desktop/brainflow/bf_gui_output.csv"

# threshold settings
label_thres = 0.2
avg_thres = 0.2

# distance settings
min_dis = 1
avg_min_dis = 1

def animate(i, board):

    global print_first

    data = board.get_board_data().T
    DataFilter.write_file(data.T, output_file, 'a')
    data = data[:, colsused] if isinstance(colsused, np.ndarray) else data[:, :]
    cols = np.arange(data[0].size) if not isinstance(colsused, np.ndarray) else colsused
    maxdat = data[:, 0].size if len(data.shape) > 1 else data.size
    leftborder = 0 if math.isnan(leftbord) else leftbord
    rightborder = maxdat if math.isnan(rightbord) else rightbord

    # inefficient vars
    max_welch = 0
    avg_freq = np.zeros(maxdat)
    sum_welch = np.zeros(maxdat)
    welch_size = 0

    ax1 = plt.subplot(3 if avg_plot and data[0].size > 1 else 2, 1, 1)
    plt.cla()
    ax1.set_title("Time Domain")
    ax1.set_xlabel("Sample Index")
    ax1.set_ylabel("Voltage (mV)")
    for i in range (data[0].size):
        if (apply_bandpass):
            if (len(data.shape) > 1):
                newdat = data[:, i]
            else:
                newdat = data

            sos = sig.butter(3, [bandpass_left*2/sampling_rate, bandpass_right*2/sampling_rate], btype = 'bandpass', output = 'sos')
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

    ax2 = plt.subplot(3 if avg_plot and data[0].size > 1 else 2, 1, 2)
    plt.cla()
    ax2.set_title("Frequency Domain using " + fft_type)
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Amplitude")
    for i in range (data[0].size):
        if (apply_bandpass):
            if (len(data.shape) > 1):
                newdat = data[:, i]
            else:
                newdat = data
            sos = sig.butter(3, [bandpass_left*2/sampling_rate, bandpass_right*2/sampling_rate], btype = 'bandpass', output = 'sos')
            newdat = sig.sosfilt(sos, newdat)[leftborder:rightborder]
        else:
            if (len(data.shape) > 1):
                newdat = data[leftborder:rightborder, i]
            else:
                newdat = data[leftborder:rightborder]

        if (fft_type == "welch"):
            welchfreq, welch_data = signal.welch(newdat, fs = sampling_rate, nperseg = per_data_seg * data[:, 0].size if not welch_all else newdat.size, noverlap = poverlap * (per_data_seg * data[:, 0].size if not welch_all else newdat.size))
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
            if ((cols.size < 12 and avg_plot == False) or (cols.size < 6 and avg_plot== True)):
                ax2.legend(cols)
            else:
                max_y = max(welch_data[left_lim:right_lim])
                max_x = welchfreq[welch_data[left_lim:right_lim].argmax()]
                ax2.annotate(cols[i], (max_x, max_y), color = "red", verticalalignment = "bottom", weight = "bold")

    sum_welch = np.zeros(welch_size)

    for i in range (data[0].size):
        #inefficient code
        if (apply_bandpass):
            if (len(data.shape) > 1):
                newdat = data[:, i]
            else:
                newdat = data
            sos = sig.butter(3, [bandpass_left*2/sampling_rate, bandpass_right*2/sampling_rate], btype = 'bandpass', output = 'sos')
            newdat = sig.sosfilt(sos, newdat)[leftborder:rightborder]
        else:
            if (len(data.shape) > 1):
                newdat = data[leftborder:rightborder, i]
            else:
                newdat = data[leftborder:rightborder]

        if (fft_type == "welch"):
            welchfreq, welch_data = signal.welch(newdat, fs = sampling_rate, nperseg = per_data_seg * data[:, 0].size if not welch_all else newdat.size, noverlap = poverlap * (per_data_seg * data[:, 0].size if not welch_all else newdat.size))
        else:
            welch_data = np.abs(np.fft.fft(newdat))
            welchfreq = np.fft.fftfreq(len(welch_data), 1/sampling_rate)
            welchfreq = np.array([x for x in welchfreq if x >= 0])
            welch_data = welch_data[:welchfreq.size]

        for j in range (welch_size):
            sum_welch[j] = sum_welch[j] + welch_data[j]

        left_lim = 0
        right_lim = welch_data.size
        if (not math.isnan(welch_left)):
            left_lim = math.ceil(np.where(welchfreq > welch_left)[0][0])
        if (not math.isnan(welch_right)):
            right_lim = math.ceil(np.where(welchfreq > welch_right)[0][0])

        if (label):
            #inefficient code
            index = peakutils.indexes(welch_data[left_lim:right_lim], thres=0, min_dist = math.ceil(np.where(welchfreq > 2 + min_dis)[0][0] - math.ceil(np.where(welchfreq > 2)[0][0])))
            index = [x for x in index if welch_data[left_lim:right_lim][x] > label_thres * max_welch]
            for j, value in enumerate(index):
                ax2.plot(welchfreq[left_lim:right_lim][value], welch_data[left_lim:right_lim][value], marker="o", ls="", ms=3)
                ax2.annotate("{:.2f}".format(welchfreq[left_lim:right_lim][value]), (welchfreq[left_lim:right_lim][value], welch_data[left_lim:right_lim][value]), verticalalignment = "top")

    if (avg_plot and data[0].size > 1):
        ax3 = plt.subplot(313)
        plt.cla()
        ax3.set_title("Average Frequency Domain using " + fft_type)
        ax3.set_xlabel("Frequency (Hz)")
        ax3.set_ylabel("Amplitude")
        ax3.plot(avg_freq[left_lim:right_lim], sum_welch[left_lim:right_lim]/data[0].size)
        index = peakutils.indexes(sum_welch[left_lim:right_lim]/data[0].size, thres = avg_thres, min_dist = math.ceil(np.where(welchfreq > 2 + avg_min_dis)[0][0] - math.ceil(np.where(welchfreq > 2)[0][0])))
        if (label):
            for j, value in enumerate(index):
                ax3.plot(avg_freq[left_lim:right_lim][value], sum_welch[left_lim:right_lim][value]/data[0].size, marker="o", ls="", ms=3)
                ax3.annotate("{:.2f}".format(avg_freq[left_lim:right_lim][value]), (avg_freq[left_lim:right_lim][value], sum_welch[left_lim:right_lim][value]/data[0].size), verticalalignment = "top")

    plt.tight_layout()

def label_extractor(input, id, array):
    try:
        return input(id) if array else [input(id)]
    except:
        return []

BoardShim.enable_dev_board_logger()
params = BrainFlowInputParams()
params.serial_port = serial_port
params.mac_address = mac_address
board = BoardShim(board_id, params)
board.prepare_session()
board.start_stream()
BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')

label_list = [None] * BoardShim.get_num_rows(board_id)
label_dict = {
    "Battery" : label_extractor(BoardShim.get_battery_channel, board_id, False),
    "EEG" : label_extractor(BoardShim.get_eeg_channels, board_id, True),
    "EMG" : label_extractor(BoardShim.get_emg_channels, board_id, True),
    "ECG" : label_extractor(BoardShim.get_ecg_channels, board_id, True),
    "Temperature" : label_extractor(BoardShim.get_temperature_channels, board_id, True),
    "Resistance" : label_extractor(BoardShim.get_resistance_channels, board_id, True),
    "EOG" : label_extractor(BoardShim.get_eog_channels, board_id, True),
    "EXG" : label_extractor(BoardShim.get_exg_channels, board_id, True),
    "EDA" : label_extractor(BoardShim.get_eda_channels, board_id, True),
    "PPG" : label_extractor(BoardShim.get_ppg_channels, board_id, True),
    "Accel" : label_extractor(BoardShim.get_accel_channels, board_id, True),
    "Analog" : label_extractor(BoardShim.get_analog_channels, board_id, True),
    "Gyro" : label_extractor(BoardShim.get_gyro_channels, board_id, True),
    "Other" : label_extractor(BoardShim.get_other_channels, board_id, True)
}

for key, value in label_dict.items():
    for count, channel in enumerate(value):
        label_list[channel] = key +  " " + str(count) if len(value) > 1 else key

if (create_csv):
    with open(output_file, 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(np.arange(BoardShim.get_num_rows(board_id)))
        writer.writerow(["Sampling Rate: " + str(BoardShim.get_sampling_rate(board_id)) + " Hz"])
        writer.writerow(["Board: " + BoardShim.get_device_name(board_id)])
        writer.writerow(label_list)

time.sleep(display_interval/1000)
ani = FuncAnimation(plt.gcf(), animate, fargs = (board, ), interval = display_interval)
plt.show()

board.stop_stream()
board.release_session()
