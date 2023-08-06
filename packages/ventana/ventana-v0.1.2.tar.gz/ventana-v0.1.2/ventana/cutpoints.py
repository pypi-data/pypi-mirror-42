"""
Cutpoints
=============
Defines methods for classifying activity levels based on a second-by-second input.

Provides 3 different methods for validation purposes
"""

import numpy as np
from ventana.utils import chunks

def freedson_cut(val):
    if val < 100:
        return "sedentary"
    elif val < 1951:
        return "light"
    elif val < 5274:
        return "moderate"
    else:
        return "vigourous"

def freedson(counts):
    """
    Freedson second-by-second classification of activity level based on second-by-second vertical counts

    :param counts: Second-by-second vertical counts (numbers)
    :type counts: list
    :return: Second-by-second classification of activity levels (strings)
    :rtype: list
    """
    minute_est = [freedson_cut(sum(x)) for x in chunks(counts, 60)]
    second_est = []
    [second_est.extend([x] * 60) for x in minute_est]
    return np.array(second_est)

def sasaki_cut(val):
    if val < 2690:
        return "light"
    elif val < 6166:
        return "moderate"
    elif val < 9642:
        return "vigourous"
    else:
        return "very vigourous"

def sasaki(counts):
    """
    Sasaki second-by-second classification of activity level based on second-by-second vertical counts

    :param counts: Second-by-second vertical counts (numbers)
    :type counts: list
    :return: Second-by-second classification of activity levels (strings)
    :rtype: list
    """
    minute_est = [sasaki_cut(sum(x)) for x in chunks(counts, 60)]
    second_est = []
    [second_est.extend([x] * 60) for x in minute_est]
    return np.array(second_est)

def nhanes_cut(val):
    if val < 100:
        return "sedentary"
    elif val < 2019:
        return "light"
    elif val < 5998:
        return "moderate"
    else:
        return "vigourous"

def nhanes(counts):
    """
    Nhanes second-by-second classification of activity level based on second-by-second vertical counts

    :param counts: Second-by-second vertical counts (numbers)
    :type counts: list
    :return: Second-by-second classification of activity levels (strings)
    :rtype: list
    """
    minute_est = [nhanes_cut(sum(x)) for x in chunks(counts, 60)]
    second_est = []
    [second_est.extend([x] * 60) for x in minute_est]
    return np.array(second_est)
    
