import numpy as np
from vlqBounds.models import SingletT
from vlqBounds import VLQBounds
import time


def main():
    s = SingletT()
    pt = VLQBounds(s)
    #pt.initialize_vlq_bounds()
    pt.initialize_xs_data()
    m_range = np.arange(800, 2200, 10)
    for m in m_range:
        pt.singletT_params(mT=m, s_l=0.3)
        pt.check_xs_limit()
    pt.get_key()

start = time.time()
main()
end = time.time()

print(end-start) 
