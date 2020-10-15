""" List of utils functions

"""
# encoding: utf-8
import numpy as np

def datetime_to_nightsec(d_time):
    try:
        new_time = d_time.hour * 3600 + d_time.minute * 60 + d_time.second
        if new_time > 16 * 3600:
            new_time -= 24 * 3600
        return new_time

    except:
        return float('nan')


def generate_timestamps_signals(signals, fs, start_time=None):
    """
    generate time array for a signal
    """
    if start_time:
        start_time_sec = datetime_to_nightsec(start_time)
        if start_time_sec > 3600 * 16:
            start_time_sec -= 24 * 3600
    else:
        start_time_sec = 0

    timestamps = np.arange(0, len(signals)) / fs  # time in sec
    timestamps += start_time_sec

    return timestamps