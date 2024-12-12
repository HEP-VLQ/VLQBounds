import numpy as np
from vlqBounds.models import DoubletT
from vlqBounds import VLQBounds


def main():
    d = DoubletT()
    vb = VLQBounds(d)
    vb.initialize_vlq_bounds()
    m_range = np.arange(800, 2201, 2)
    k_T_range = np.linspace(1e-4, 1.2, 30)
    for k in k_T_range:
        for m in m_range:
            vb.doubletT_TB_params(mT=m, k_T=k)
            vb.check_against_xs_and_coupling_limits()
    vb.df.to_csv("~/data/T_doublet_kT.dat", sep=' ')
    vb.get_key()


main()

