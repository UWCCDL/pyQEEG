import numpy as np
from sklearn.linear_model import LinearRegression


def connection(elem1, elem2):
    if elem1 > elem2:
        return f"{elem2}_{elem1}"
    return f"{elem1}_{elem2}"


def bounds_ok(sub, lower, upper):
    return (min(sub) >= lower) and (max(sub) <= upper)


def blink_ok(bsub):
    return np.all(bsub <= 0.5)


def qual_ok(qsub):
    return min(qsub) > 1


def detrend_data(series, gyro_x, gyro_y):
    y = series.reshape(-1, 1)
    X = np.array(range(len(series))).reshape(-1, 1)
    model = LinearRegression().fit(X, y)
    y -= model.predict(X)
    if gyro_x is not None and gyro_y is not None:
        X = np.array([[value1, value2] for value1, value2 in zip(gyro_x, gyro_y)])
        model = LinearRegression().fit(X, y)
        y -= model.predict(X)
    return y.reshape(-1)


def get_bounds(arr):
    m = np.mean(arr)
    sd = np.std(arr, ddof=1)
    lower = m - 3 * sd
    upper = m + 3 * sd
    return lower, upper


def longest_quality(qual, sampling):
    qual[qual >= 3] = 3

    def rle(arr):
        """
        Run length encoding.
        :return: tuple (runlengths, startpositions, values)
        """
        y = arr[1:] != arr[:-1]  # pairwise unequal (string safe)
        i = np.append(np.where(y), len(arr) - 1)  # must include last element pos
        z = np.diff(np.append(-1, i))  # run lengths
        p = np.cumsum(np.append(0, z))[:-1]  # positions
        return z, p, arr[i]

    length, pos, val = rle(qual)
    if 3 in val:
        return max(length[val == 3]) / sampling
    return 0


def get_channels_with_bad_spectrum(all_spectra):
    result = []
    average_channel_power = {channel: np.mean(spectrum.power) for channel, spectrum in all_spectra.items()}
    lower, upper = get_bounds([average for channel, average in average_channel_power.items()])
    for channel, average in average_channel_power.items():
        if average > upper or average < lower:
            result.append(channel)
    return result
