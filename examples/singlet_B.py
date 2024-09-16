import numpy as np
from vlqBounds.models import SingletB
from vlqBounds import VLQBounds


def main():
    s = SingletB()
    pt = VLQBounds(s)
    pt.set_VLQ_type('B')
    pt.filling_couplings_and_xs_limits()
    m_range = np.arange(800, 2000, 200)
    for m in m_range:
        params = {
                "mB": m,
                "s_l": 0.1
        }
        pt.singletB_params(**params)
        pt.check_against_xs_and_coupling_limits()
    pt.get_key()


main()
