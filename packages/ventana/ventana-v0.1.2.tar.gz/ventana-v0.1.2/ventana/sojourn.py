"""
Sojourn
=============
Defines methods for classifying activity levels based on a second-by-second input using sojourn methods.

Provides 1x and 3x methods for validation purposes
"""

import numpy as np
from ventana.METs import cr2_mets

sit_cut = 90
act_cut = 10
cut_1 = 0.05
cut_2 = 0.12
cut_3 = 0.55

def yield_sojourns(values):
    running = []
    flag = True if values[0] > 0. else False
    for value in values:
        if (value > 0) == flag:
            running.append(value)
        else:
            yield running
            running = [value]
            flag = not flag

def is_too_short_undet(ident, length):
    return (ident == "undetermined") and (length < act_cut)

def combine_sojourns(clean_s, clean_id):
    skip = False
    for i, soj in enumerate(clean_s):
        if skip:
            skip = False
            continue
        if is_too_short_undet(clean_id[i], len(soj)):
            if (i == 0) or (i + 1 == len(clean_id)):
                yield soj, "undetermined"
            elif clean_id[i - 1] == clean_id[i + 1]:
                yield clean_s[i - 1] + soj + clean_s[i + 1], clean_id[i - 1]
                skip = True
            else:
                yield clean_s[i - 1] + soj, clean_id[i - 1]
        else:
            if (i + 1 < len(clean_id)) and is_too_short_undet(clean_id[i + 1], len(clean_s[i + 1])):
                continue
            yield soj, clean_id[i]



def clean_sojourns(sojourns, identity):
    j = 0
    clean_s = []
    clean_id = []
    for i in range(len((identity))):
        if j > 0:
            j -= 1
            continue
        if (i + 1 < len(identity)) and (identity[i] == identity[i + 1]):
            x = sojourns[i]
            j = 0
            while (i + j + 1 < len(identity)) and (identity[i + j] == identity[i + j + 1]):
                x.extend(sojourns[i + j + 1])
                j += 1
            clean_s.append(x)
            clean_id.append(identity[i])
        else:
            clean_s.append(sojourns[i])
            clean_id.append(identity[i])
    return combine_sojourns(clean_s, clean_id)

def sojourn_1x(counts):
    """
    Sojourn second-by-second estimation of METs based on second-by-second vertical counts

    :param counts: Second-by-second vertical counts (numbers)
    :type counts: list
    :return: Second-by-second estimation of METs (floats)
    :rtype: list
    """
    base_identity = []
    sojourns = []
    for sojourn in yield_sojourns(counts):
        if (sojourn[0] == 0) and (len(sojourn) > sit_cut):
            base_identity.append("sedentary")
        elif (sojourn[0] != 0) and (len(sojourn) > act_cut):
            base_identity.append("activity")
        else:
            base_identity.append("undetermined")
        sojourns.append(sojourn)
    pred = []
    for sojourn, level in clean_sojourns(sojourns, base_identity):
        # four options
        # sendentary / undetermined can fall into one of three options
        # activity used MET method
        mets = []
        if level == "activity":
            mets = cr2_mets(sojourn)
        else:
            val_cut = np.mean(sojourn)
            if val_cut > cut_3:
                mets = cr2_mets(sojourn)
            elif (val_cut > cut_1) and (val_cut <= cut_2) and (len(sojourn) > sit_cut):
                mets = [1.2] * len(sojourn)
            elif (val_cut > cut_1) and (val_cut <= cut_2) and (len(sojourn) <= sit_cut):
                mets = [1.5] * len(sojourn)
            elif (val_cut > cut_2) and (val_cut <= cut_3):
                mets = [1.7] * len(sojourn)
            else:
                mets = [1.0] * len(sojourn)
        pred.extend(mets)
    return pred