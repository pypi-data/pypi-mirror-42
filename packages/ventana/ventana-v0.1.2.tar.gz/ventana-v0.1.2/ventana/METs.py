"""
METs
=============
Defines methods for estimating METs on a second-by-second input.

Provides 4 different methods for validation purposes
"""

import numpy as np
from math import log
from ventana.utils import chunks

# solve memory issues
# look to memoize and to reduce iterations

def _get_indices(i, n):
    if i < 5:
        return list(range(0, min(i + 5, n)))
    elif i >= n - 5:
        return list(range(i - 5, n - 1))
    else:
        return list(range(i - 5, i + 5))

def cr2_mets_est(i, val, agg_vals, agg_sum):
    slicer = _get_indices(i, len(agg_sum))
    slice_val = agg_vals[slicer]
    min_val = np.max(slice_val)
    agg_sum_val = agg_sum[i]
    if min_val <= 0:
        return 0.
    elif agg_sum_val <= 8:
        return 1.
    elif min_val <= 10. and min_val > 0. and agg_sum_val > 8:
        return 2.294275 * (0.00084679 * agg_sum_val) ** 2
    elif min_val > 10. and agg_sum_val > 8:
        return 0.749395 + (0.716431 * log(agg_sum_val)) - (0.179874 * (log(agg_sum_val) ** 2)) + (0.033173 * (log(agg_sum_val) ** 3))
    else:
        return 0.

def c_mets_est(i, val, cvs):
    if val > 50 and cvs[i] > 0. and cvs[i] < 10.:
        return 2.379833 * (0.00013529 * val) ** 2
    elif val > 50 and cvs[i] == 0. or cvs[i] > 10.:
        return 2.330519 + 0.001646 * val - ((1.2017 * 10 ** -7.) * val ** 2) + ((3.3779 * 10 ** -12.) * val ** 3)
    else:
        return 1.

def cr2_mets(counts):
    """
    Crouter2 second-by-second estimation of METs based on second-by-second vertical counts

    :param counts: Second-by-second vertical counts (numbers)
    :type counts: list
    :return: Second-by-second estimation of METs (floats)
    :rtype: list
    """
    tmp_chunks = list(chunks(counts, 10))
    agg_vals = np.array([100 * np.std(x) / np.mean(x) if np.mean(x) > 0. else 0. for x in tmp_chunks])
    agg_sum = [np.sum(x) for x in tmp_chunks]
    METs = [cr2_mets_est(i, val, agg_vals, agg_sum) for i, val in enumerate(agg_vals)]
    minute_mets = [np.mean(x) for x in chunks(METs, 6)]
    second_mets = []
    [second_mets.extend([x] * 60) for x in minute_mets]
    return np.array(second_mets)

def c_mets(counts):
    """
    Original crouter second-by-second estimation of METs based on second-by-second vertical counts

    :param counts: Second-by-second vertical counts (numbers)
    :type counts: list
    :return: Second-by-second estimation of METs (floats)
    :rtype: list
    """
    cpm = list(chunks(counts, 60))
    cvs = [100. * np.std(x) / np.mean(x) if np.mean(x) > 0. else 0. for x in cpm]
    METs = [c_mets_est(i, np.sum(val), cvs) for i, val in enumerate(cpm)]
    second_mets = []
    [second_mets.extend([x] * 60) for x in METs]
    return np.array(second_mets)

def sasaki_mets(counts):
    """
    Sasaki second-by-second estimation of METs based on second-by-second vector magnitude counts

    :param counts: Second-by-second vector magnitude counts (numbers)
    :type counts: list
    :return: Second-by-second estimation of METs (floats)
    :rtype: list
    """
    METs = [0.668876 + 0.000863 * np.sum(x) for x in chunks(counts, 60)]
    second_mets = []
    [second_mets.extend([x] * 60) for x in METs]
    return np.array(second_mets)

def freedson_mets(counts):
    """
    Freedson second-by-second estimation of METs based on second-by-second vertical counts

    :param counts: Second-by-second vertical counts (numbers)
    :type counts: list
    :return: Second-by-second estimation of METs (floats)
    :rtype: list
    """
    METs = [1.439008 + 0.000795 * np.sum(x) for x in chunks(counts, 60)]
    second_mets = []
    [second_mets.extend([x] * 60) for x in METs]
    return np.array(second_mets)



