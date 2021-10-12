import pandas as pd


def get_spectra_dataframe(subject, freq, all_spectra, network_spectra):
    freq_columns = [f"{x}Hz" for x in freq]
    df = pd.DataFrame(columns=(["Subject", "Channel"] + freq_columns))

    def get_row(channel, spectrum):
        row = {col: power for col, power in zip(freq_columns, spectrum)}
        row["Subject"] = subject
        row["Channel"] = channel
        return row

    for channel, spectrum in all_spectra.items():
        df = df.append(get_row(channel, spectrum.power), ignore_index=True)
    for channel, spectrum in network_spectra.items():
        df = df.append(get_row(channel, spectrum), ignore_index=True)
    return df


def get_coherence_dataframe(subject, freq, all_cohr, network_coherence):
    freq_columns = [f"{x}Hz" for x in freq]
    df = pd.DataFrame(columns=(["Subject", "Connection"] + freq_columns))

    def get_row(connection, coherence):
        row = {col: cohr for col, cohr in zip(freq_columns, coherence)}
        row["Subject"] = subject
        row["Connection"] = connection
        return row

    for connection, coherence in all_cohr.items():
        df = df.append(get_row(connection, coherence.coherence), ignore_index=True)
    for connection, coherence in network_coherence.items():
        df = df.append(get_row(connection, coherence), ignore_index=True)
    return df


def get_excluded_dataframe(subject, session, too_few_samples, no_peak, bad_spectrum, missing_o1_o2):
    df = pd.DataFrame(columns=["Subject", "Session", "Channel", "Reason", "ExcludedFrom"])
    for channel in too_few_samples:
        df = df.append({"Subject": subject,
                        "Session": session,
                        "Channel": channel,
                        "Reason": "Too few samples",
                        "ExcludedFrom": "WholeHeadIAF, Network Power and Coherence"})
    for channel in no_peak:
        df = df.append({"Subject": subject,
                        "Session": session,
                        "Channel": channel,
                        "Reason": "NoPeak",
                        "ExcludedFrom": "WholeHeadIAF"})
    for channel in bad_spectrum:
        df = df.append({"Subject": subject,
                        "Session": session,
                        "Channel": channel,
                        "Reason": "BadSpectrum",
                        "ExcludedFrom": "WholeHeadIAF, Network Power and Coherence"})
    if missing_o1_o2:
        df = df.append({"Subject": subject,
                        "Session": session,
                        "Channel": "All",
                        "Reason": "Missing O1 AND O2",
                        "ExcludedFrom": "Individualized Bands"})
    return df
