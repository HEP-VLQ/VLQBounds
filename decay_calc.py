from utils import *


def calculate_decay_width(involved_masses: list, sin_angle=None, kappa=None, width_ratio=None, coupling=None,
                          decay_constants=None, to_higgs=False):
    m_vlq, m_A, m_q = involved_masses
    if to_higgs:
        if width_ratio is None:
            if kappa is None:
                if sin_angle is not None:
                    width = calculate_width_to_higgs_from_mixing(decay_constants, m_vlq, coupling, m_q)
                    return width
                else:
                    raise Exception("Calculation error: Width, universal coupling, and mixing are all None.")
            else:
                k = kappa / np.sqrt(2)
                width = calculate_width_to_higgs_from_k(decay_constants, m_vlq, k, m_q)
                return width
        else:
            k = kappa_coupling_from_width(m_vlq, width_ratio) / np.sqrt(2)
            width = calculate_width_to_higgs_from_k(decay_constants, m_vlq, k, m_q)
            return width
    else:
        if width_ratio is None:
            if kappa is None:
                if sin_angle is not None:
                    width = calculate_width(decay_constants, m_vlq, m_A, coupling, m_q)
                    return width
                else:
                    raise Exception("Calculation error: Width, universal coupling, and mixing are all None.")
            else:
                k = kappa / np.sqrt(2)
                width = calculate_width(decay_constants, m_vlq, m_A, [k, 0], m_q)
                return width
        else:
            k = kappa_coupling_from_width(m_vlq, width_ratio) / np.sqrt(2)
            width = calculate_width(decay_constants, m_vlq, m_A, [k, 0], m_q)
            return width


def kappa_coupling_from_width(m_vlq: float, width_ratio: float):
    k_vlq = np.sqrt(2) * np.sqrt(width_ratio * m_vlq / ((c.Cst1 * m_vlq / (c.MW ** 2) * np.sqrt(
        lambda_func(m_vlq, c.Mb, c.MW)) * (1 + r_x(c.MW, m_vlq) ** 2 - 2 * r_x(c.Mb, m_vlq) ** 2
                                           - 2 * r_x(c.MW, m_vlq) ** 4 + r_x(c.Mb, m_vlq) ** 4
                                           + r_x(c.Mb, m_vlq) ** 2 * r_x(c.MW, m_vlq) ** 2))
                                           + (c.Cst2 * m_vlq / (c.MZ ** 2) * np.sqrt(lambda_func(m_vlq, c.Mt, c.MZ))
                                              * (1 + r_x(c.MZ, m_vlq) ** 2 - 2 * r_x(c.Mt, m_vlq) ** 2
                                                 - 2 * r_x(c.MZ, m_vlq) ** 4 + r_x(c.Mt, m_vlq) ** 4
                                                 + r_x(c.Mt, m_vlq) ** 2 * r_x(c.MZ, m_vlq) ** 2))
                                           + (c.Cst3 * m_vlq / (c.MW ** 2) * np.sqrt(lambda_func(m_vlq, c.Mt, c.Mh))
                                                                           * (1 + r_x(c.Mt, m_vlq) ** 2
                                                                              - r_x(c.Mh, m_vlq) ** 2))))
    return k_vlq
