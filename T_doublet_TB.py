import numpy as np
from vlqBounds.models import DoubletT, DoubletB
from vlqBounds import VLQBounds


def main():
    dT = DoubletT()
    vb1 = VLQBounds(dT)
    dB = DoubletB()
    vb2 = VLQBounds(dB)
    vb1.initialize_vlq_bounds()
    vb2.initialize_vlq_bounds()
    for i in range(2000):
        print("i:", i)
        s = np.random.uniform(0, 0.8)
        m = np.random.uniform(1400, 2000)
        vb1.doubletT_TB_params(mT=m, s_u_r=s)
        vb1.check_against_xs_and_coupling_limits()
        vb1.print_result()
        vb2.doubletB_TB_params(mB=m, s_d_r=s)
        vb2.check_against_xs_and_coupling_limits()
        vb2.print_result()
    vb1.df.to_csv("~/data/T_doublet_wm1.dat", sep=' ')
    vb2.df.to_csv("~/data/B_doublet_wm2.dat", sep=' ')
    #vb.get_key()


main()

