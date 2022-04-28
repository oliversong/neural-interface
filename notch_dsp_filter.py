from numpy import cos, sin, pi, absolute, arange
from scipy.signal import kaiserord, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show


# ------------------------------------------------
# Create a signal for testing.
# ------------------------------------------------

sample_rate = 250.0
n_samples = 500
t = arange(n_samples) / sample_rate
x = 0.9*cos(2*pi*0.48*t)

# ------------------------------------------------
# Create a FIR filter and apply it to x.
# ------------------------------------------------

# The Nyquist rate of the signal.
nyq_rate = sample_rate / 2.0

# The cutoff frequency of the filter.
cutoff_hz = 60.0

# The passband frequency of the filter.
pass_hz = 59.0

# The desired width of the transition from pass to stop,
# relative to the Nyquist rate.
width = (cutoff_hz - pass_hz)/nyq_rate

# The desired attenuation in the stop band, in dB.
ripple_db = 90.0

# Compute the order for the FIR filter.
N = round(ripple_db/(22.0 * width))

# Use firwin to create a bandstop FIR filter.
taps = firwin(N, [pass_hz/nyq_rate, cutoff_hz/nyq_rate])

# Use lfilter to filter x with the FIR filter.
filtered_x = lfilter(taps, 1.0, x)

# Print filter coefficients into python console for viewing.
print("The FIR filter has", len(taps), "coefficients")
print("\n")
print("The following values are the coefficients of the filter: \n")
print(taps)
print("\n")
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

