from numba import jit

import numpy as np

__version__ = "0.0.3"

@jit
def inv_mass_pt_eta_phi(pt1, eta1, phi1, pt2, eta2, phi2):
    return np.sqrt(2 * pt1 *pt2 * (np.cosh(eta1-eta2) - np.cos(phi2-phi1)))

@jit
def calculate_jet_ht(jet_pt):
    """Calculate HT
    
    HT is calculated as the scalar sum of jet transverse momenta
    :param jet_pt: JaggedArray of jet PTs in all events
    :type jet_pt: JaggedArray
    :return: Array with HT values for each event
    :rtype: numpy.array
    """
    nevent = len(jet_pt)
    ret = np.empty(nevent)
    for i in range(nevent):
        ret[i] = np.sum(jet_pt[i])
    return ret
