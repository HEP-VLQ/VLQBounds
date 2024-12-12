import numpy as np
from vlqBounds.models import SingletT
from vlqBounds import VLQBounds


def main():
    s = SingletT()
    pt = VLQBounds(s)
    pt.initialize_vlq_bounds()
    mT_range = np.arange(800, 2200, 10)
    sin_range = np.linspace(0.4, 1, 30)
    for s_L in sin_range:
        for m_T in mT_range:
            pt.singletT_params(mT=m_T, k_T=s_L)
            pt.check_against_xs_and_coupling_limits()
        pt.get_key()


main()
