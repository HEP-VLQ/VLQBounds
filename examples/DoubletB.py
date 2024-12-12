import numpy as np
from vlqBounds.models import DoubletB
from vlqBounds import VLQBounds


def main():
    d = DoubletB()
    vlq = VLQBounds(d)
    vlq.initialize_vlq_bounds()
    m_range = np.arange(800, 2002, 2)
    for k in np.linspace(1e-4, 1, 30):
        for m in m_range:
            vlq.doubletB_BY_params(mB=m, k_B=k)
            vlq.check_against_xs_and_coupling_limits()
    vlq.get_key()
    vlq.df.to_csv("~/doubletB_example.dat", sep=' ')


main()
