name = "feelfree"

from matplotlib.mlab import psd, csd


def resample_test():
    return ('resample test')


def tfestimate_test():
    return ('tfestimate test')


def force_test():
    return ('force test')


def location_test():
    return ('location test')


def tfetimate(x, y, fs=None, nfft=None, noverlap=None):
    """estimate transfer function from x to y, see csd for calling convention"""
    return csd(x, y, nfft, fs, None, None, noverlap, None, None, None) / psd(x, nfft, fs, None, None, noverlap, None,
                                                                             None, None)
    # return csd(y, x, *args, **kwargs) / psd(x, *args, **kwargs)
    # return csd_ret / psd_ret
