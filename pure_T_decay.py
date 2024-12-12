import numpy as np
from vlqBounds.models import PureT
from vlqBounds import VLQBounds


def main():
    p = PureT()
    vb = VLQBounds(p)
    vb.initialize_xs_data()
    mT_range = np.arange(800, 2000, 1)
    for mT in mT_range:
        vb.pure_T_to_Ht(mT)
        vb.check_against_xs_limits()

    vb.get_key()


main()

