"""
Spectrogram functions.
"""
import numpy as np
import matplotlib.pyplot as plt
from lspopt import spectrogram_lspopt
from matplotlib.colors import Normalize
from dreem_master_bin.utils import datetime_to_nightsec

# Set default font size to 12
plt.rcParams.update({'font.size': 12})

frequency_bands = {
    'delta': [0.5, 4],
    'theta': [4, 8],
    'lowfreq': [0.5, 8],
    'alpha': [8, 12],
    'sigma': [11, 15],
    'beta': [15, 18],
    'kcomp': [0.9, 11]
}


def compute_spectrogram(eeg_data, fs, win_sec=30, fmin=0.5, fmax=18):
    """
    Compute spectrogram from EEG 1D-array
    """
    # Calculate multi-taper spectrogram
    nperseg = int(win_sec * fs)
    assert eeg_data.size > 2 * nperseg, 'Data length must be at least 2 * win_sec.'
    f, t, Sxx = spectrogram_lspopt(eeg_data, fs, nperseg=nperseg, noverlap=0)
    Sxx = 10 * np.log10(Sxx)  # Convert uV^2 / Hz --> dB / Hz

    # Select only relevant frequencies (up to 30 Hz)
    good_freqs = np.logical_and(f >= fmin, f <= fmax)
    Sxx = Sxx[good_freqs, :]
    f = f[good_freqs]

    return Sxx, t, f


def plot_spectrogram(spectrogram_array,
                     times,
                     frequencies,
                     trimperc=2.5,
                     cmap='RdBu_r',
                     axe_plot=None,
                     rescale=3600.,
                     start_time=0,
                     title='spectrogram',
                     colourbar=None):
    """
    plot spectrogram
    """
    # data
    t, f, Sxx = times, frequencies, spectrogram_array
    start_hour = datetime_to_nightsec(start_time)
    if np.isnan(start_hour):
        start_hour = 0
    t = (t + start_hour) / rescale

    # Normalization
    vmin, vmax = np.percentile(Sxx, [0 + trimperc, 100 - trimperc])
    norm = Normalize(vmin=vmin, vmax=vmax)

    # axes
    if axe_plot is None:
        fig, axs = plt.subplots(1, 1, figsize=(12, 4))
        ax = np.ravel(axs)[0]
    else:
        ax = axe_plot

    im = ax.pcolormesh(t, f, Sxx, norm=norm, cmap=cmap, antialiased=True, shading='auto')
    tmp = range(-8, 24, 2)
    ax.set_xticks(tmp)
    ax.set_xticklabels([t % 24 for t in tmp])
    ax.set_xlim(t[0], t[-1])
    ax.set_ylabel('Frequency [Hz]')
    ax.set_ylim(0, 15)
    ax.set_title(title)

    # Add colorbar
    if colourbar:
        cbar = plt.colorbar(im, ax=ax, cax=colourbar, shrink=0.95, fraction=0.1, aspect=25)
        cbar.ax.set_ylabel('Log Power (dB / Hz)', rotation=270, labelpad=20)

    if axe_plot is None:
        fig.show()

    return ax
