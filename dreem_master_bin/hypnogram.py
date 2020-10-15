""" Hypnogram utils functions.

hypnogram_to_epoch
find_stages_period
merge_close_periods
intersect_periods

"""
# encoding: utf-8
import numpy as np
from dreem_master_bin.utils import datetime_to_nightsec

stage_colors = [(0.5, 0.2, 0.1), (0.5, 0.3, 1), (1, 0.5, 1), (0.8, 0, 0.7), (0.1, 0.7, 0)]


def plot_hypnogram(
        hypnogram_i,
        axe_plot=None,
        binsize=30,
        rescale=3600,
        start_time=0,
        title='Hypnogram',
):
    ytick_substage = [4, 2, 1.5, 1, 3, 4.7]
    ylabel_substage = ['N3', 'N2', 'N1', 'REM', 'WAKE', '']

    # data
    hypnogram = np.array(hypnogram_i)
    start_hour = datetime_to_nightsec(start_time)
    if np.isnan(start_hour):
        start_hour = 0
    hypnogram[hypnogram < 0] = 5
    hypnogram[hypnogram > 4] = 5
    x_hypno = (np.arange(len(hypnogram)) * binsize + start_hour) / rescale
    graph_hypno = np.asarray([ytick_substage[stage] for stage in hypnogram])

    # plot
    if axe_plot is None:
        fig, axs = plt.subplots(1, 1, figsize=(9, 7))
        ax = np.ravel(axs)[0]
    else:
        ax = axe_plot

    ax.set_title(title)
    ax.step(x_hypno, graph_hypno, 'k', linewidth=0.5)
    # colors
    for stage in range(5):
        xs = x_hypno[hypnogram == stage]
        ys = graph_hypno[hypnogram == stage]
        ax.scatter(xs, ys, s=5, c=np.array([stage_colors[stage]]), marker='s', linewidths=0.0)

    tmp = range(-8, 24, 2)
    ax.set_xticks(tmp)
    ax.set_xticklabels([t % 24 for t in tmp])
    ax.set_yticks(np.sort(ytick_substage))
    ax.set_yticklabels(ylabel_substage)
    ax.set_ylim(0, 6)
    ax.set_xlim(min(x_hypno), max(x_hypno))

    if axe_plot is None:
        fig.show()

    return ax
