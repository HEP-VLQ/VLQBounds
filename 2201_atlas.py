import numpy as np
from vlqBounds.models import SingletT
from vlqBounds import VLQBounds


def main():
    s = SingletT()
    vlq = VLQBounds(s)
    vlq.initialize_xs_data()
    mT_range = np.arange(1000, 2301, 1)
    sin_range = np.linspace(0.1, 1.1, 40)
    for k in sin_range:
        for m_T in mT_range:
            vlq.singletT_params(mT=m_T, k_T=k)
            vlq.check_against_xs_limits()
    vlq.df.to_csv("~/data/2201.dat", sep=' ')

 main()
