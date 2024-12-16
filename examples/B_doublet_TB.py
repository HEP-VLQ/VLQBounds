import numpy as np
from src.models import DoubletB
from src import VLQBounds


def main():
    d = DoubletB()
    vb = VLQBounds(d)
    vb.initialize_vlq_bounds()
    for i in range(2000):
        print("i:", i)
        s = np.random.uniform(0,0.8)
        m = np.random.uniform(1400, 2000)
        vb.doubletB_TB_params(mB=m, s_d_r=s)
        vb.check_against_xs_and_coupling_limits()
        vb.print_result()
    vb.df.to_csv("~/data/B_doublet_wm.dat", sep=' ')
    vb.get_key()


main()

