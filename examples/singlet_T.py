import numpy as np
from vlqBounds.models import SingletT
from vlqBounds import VLQBounds


def main():
    s = SingletT()
    pt = VLQBounds(s)
    pt.filling_couplings_and_xs_limits()
    m_range = np.arange(800, 2200, 200)
    for m in m_range:
        params = {
                "mT": m,
                "s_l": 0.3
        }
        pt.singletT_params(**params)
        pt.check_against_xs_and_coupling_limits()
    pt.get_key()


main()
