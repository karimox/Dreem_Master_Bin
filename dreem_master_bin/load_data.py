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
        'eeg_1': 'channel1/visualization',
        'eeg_2': 'channel2/visualization',
        'hypnogram': 'algo/dreemnogram',
        'accelerometer': 'accelerometer/norm',
        'x_acc': 'accelerometer/x',
        'y_acc': 'accelerometer/y',
        'z_acc': 'accelerometer/z'
    }

    results = {}
    with h5py.File(filename, "r") as fi:
        for key, field in fields.items():
            results[key] = fi[field][()]
        results['start_time'] = fi.attrs['start_time']
    return results
