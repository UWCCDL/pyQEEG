from pyqeeg.analysis import run_analysis


if __name__ == '__main__':
    all_spectra, network_spectra, all_cohr, network_cohr, summmary = run_analysis(subject="test",
                                                                                  session="rest",
                                                                                  min_samples_for_inclusion=33,
                                                                                  return_object=True)

