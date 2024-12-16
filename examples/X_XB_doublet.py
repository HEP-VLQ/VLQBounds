import numpy as np
from src.models import DoubletX
from src import VLQBounds
import random


def main():
    d = DoubletX()
    vlq = VLQBounds(d)
    vlq.initialize_vlq_bounds()
    m_range = np.arange(600, 2001, 200)
    for m in m_range:
        s = random.choice(np.linspace(1e-3, 0.6, 10))
        vlq.doubletX_XT_params(mX=m, s_r=s)
        vlq.check_against_xs_and_coupling_limits()
    vlq.get_key()


main()

