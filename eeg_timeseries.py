import pygame
from numpy import absolute, arange
import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
from matplotlib import style
from collections import deque
from math import *
from pylsl import StreamInlet, resolve_stream
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show
from time import sleep
import bandpass_dsp_fir_filter


# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create a new inlet to read from the stream
total_channels = 3
channel = 0
inlet = StreamInlet(streams[channel])
duration = 3


def test_lsl_sampling_rate():
    start = time.time()
    numSamples = 0
    validSamples = 0
    numChunks = 0

    while time.time() <= start + duration:
        # get chunks of samples
        samples, timestamp = inlet.pull_chunk()

        if samples:
            numChunks += 1
            print(len(samples))
            numSamples += len(samples)
            #print(samples)
            validSamples +=1

    print("Number of Chunks == {}".format(numChunks))
    print("Valid Samples and Duration == {} / {}".format(validSamples, duration))
    print("Avg Sampling Rate == {}".format(numSamples/duration))


def test_lsl_pulse_data(inlet, channel):
    start = time.time()
    raw_pulse_signal = []

    while time.time() <= start + duration:
        chunk, timestamp = inlet.pull_chunk()
        if timestamp:
                for sample in chunk:
                    #print(sample)
                    raw_pulse_signal.append(sample[channel])

    filtered_pulse_signal = bandpass_dsp_fir_filter.lfilter(bandpass_dsp_fir_filter.taps, 1.0, raw_pulse_signal)
    bins = len(raw_pulse_signal)
    shift = round((bandpass_dsp_fir_filter.N-1) / bandpass_dsp_fir_filter.sample_rate)
    t = arange(bins) / bandpass_dsp_fir_filter.sample_rate
    #print(raw_pulse_signal)
    #print(filtered_pulse_signal)

    print("Avg Sampling Rate == {}".format(len(raw_pulse_signal) / duration))

    x = t[bandpass_dsp_fir_filter.N-shift:]
    y = filtered_pulse_signal[bandpass_dsp_fir_filter.N-shift:]

    return x, y


loop = True
while loop:

    x_0, y_0 = test_lsl_pulse_data(inlet, 0)

    x_1, y_1 = test_lsl_pulse_data(inlet, 1)

    x_2, y_2 = test_lsl_pulse_data(inlet, 2)

    x_3, y_3 = test_lsl_pulse_data(inlet, 3)

    plt.subplot(4, 1, 1)
    plt.plot(x_0, y_0)
    ylim(-30, 30)
    plt.title('Channel 1')
    plt.xlabel('Time [s]')
    plt.ylabel('Analog Signal [uV]')

    plt.subplot(4, 1, 2)
    plt.plot(x_1, y_1)
    ylim(-30, 30)
    plt.title('Channel 2')
    plt.xlabel('Time [s]')
    plt.ylabel('Analog Signal [uV]')

    plt.subplot(4, 1, 3)
    plt.plot(x_2, y_2)
    ylim(-30, 30)
    plt.title('Channel 3')
    plt.xlabel('Time [s]')
    plt.ylabel('Analog Signal [uV]')

    plt.subplot(4, 1, 4)
    plt.plot(x_3, y_3)
    ylim(-30, 30)
    plt.title('Channel 4')
    plt.xlabel('Time [s]')
    plt.ylabel('Analog Signal [uV]')

    plt.show()
    #plt.pause(3)
    #plt.close('all')

