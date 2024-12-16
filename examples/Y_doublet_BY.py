import numpy as np
from src.models import DoubletY
from src import VLQBounds


def main():
    d = DoubletY()
    vlq = VLQBounds(d)
    vlq.initialize_vlq_bounds()
    m_range = np.arange(800, 2001, 200)
    for m in m_range:
        s = np.random.uniform(1e-03, 0.6)
        vlq.doubletY_BY_params(mY=m, s_r=s)
        vlq.check_against_xs_and_coupling_limits()
        vlq.print_result()


main()

