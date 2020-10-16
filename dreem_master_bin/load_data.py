""" Load sleep records

"""
import os
import h5py
import numpy as np

from dreem_master_bin import path_repo

path_records = os.path.join(path_repo, "data", "Records/")
path_datasets = os.path.join(path_repo, "data", "datasets/")

list_record = [1934791, 1980547, 1989860, 1994755]


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


def load_spectral_datasets():
    """Load datasets with spectral power."""
    # train
    load_path = os.path.join(path_datasets, "record_datatrain_spectrogram.npz")
    npzfile = np.load(load_path)
    x_train, y_train = npzfile['x_train'], npzfile['y_train']

    # test
    load_path = os.path.join(path_datasets, "record_datatest_spectrogram.npz")
    npzfile = np.load(load_path)
    x_test, y_test = npzfile['x_test'], npzfile['y_test']

    return x_train, y_train, x_test, y_test


def load_feature_datasets():
    """Load datasets with precomputed features."""
    # train
    load_path = os.path.join(path_datasets, "record_datatrain_features.npz")
    npzfile = np.load(load_path)
    x_train, y_train = npzfile['x_train'], npzfile['y_train']

    # test
    load_path = os.path.join(path_datasets, "record_datatest_features.npz")
    npzfile = np.load(load_path)
    x_test, y_test = npzfile['x_test'], npzfile['y_test']

    return x_train, y_train, x_test, y_test
