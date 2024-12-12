import numpy as np
from vlqBounds.models import SingletB
from vlqBounds import VLQBounds


def main():
    s = SingletB()
    vb = VLQBounds(s)
    vb.initialize_vlq_bounds()
    m_range = np.arange(800, 2001, 2)
    for w in np.linspace(1e-5,  0.3, 30):
        for m in m_range:
            vb.singletB_params(mB=m, w_m=w)
            vb.check_against_xs_and_coupling_limits()
    vb.get_key()
    vb.df.to_csv("~/data/singletB_width_res.dat", sep=' ')


main()

