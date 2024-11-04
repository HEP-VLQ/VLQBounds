import numpy as np
from vlqBounds.models import DoubletB
from vlqBounds import VLQBounds


def main():
    s = DoubletB()
    pt = VLQBounds(s)
    pt.initialize_vlq_bounds()
    '''
    m_range = np.arange(800, 2000, 200)
    for m in m_range:
        params = {
                "mB": m,
                "s_l": 0.1
        }
        pt.singletB_params(**params)
        pt.check_against_xs_and_coupling_limits()
    pt.get_key()
    '''

main()
