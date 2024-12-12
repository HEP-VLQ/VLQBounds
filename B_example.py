import numpy as np
from vlqBounds.models import SingletB
from vlqBounds import VLQBounds


def main():
    s = SingletB()
    pt = VLQBounds(s)
    pt.initialize_coupling_bounds()
    m_range = np.arange(800, 2000, 2)
    for k in np.linspace(1e-2, 1.4, 40):
        for m in m_range:
            params = {
                    "mB": m,
                    "k_B": k
            }
            pt.singletB_params(**params)
            pt.check_against_coupling_limits()
    pt.get_key()
    #pt.df.to_csv("../../singletB_cms_single_prod.txt", sep=' ')


main()
