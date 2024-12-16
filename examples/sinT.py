import numpy as np
from src.models import SingletT
from src import VLQBounds


def main():
    s = SingletT()
    vb = VLQBounds(s)
    vb.initialize_vlq_bounds()
    m_range = np.arange(800, 2001, 2)
    for w in np.linspace(1e-6, 0.3, 20):
        for m in m_range:
            vb.singletT_params(mT=m, w_m=w)
            vb.check_against_xs_and_coupling_limits()
            vb.print_result()
    vb.get_key()
    vb.df.to_csv("data/sinT_res_width_to_mass.dat", sep=" ")


main()
