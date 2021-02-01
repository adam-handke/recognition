from __future__ import division
import sys
import scipy.io.wavfile
from pylab import *
from numpy import *
from scipy import *
from scipy import signal

file = sys.argv[1]
w, input_data = scipy.io.wavfile.read(file)
data = []

# Controlling if data is stereo or mono

try:
    tmp = input_data[0, 0]
    # stereo - using only first channel
    data = input_data[:, 0]
except IndexError:
    # mono - using whole data
    data = input_data

# High-pass filter
filter_stop = 90
filter_pass = 100
filter_order = 1001
rate = w / 2.0
filter_coefficients = signal.firls(filter_order, (0, filter_stop, filter_pass, rate), (0, 0, 1, 1), nyq=rate)
filtered_data = signal.filtfilt(filter_coefficients, [1], data)

fft_data = fft.fft(filtered_data)

# Harmonic product spectrum method
order = 4
min_freq = 50
freq = np.zeros(fft_data.shape[0])

length = int((fft_data.shape[0] - 1) / order)
hps_data = fft_data[np.arange(0, length)]
min_length = int(round(min_freq / w * 2 * (fft_data.shape[0] - 1)))

for i in range(1, order):
    tmp_data = fft_data[::(i + 1)]
    hps_data *= tmp_data[np.arange(0, length)]

freq = np.argmax(hps_data[np.arange(min_length, hps_data.shape[0])], axis=0)

base_freq = (freq + min_length) / (fft_data.shape[0] - 1) * w

# Comparison with an empirically set threshold (based on a training set)
if base_freq > 173:
    gender = 'F'
else:
    gender = 'M'

print(gender, ', ', round(base_freq, 2), " Hz", sep='')
