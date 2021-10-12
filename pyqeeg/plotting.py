
def plot_coherence(all_cohr, band_info):
    for connection, coherence in all_cohr.items():
        plot_connection_coherence(connection, coherence)


def plot_connection_coherence(connection, coherence):
    pass


def plot_spectra(all_spectra, band_info):
    for channel, spectrum in all_spectra.items():
        plot_spectrum(channel, spectrum)


def plot_spectrum(channel, spectrum):
    pass


