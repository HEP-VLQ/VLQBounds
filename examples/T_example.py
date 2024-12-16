import numpy as np
from src.models import DoubletT
from src import VLQBounds


def main():
    s = DoubletT()
    pt = VLQBounds(s)
    pt.initialize_coupling_bounds()
    m_range = np.arange(700, 2000, 2)
    for k in np.linspace(1e-3, 1.4, 40):
        for m in m_range:
            pt.singletT_params(mT=m, k_T=k)
            pt.check_against_coupling_limits()
    pt.get_key()


main()

