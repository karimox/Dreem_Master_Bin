"""
Plotting functions of YASA.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dreem_master_bin.utils import datetime_to_nightsec


def compute_movement_variance(data, fs=50., buff_len_sec=1, computation_delay=0.1):
    """
    variance from accelerometer data
    """

    data = pd.DataFrame(data, columns=['x', 'y', 'z'])
    npts_var = int(fs * buff_len_sec)
    mov_variance = data.rolling(npts_var).var()
    npts_compute = int(fs * computation_delay)
    mov_variance = mov_variance.groupby(mov_variance.index // npts_compute).max()
    mov_variance = mov_variance.to_numpy()

    sampling_frequency = 1. / computation_delay

    return mov_variance, sampling_frequency


def movement_from_variance(mov_variance, thresh_var_light=0.000186, thresh_var_strong=0.02):

    little_movement = np.zeros(mov_variance.shape[0])
    strong_movement = np.zeros(mov_variance.shape[0])

    max_variance = np.max(mov_variance, 1)
    idx_little = np.logical_and(max_variance >= thresh_var_light, max_variance <= thresh_var_strong)
    idx_strong = max_variance >= thresh_var_strong

    little_movement[idx_little] = 1
    strong_movement[idx_strong] = 1

    return little_movement, strong_movement


def plot_accelerometer(accelerometer_array,
                       axe_plot=None,
                       fs=50.,
                       rescale=3600.,
                       start_time=0,
                       color='k',
                       y_label='accelero var',
                       title='movement'):
    """
    plot accelerometer norm
    """

    start_hour = datetime_to_nightsec(start_time)
    if np.isnan(start_hour):
        start_hour = 0
    t = np.arange(0, len(accelerometer_array)) / fs
    t = (t + start_hour) / rescale

    if axe_plot is None:
        fig.show()

    # axes
    if axe_plot is None:
        fig, axs = plt.subplots(1, 1, figsize=(12, 4))
        ax = np.ravel(axs)[0]
    else:
        ax = axe_plot

    ax.plot(t, accelerometer_array, color=color)

    tmp = range(-8, 24, 2)
    ax.set_xticks(tmp)
    ax.set_xticklabels([t % 24 for t in tmp])
    ax.set_xlim(t[0], t[-1])
    ax.set_ylabel(y_label)
    ax.set_title(title)

    return ax
