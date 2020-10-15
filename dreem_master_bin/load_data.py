""" Load sleep records

"""
import os
import h5py
import numpy as np

from td_dreem_bin import path_repo

path_records = os.path.join(path_repo, "data", "Records/")

list_record = [1934791, 1980547, 1989860, 1994755, 2020368]


def get_one_record(record):
    """ load one Dreem record"""
    filename = path_records + str(record) + '.h5'
    fields = {
        'eeg': 'eeg',
        'hypnogram': 'hypnogram',
        'accelerometer': 'accelerometer',
        'spectrogram': 'spectrogram/spectrogram',
        't': 'spectrogram/t',
        'freq': 'spectrogram/freq',
        'fs': 'sampling_frequency',
        'start_time': 'start_time'
    }

    results = {}
    with h5py.File(filename, "r") as fi:
        for key, field in fields.items():
            results[key] = fi[field][()]
    return results
