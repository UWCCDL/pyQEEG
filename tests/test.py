import numpy as np
import pytest

from pyqeeg.analysis import run_analysis


all_spectra, net_spectra, all_cohr, net_cohr, summary = run_analysis(subject="test",
                                                                      session="rest",
                                                                      filename="tests/test_data/test_rest.txt",
                                                                      min_samples_for_inclusion=33,
                                                                      return_object=True)


def test_spectra():
    with open("tests/test_data/test_rest_spectra.txt", "r") as file:
        header = file.readline()
        for line in file.readlines():
            values = line.strip().split("\t")
            channel = values[1]
            real_spectrum = [float(v) for v in values[2:]]
            if channel in all_spectra.keys():
                computed_spectrum = all_spectra[channel].power
            else:
                computed_spectrum = net_spectra[channel]
            assert np.isclose(real_spectrum, computed_spectrum).all()


# def test_coherence():
#     with open("tests/test_data/test_rest_coherence.txt", "r") as file:
#         header = file.readline()
#         for line in file.readlines():
#             values = line.strip().split("\t")
#             connection = values[1]
#             real_coherence = [float(v) if v != "NA" else np.nan for v in values[2:]]
#             if connection in all_cohr.keys():
#                 computed_coherence = all_cohr[connection].coherence
#             else:
#                 computed_coherence = net_cohr[connection]
#             assert equal(real_coherence, computed_coherence)


def test_summary():
    with open("tests/test_data/test_rest_summary.txt", "r") as file:
        keys = file.readline().strip().split("\t")
        values = []
        for value in file.readline().strip().split("\t"):
            try:
                values.append(float(value))
            except ValueError:
                values.append(value)

    for key, value in zip(keys, values):
        if not "coherence" in key:
            if isinstance(value, float):
                assert np.isclose(summary.data[key], value)
            else:
                assert summary.data[key] == value
