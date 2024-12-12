import numpy as np
from vlqBounds.models import DoubletY
from vlqBounds import VLQBounds


def main():
    d = DoubletY()
    vlq = VLQBounds(d)
    vlq.initialize_vlq_bounds()
    m_range = np.arange(800, 2001, 200)
    #s_R_range = np.linspace(1e-4, 1, 10)
    #for s_R in s_R_range:
    for m in m_range:
        s = np.random.uniform(1e-03, 0.6)
        print(s)
        vlq.doubletY_BY_params(mY=m, s_r=s)
        vlq.check_against_xs_and_coupling_limits()
        vlq.print_result()
    #vlq.df.to_csv("~/data/Y_doublet_s_r.dat", sep=' ')
    #vlq.get_key()

main()

