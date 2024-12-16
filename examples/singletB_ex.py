import numpy as np
from src.models import SingletB
from src import VLQBounds


def main():
    s = SingletB()
    vb = VLQBounds(s)
    vb.initialize_vlq_bounds()
    m_range = np.arange(800, 2001, 2)
    for w in np.linspace(1e-5,  0.3, 30):
        for m in m_range:
            vb.singletB_params(mB=m, w_m=w)
            vb.check_against_xs_and_coupling_limits()
            vb.print_result()
    vb.get_key()


main()

