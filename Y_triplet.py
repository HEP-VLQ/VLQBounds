import numpy as np
from vlqBounds.models import TripletY
from vlqBounds import VLQBounds


def main():
    t = TripletY()
    vlq = VLQBounds(t)
    vlq.initialize_vlq_bounds()
    m_range = np.arange(800, 2001, 2)
    s_d_l_range = np.linspace(1e-4, 1, 30)
    for s_d_l in s_d_l_range:
        for m in m_range:
            vlq.tripletY_TBY_params(mY=m, s_d_l=s_d_l)
            vlq.check_against_xs_and_coupling_limits()
    vlq.df.to_csv("~/data/Y_triplet.dat", sep=' ')
    vlq.get_key()

main()
