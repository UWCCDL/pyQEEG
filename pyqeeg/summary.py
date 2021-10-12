import itertools
import numpy as np


def spectral_quality(spectrum, freq, limit=40):
    power = spectrum.power[freq <= limit]
    diffs = power[1:] - power[:-1]
    return np.std(diffs, ddof=1)


def mean_by_band(arr, freq, band):
    #print(freq)
    #print((freq >= band.lower_bound) & (freq < band.upper_bound))
    #print(arr)
    #print(arr[(freq >= band.lower_bound) & (freq < band.upper_bound)])
    return np.mean(arr[(freq >= band.lower_bound) & (freq < band.upper_bound)])


class Summary:
    def __init__(self, subject, version, session, sampling, window, sliding, duration):
        self.data = {
            "Subject": subject,
            "Version": version,
            "Session": session,
            "Sampling": sampling,
            "Window": window,
            "Sliding": sliding,
            "Duration": duration
        }

    def fill_meta_blinks(self, blink):
        blink_onset = blink[1:] - blink[:-1]
        self.data["Meta_Blinks"] = sum(blink_onset[blink_onset > 0])

    def fill_whole_head_iaf(self, whole_head_iaf):
        self.data["WholeHeadIAF"] = whole_head_iaf if whole_head_iaf else np.nan

    def fill_band_method(self, band_method):
        self.data["BandMethod"] = band_method

    def fill_spectra_metrics(self, all_spectra, iafs, bands, freq, network_spectra):
        for channel, iaf in iafs.items():
            self.data[f"{channel}_IAF"] = iaf.freq if iaf.freq else np.nan
            self.data[f"{channel}_IAF_Power"] = iaf.power if iaf.power else np.nan

        for channel, spectrum in all_spectra.items():
            self.data[f"Meta_{channel}_Samples"] = spectrum.good_samples
            self.data[f"Meta_{channel}_LongestQualitySegment"] = spectrum.longest_quality_segment
            self.data[f"Meta_{channel}_SpectralQuality"] = spectral_quality(spectrum, freq)
            for band in bands:
                self.data[f"{channel}_mean_{band.name}_power"] = mean_by_band(spectrum.power, freq, band)

        for network, network_spectrum in network_spectra.items():
            for band in bands:
                self.data[f"{network}_mean_{band.name}_power"] = mean_by_band(network_spectrum, freq, band)

    def fill_coherence_metrics(self, all_cohr, bands, freq, network_coherence):
        for channel_connection, coherence in all_cohr.items():
            for band in bands:
                self.data[f"{channel_connection}_mean_{band.name}_coherence"] = mean_by_band(coherence.coherence, freq, band)

        for network_connection, coherence in network_coherence.items():
            for band in bands:
                self.data[f"{network_connection}_mean_{band.name}_coherence"] = mean_by_band(coherence, freq, band)

    def write_to_file(self, filename):
        with open(filename, "w") as out:
            keys_list = list(self.data.keys())
            out.write("\t".join(keys_list) + "\n")
            out.write("\t".join([str(self.data[key]) for key in keys_list]))
