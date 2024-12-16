import numpy as np
from vlqBounds.models import PureT
from vlqBounds import VLQBounds


def main():
    p = PureT()
    vb = VLQBounds(p)
    vb.initialize_xs_data()
    mT = np.arange(800, 2000, 1)
    for m in mT:
        vb.pure_T_to_Ht(m)
        vb.check_against_xs_limits()
    vb.get_key()


main()

