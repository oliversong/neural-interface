from numpy import cos, sin, pi, absolute, arange
from scipy.signal import kaiserord, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show


# ------------------------------------------------
# Create a signal for testing.
# ------------------------------------------------

sample_rate = 250
n_samples = 1000
t = arange(n_samples) / sample_rate
x = 0.9*cos(2*pi*0.024*t) + 0.2*sin(2*pi*2.5*t+0.1) + \
        0.2*sin(2*pi*15.3*t) + 0.1*sin(2*pi*16.7*t + 0.1) + \
            0.1*sin(2*pi*23.45*t+.8)


# ------------------------------------------------
# Create a FIR filter and apply it to x.
# ------------------------------------------------

# The Nyquist rate of the signal.
nyq_rate = sample_rate / 2.0

# The cutoff frequency of the filter.
cutoff_hz = 13.0

# The passband frequency of the filter.
pass_hz = 7.0

# The desired width of the transition from pass to stop,
# relative to the Nyquist rate.
width = (cutoff_hz - pass_hz)/nyq_rate

# The desired attenuation in the stop band, in dB.
ripple_db = 90.0

# Compute the order for the FIR filter.
N, beta = kaiserord(ripple_db, width)
beta = round(beta)

# Use firwin with a nuttall window to create a bandpass FIR filter.
taps = firwin(N, [pass_hz/nyq_rate, cutoff_hz/nyq_rate], pass_zero=False, window=('kaiser', beta))

# Use lfilter to filter x with the FIR filter.
filtered_x = lfilter(taps, 1.0, x)

# Print filter coefficients into python console for viewing.
print("The FIR filter has", len(taps), "coefficients")
print("\n")
print("The following values are the coefficients of the filter: \n")
print(taps)
print("\n")
print("The beta value for the kaiser window is : \n")
print(beta)
# ------------------------------------------------
# Plot the FIR filter coefficients.
# ------------------------------------------------

figure(1)
plot(taps, 'bo-', linewidth=2)
title('Filter Coefficients (%d taps)' % N)
grid(True)

# ------------------------------------------------
# Plot the magnitude response of the filter.
# ------------------------------------------------

figure(2)
clf()
w, h = freqz(taps, worN=8000)
plot((w/pi)*nyq_rate, absolute(h), linewidth=2)
xlabel('Frequency (Hz)')
ylabel('Gain')
title('Frequency Response')
ylim(-0.05, 1.05)
grid(True)

# Upper inset plot.
ax1 = axes([0.42, 0.6, .45, .25])
plot((w/pi)*nyq_rate, absolute(h), linewidth=2)
xlim(0, 50.0)
ylim(0.9985, 1.001)
grid(True)

# Lower inset plot
ax2 = axes([0.42, 0.25, .45, .25])
plot((w/pi)*nyq_rate, absolute(h), linewidth=2)
xlim(12.0, 50.0)
ylim(0.0, 0.05)
grid(True)

# ------------------------------------------------
# Plot the original and filtered signals.
# ------------------------------------------------

# The phase delay of the filtered signal.
delay = 0.5 * (N-1) / sample_rate

figure(3)
# Plot the original signal.
plot(t, x)
# Plot the filtered signal, shifted to compensate for the phase delay.
plot(t-delay, filtered_x, 'r-')
# Plot just the "good" part of the filtered signal.  The first N-1
# samples are "corrupted" by the initial conditions.
plot(t[N-1:]-delay, filtered_x[N-1:], 'g', linewidth=4)

xlabel('t')
grid(True)

show()
