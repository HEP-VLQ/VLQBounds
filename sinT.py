import numpy as np
from vlqBounds.models import SingletT
from vlqBounds import VLQBounds
import random


def main():
    s = SingletT()
    pt = VLQBounds(s)
    pt.initialize_vlq_bounds()
    m_range = np.arange(800, 2001, 200)
    for m in m_range:
        s = random.choice(np.linspace(1e-3, 0.6, 10))
        pt.singletT_params(mT=m, s_l=s)
        pt.check_against_xs_and_coupling_limits()
        pt.print_result()
    #pt.get_key()


main()
