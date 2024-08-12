import constants as c
from utils import *
from theory_XS import *


class SingletB:

    def __init__(self):
        self.__model = 'Singlet'
        self.mB_theo = None
        self.sin_l = None
        self.kappa = None
        self.width_ratio = None

    def set_mB(self, mB):
        self.mB_theo = mB

    def set_sin_l(self, s_l):
        self.sin_l = s_l

    def set_coupling_strength(self, k):
        self.kappa = k

    def set_width_mass_ratio(self, wr):
        self.width_ratio = wr

    def model(self):
        return self.__model

    def get_mB(self):
        return self.mB_theo

    def get_sin_left(self):
        if self.sin_l is not None:
            return self.sin_l
        else:
            if self.kappa is not None:
                return self.kappa / np.sqrt(2)
            else:
                if self.width_ratio is not None:
                    kappa = self.kappa_coupling_from_width()
                    return kappa / np.sqrt(2)

    def get_width_mass_ratio(self):
        if self.width_ratio is None:
            g1 = self.B_decay_to_wt()
            g2 = self.B_decay_to_hb()
            g3 = self.B_decay_to_zb()
            gamma_mv_ratio = (g1 + g2 + g3) / self.mB_theo
            return gamma_mv_ratio
        else:
            return self.width_ratio

    def get_coupling_strength(self):
        if self.width_ratio is None:
            if self.kappa is None:
                return np.sqrt(2) * self.get_sin_left()
            else:
                return self.kappa
        else:
            k = self.kappa_coupling_from_width()
            return k

    def get_xs_pp_QQ(self):
        mB = self.get_mB()
        xs_pp_BB = xs_pp_QQ_theo(mB)
        return xs_pp_BB

    def get_xs_pp_Bbq_tWbq(self, i):
        if i  == 21:
            mT = self.get_mB()
            xs_pp_BtW = xs_pp_Vb_qWb(mT, '2111.10216_Fig4_left_pp_B_Wt_singlet_theo.dat', vlq='B')
            return xs_pp_BtW * 1000

    def get_xs_pp_Btq_tWtq(self, i):
        if i == 22:
            mT = self.get_mB()
            xs_pp_BtW = xs_pp_Vb_qWb(mT, '2111.10216_Fig4_right_pp_Bt_Wt_singlet_theo.dat', vlq='B')
            return xs_pp_BtW * 1000

    def get_xs_pp_Bj_bHj_ts_channels(self, i):
        if i in [15, 16, 17]:
            mT = self.get_mB()
            k = self.get_coupling_strength()
            linear_interp = interp2d_xs_theo('2308.02595', 'singlet', mT, k, vlq='B')
            return linear_interp * 1000


    def get_xs_pp_Bbq_bHbq(self, i):
        if i in [4, 5, 6, 7]:
            mB = self.get_mB()
            w = self.get_width_mass_ratio()
            interp = interp2d_xs_theo('1802.01486', 'singlet', mB, w, vlq='B')
            return interp * 1000

    def get_xs_pp_Bbq_bZbq(self, i):
        if i == 19:
            mB = self.get_mB()
            interp = interp2d_xs_theo('1701.07409_Fig5_right', 'singlet', mB, 0.5, vlq='B')
            return interp * 1000

    def get_xs_pp_Btq_bZtq(self, i):
        if i == 18:
            mB = self.get_mB()
            interp = interp2d_xs_theo('1701.07409_Fig5_left', 'singlet', mB, 0.5, vlq='B')
            return interp * 1000

    def B_decay_to_wt(self):
        constant = c.G ** 2 / (64 * c.PI)
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_l is not None:
                    s_l = self.sin_l

                    gamma = (constant * self.mB_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mt, c.MW))
                             * s_l ** 2 * (1 + r_x(c.MW, self.mB_theo) ** 2 - 2 * r_x(c.Mt, self.mB_theo) ** 2
                             - 2 * r_x(c.MW, self.mB_theo) ** 4 + r_x(c.Mt, self.mB_theo) ** 4
                             + r_x(c.Mt, self.mB_theo) ** 2 * r_x(c.MW, self.mB_theo) ** 2))
                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")
            else:
                gamma = (constant * self.mB_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mt, c.MW))
                         * (self.kappa / np.sqrt(2)) ** 2 * (1 + r_x(c.MW, self.mB_theo) ** 2
                                                             - 2 * r_x(c.Mt, self.mB_theo) ** 2
                                                             - 2 * r_x(c.MW, self.mB_theo) ** 4
                                                             + r_x(c.Mt, self.mB_theo) ** 4
                                                             + r_x(c.Mt, self.mB_theo) ** 2
                                                             * r_x(c.MW, self.mB_theo) ** 2))
                return gamma
        else:
            kappa = self.kappa_coupling_from_width()
            gamma = (constant * self.mB_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mt, c.MW))
                     * (kappa / np.sqrt(2)) ** 2 * (1 + r_x(c.MW, self.mB_theo) ** 2
                                                    - 2 * r_x(c.Mt, self.mB_theo) ** 2
                                                    - 2 * r_x(c.MW, self.mB_theo) ** 4
                                                    + r_x(c.Mt, self.mB_theo) ** 4
                                                    + r_x(c.Mt, self.mB_theo) ** 2
                                                    * r_x(c.MW, self.mB_theo) ** 2))
            return gamma

    def B_decay_to_zb(self):
        constant = c.G ** 2 / (128 * c.PI * c.C_W ** 2)
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_l is not None:
                    s_l = self.sin_l
                    c_l = np.sqrt(1 - s_l ** 2)

                    gamma = (constant * self.mB_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.MZ))
                             * (s_l * c_l) ** 2 * (1 + r_x(c.MZ, self.mB_theo) ** 2 - 2 * r_x(c.Mb, self.mB_theo) ** 2
                             - 2 * r_x(c.MZ, self.mB_theo) ** 4 + r_x(c.Mb, self.mB_theo) ** 4
                             + r_x(c.Mb, self.mB_theo) ** 2 * r_x(c.MZ, self.mB_theo) ** 2))

                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")
            else:
                gamma = (constant * self.mB_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.MZ))
                         * (self.kappa / np.sqrt(2)) ** 2 * (1 + r_x(c.MZ, self.mB_theo) ** 2
                                                             - 2 * r_x(c.Mb, self.mB_theo) ** 2
                                                             - 2 * r_x(c.MZ, self.mB_theo) ** 4
                                                             + r_x(c.Mb, self.mB_theo) ** 4
                                                             + r_x(c.Mb, self.mB_theo) ** 2
                                                             * r_x(c.MZ, self.mB_theo) ** 2))
                return gamma
        else:
            kappa = self.kappa_coupling_from_width()
            gamma = (constant * self.mB_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.MZ))
                     * (kappa / np.sqrt(2)) ** 2 * (1 + r_x(c.MZ, self.mB_theo) ** 2
                                                    - 2 * r_x(c.Mb, self.mB_theo) ** 2
                                                    - 2 * r_x(c.MZ, self.mB_theo) ** 4
                                                    + r_x(c.Mb, self.mB_theo) ** 4
                                                    + r_x(c.Mb, self.mB_theo) ** 2
                                                    * r_x(c.MZ, self.mB_theo) ** 2))
            return gamma

    def B_decay_to_hb(self):
        constant = c.G ** 2 / (128 * c.PI)
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_l is not None:
                    s_l = self.sin_l
                    c_l = np.sqrt(1 - s_l ** 2)
                    gamma = (constant * self.mB_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.Mh))
                             * (s_l * c_l) ** 2 * (1 + 6 * r_x(c.Mb, self.mB_theo) ** 2
                             - r_x(c.Mh, self.mB_theo) ** 2 + r_x(c.Mb, self.mB_theo) ** 4
                             - r_x(c.Mb, self.mB_theo) ** 2 * r_x(c.Mh, self.mB_theo) ** 2))

                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")
            else:
                gamma = (constant * self.mB_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.Mh))
                         * (self.kappa / np.sqrt(2)) ** 2 * (1 + r_x(c.Mb, self.mB_theo) ** 2
                                                             - r_x(c.Mh, self.mB_theo) ** 2))
                return gamma
        else:
            kappa = self.kappa_coupling_from_width()
            gamma = (constant * self.mB_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.Mh))
                     * (kappa / np.sqrt(2)) ** 2 * (1 + r_x(c.Mb, self.mB_theo) ** 2
                                                    - r_x(c.Mh, self.mB_theo) ** 2))
            return gamma

    def get_brBwt(self):
        gamma_wb = self.B_decay_to_wt()
        gamma_zt = self.B_decay_to_zb()
        gamma_ht = self.B_decay_to_hb()
        br_to_wb = gamma_wb / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_wb

    def get_brBzb(self):
        gamma_wb = self.B_decay_to_wt()
        gamma_zt = self.B_decay_to_zb()
        gamma_ht = self.B_decay_to_hb()
        br_to_zt = gamma_zt / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_zt

    def get_brBhb(self):
        gamma_wb = self.B_decay_to_wt()
        gamma_zt = self.B_decay_to_zb()
        gamma_ht = self.B_decay_to_hb()
        br_to_ht = gamma_ht / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_ht

    def get_coupling_to_zt_or_ht(self):
        c_l = np.sqrt(1 - self.sin_l ** 2)
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_l is not None:
                    return self.sin_l * c_l
                else:
                    raise Exception("Width, universal coupling and mixing are all None.")
            else:
                return self.kappa / np.sqrt(2)
        else:
            return self.kappa_coupling_from_width() / np.sqrt(2)

    def kappa_coupling_from_width(self, mB=None, wr=None):
        if wr is None:
            width_ratio = self.width_ratio
        else:
            width_ratio = wr

        if mB is None:
            MB = self.get_mB()
        else:
            MB = mB

        kappa = np.sqrt(2) * np.sqrt(width_ratio * MB / ((c.Cst1 * MB / (c.MW ** 2) * np.sqrt(
            lambda_func(MB, c.Mt, c.MW)) * (1 + r_x(c.MW, MB) ** 2 - 2 * r_x(c.Mt, MB) ** 2
                                            - 2 * r_x(c.MW, MB) ** 4 + r_x(c.Mt, MB) ** 4
                                            + r_x(c.Mt, MB) ** 2 * r_x(c.MW, MB) ** 2))
                                                         + (c.Cst2 * MB / (c.MZ ** 2)
                                                            * np.sqrt(lambda_func(MB, c.Mb, c.MZ))
                                                            * (1 + r_x(c.MZ, MB) ** 2
                                                               - 2 * r_x(c.Mb, MB) ** 2
                                                               - 2 * r_x(c.MZ, MB) ** 4
                                                               + r_x(c.Mb, MB) ** 4 + r_x(c.Mb, MB) ** 2
                                                               * r_x(c.MZ, MB) ** 2))
                                                         + (c.Cst3 * MB / (c.MW ** 2)
                                                            * np.sqrt(lambda_func(MB, c.Mb, c.Mh))
                                                            * (1 + r_x(c.Mb, MB) ** 2
                                                               - r_x(c.Mh, MB) ** 2))))
        return kappa


class DoubletB:

    def __init__(self):
        self.__model = 'Doublet'
        self.mB_theo = None
        self.sin_r = None
        self.sin_d_r = None
        self.kappa = None
        self.width_ratio = None
        self.which_d = 'BY'

    def set_mB(self, mB):
        self.mB_theo = mB

    def set_sin_r(self, s_r):
        self.sin_r = s_r

    def set_sin_d_r(self, s_d_r):
        self.sin_d_r = s_d_r

    def set_coupling_strength(self, k):
        self.kappa = k

    def set_width_mass_ratio(self, wr):
        self.width_ratio = wr

    def change_to_TB(self):
        self.which_d = 'TB'

    def get_mB(self):
        return self.mB_theo

    def get_which_doublet(self):
        return self.which_d

    def model(self):
        return self.__model

    def get_sin_down_right(self):
        return self.sin_d_r

    def get_width_mass_ratio(self):
        if self.width_ratio is None:
            if self.which_d == 'BY':
                g1 = self.B_decay_to_wt_BY()
                g2 = self.B_decay_to_zb_BY()
                g3 = self.B_decay_to_hb_BY()
                gamma_mB_ratio = (g1 + g2 + g3) / self.mB_theo
                return gamma_mB_ratio
            else:
                g2 = self.B_decay_to_zb_TB()
                g3 = self.B_decay_to_hb_TB()
                gamma_mB_ratio = (g2 + g3) / self.mB_theo
                return gamma_mB_ratio
        else:
            return self.width_ratio


    def get_xs_pp_Bbq_bHbq(self, i):
        if i in [5, 6, 7, 8]:
            mB = self.get_mB()
            w = self.get_width_mass_ratio()
            interp = interp2d_xs_theo('1802.01486', 'doublet', mB, w, vlq='B')
            return interp * 1000


    def get_xs_pp_Btq_bZtq(self, i):
        if i == 21:
            mT = self.get_mT()
            interp = interp2d_xs_theo('1701.07409', 'doublet', mT, 0.5)
            return interp * 1000
        elif i == 7:
            mT = self.get_mT()
            interp = interp2d_xs_theo('1708.01062', 'doublet', mT, 0.5)
            return interp * 1000
        elif i in [11, 12, 17, 18]:
            mT = self.get_mT()
            w = self.get_width_mass_ratio()
            interp = interp2d_xs_theo('1909.04721', 'doublet', mT, w)
            return (interp * 1000) / 2

    def get_xs_pp_Bj_bHj_ts_channels(self, i):
        if i in [15, 16, 17]:
            mT = self.get_mB()
            k = self.get_coupling_strength()
            linear_interp = interp2d_xs_theo('2308.02595', 'doublet', mT, k, vlq='B')
            return linear_interp * 1000

    def get_xs_pp_Bbq_tWbq(self, i):
        if i  == 20:
            mT = self.get_mB()
            xs_pp_BtW = xs_pp_Vb_qWb(mT, '2111.10216_CMS_Fig4_left_pp_B_Wt_singlet_doublet.dat', vlq='B')
            return xs_pp_BtW * 1000

    def get_xs_pp_Btq_tWtq(self, i):
        if i == 21:
            mT = self.get_mB()
            xs_pp_BtW = xs_pp_Vb_qWb(mT, '2111.10216_CMS_Fig4_right_pp_B_Wt_singlet_doublet.dat', vlq='B')
            return xs_pp_BtW * 1000

    def B_decay_to_wt_BY(self):
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_r is not None:
                    s_l = self.sin_left_calc(self.sin_r)
                    gamma = (c.Cst1 * self.mB_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mt, c.MW))
                             * s_l ** 2 * (1 + r_x(c.MW, self.mB_theo) ** 2 - 2 * r_x(c.Mt, self.mB_theo) ** 2 -
                                           2 * r_x(c.MW, self.mB_theo) ** 4 + r_x(c.Mt, self.mB_theo) ** 4
                                           + r_x(c.Mt, self.mB_theo) ** 2 * r_x(c.MW, self.mB_theo) ** 2))
                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")
            else:
                gamma = (c.Cst1 * self.mB_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mt, c.MW))
                         * self.kappa ** 2 * (1 + r_x(c.MW, self.mB_theo) ** 2 - 2 * r_x(c.Mt, self.mB_theo) ** 2
                                              - 2 * r_x(c.MW, self.mB_theo) ** 4 + r_x(c.Mt, self.mB_theo) ** 4
                                              + r_x(c.Mt, self.mB_theo) ** 2 * r_x(c.MW, self.mB_theo) ** 2))
                return gamma
        else:
            kappa = self.kappa_coupling_from_width(from_Bwidth=True, mB=self.get_mB())
            gamma = (c.Cst1 * self.mB_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mt, c.MW))
                     * kappa ** 2 * (1 + r_x(c.MW, self.mB_theo) ** 2 - 2 * r_x(c.Mt, self.mB_theo) ** 2
                                     - 2 * r_x(c.MW, self.mB_theo) ** 4 + r_x(c.Mt, self.mB_theo) ** 4
                                     + r_x(c.Mt, self.mB_theo) ** 2 * r_x(c.MW, self.mB_theo) ** 2))
            return gamma

    def B_decay_to_zb_BY(self):
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_r is not None:
                    s_l = self.sin_left_calc(self.sin_r)
                    c_l = np.sqrt(1 - s_l ** 2)
                    s_r = self.get_sin_right()
                    c_r = np.sqrt(1 - s_r ** 2)

                    gamma = (c.Cst2 * self.mB_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.MZ))
                             * ((s_r * c_r) ** 2 + (2 * s_l * c_l) ** 2) * ((1 + r_x(c.MZ, self.mB_theo) ** 2
                                                                             - 2 * r_x(c.Mb, self.mB_theo) ** 2
                                                                             - 2 * r_x(c.MZ, self.mB_theo) ** 4
                                                                             + r_x(c.Mb, self.mB_theo) ** 4
                                                                             + r_x(c.Mb, self.mB_theo) ** 2
                                                                             * r_x(c.MZ, self.mB_theo) ** 2)
                                                                            - 12 * r_x(c.MZ, self.mB_theo) ** 2
                                                                            * r_x(c.Mb, self.mB_theo) * 2
                                                                            * s_l * c_l * s_r * c_r))
                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")
            else:
                gamma = (c.Cst2 * self.mB_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.MZ))
                         * (self.kappa ** 2) * ((1 + r_x(c.MZ, self.mB_theo) ** 2 - 2 * r_x(c.Mb, self.mB_theo) ** 2
                                                - 2 * r_x(c.MZ, self.mB_theo) ** 4 + r_x(c.Mb, self.mB_theo) ** 4
                                                + r_x(c.Mb, self.mB_theo) ** 2 * r_x(c.MZ, self.mB_theo) ** 2)))
                return gamma
        else:
            kappa = self.kappa_coupling_from_width(from_Bwidth=True, mB=self.get_mB())
            gamma = (c.Cst2 * self.mB_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mt, c.MZ))
                     * (kappa ** 2) * ((1 + r_x(c.MZ, self.mB_theo) ** 2 - 2 * r_x(c.Mb, self.mB_theo) ** 2
                                        - 2 * r_x(c.MZ, self.mB_theo) ** 4 + r_x(c.Mb, self.mB_theo) ** 4
                                        + r_x(c.Mb, self.mB_theo) ** 2 * r_x(c.MZ, self.mB_theo) ** 2)))
            return gamma

    def B_decay_to_hb_BY(self):
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_u_r is not None:
                    s_r = self.get_sin_right()
                    c_r = np.sqrt(1 - s_r ** 2)

                    gamma = (c.Cst3 * self.mB_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.Mh))
                             * (s_r * c_r) ** 2 * (1 + 6 * r_x(c.Mb, self.mB_theo) ** 2
                             - r_x(c.Mh, self.mB_theo) ** 2 + r_x(c.Mb, self.mB_theo) ** 4
                             - r_x(c.Mb, self.mB_theo) ** 2 * r_x(c.Mh, self.mB_theo) ** 2))

                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")
            else:
                gamma = (c.Cst3 * self.mB_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.Mh))
                         * self.kappa ** 2 * (1 + r_x(c.Mb, self.mB_theo) ** 2 - r_x(c.Mh, self.mB_theo) ** 2))
                return gamma
        else:
            kappa = self.kappa_coupling_from_width(from_Bwidth=True, mB=self.get_mB())
            gamma = (c.Cst3 * self.mB_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.Mh))
                     * kappa ** 2 * (1 + r_x(c.Mb, self.mB_theo) ** 2 - r_x(c.Mh, self.mB_theo) ** 2))
            return gamma

    def B_decay_to_zb_TB(self):
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_d_r is not None:
                    s_d_r = self.get_sin_down_right()
                    c_d_r = np.sqrt(1 - s_d_r ** 2)

                    gamma = (c.Cst2 * self.mB_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.MZ))
                             * (s_d_r * c_d_r) ** 2 * ((1 + r_x(c.MZ, self.mB_theo) ** 2
                                                       - 2 * r_x(c.Mb, self.mB_theo) ** 2
                                                        - 2 * r_x(c.MZ, self.mB_theo) ** 4
                                                        + r_x(c.Mb, self.mB_theo) ** 4 + r_x(c.Mb, self.mB_theo) ** 2
                                                        * r_x(c.MZ, self.mB_theo) ** 2)))

                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")

            else:
                gamma = (c.Cst2 * self.mB_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.MZ))
                         * self.kappa ** 2 * ((1 + r_x(c.MZ, self.mB_theo) ** 2
                                              - 2 * r_x(c.Mb, self.mB_theo) ** 2 - 2 * r_x(c.MZ, self.mB_theo) ** 4
                                              + r_x(c.Mt, self.mB_theo) ** 4 + r_x(c.Mt, self.mB_theo) ** 2
                                              * r_x(c.MZ, self.mB_theo) ** 2)))

                return gamma
        else:
            kappa = self.kappa_coupling_from_width()
            gamma = (c.Cst2 * self.mB_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.MZ))
                     * kappa ** 2 * ((1 + r_x(c.MZ, self.mB_theo) ** 2 - 2 * r_x(c.Mb, self.mB_theo) ** 2
                                      - 2 * r_x(c.MZ, self.mB_theo) ** 4 + r_x(c.Mb, self.mB_theo) ** 4
                                      + r_x(c.Mb, self.mB_theo) ** 2 * r_x(c.MZ, self.mB_theo) ** 2)))

            return gamma

    def B_decay_to_hb_TB(self):
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_d_r is not None:
                    s_d_r = self.get_sin_down_right()
                    c_d_r = np.sqrt(1 - s_d_r ** 2)

                    gamma = (c.Cst3 * self.mB_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.Mh))
                             * (s_d_r * c_d_r ** 2) * (1 + 6 * r_x(c.Mb, self.mB_theo) ** 2
                             - r_x(c.Mh, self.mB_theo) ** 2 + r_x(c.Mb, self.mB_theo) ** 4
                             - r_x(c.Mb, self.mB_theo) ** 2 * r_x(c.Mh, self.mB_theo) ** 2))

                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")
            else:
                gamma = (c.Cst3 * self.mB_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.Mh))
                         * self.kappa ** 2 * (1 + r_x(c.Mb, self.mB_theo) ** 2 - r_x(c.Mh, self.mB_theo) ** 2))
                return gamma
        else:
            kappa = self.kappa_coupling_from_width()
            gamma = (c.Cst3 * self.mB_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.Mh))
                     * kappa ** 2 * (1 + r_x(c.Mb, self.mB_theo) ** 2 - r_x(c.Mh, self.mB_theo) ** 2))
            return gamma

    def kappa_coupling_from_width(self, mB=None, wr=None):
        if wr is None:
            width_ratio = self.width_ratio
        else:
            width_ratio = wr
        if mB is None:
            MB = self.get_mB()
        else:
            MB = mB

        kappa = np.sqrt(width_ratio * MB / ((c.Cst2 * MB / (c.MZ ** 2)
                                             * np.sqrt(lambda_func(MB, c.Mb, c.MZ))
                                             * (1 + r_x(c.MZ, MB) ** 2 - 2 * r_x(c.Mb, MB) ** 2
                                                - 2 * r_x(c.MZ, MB) ** 4 + r_x(c.Mb, MB) ** 4
                                                + r_x(c.Mb, MB) ** 2 * r_x(c.MZ, MB) ** 2))
                                            + (c.Cst3 * MB / (c.MW ** 2)
                                               * np.sqrt(lambda_func(MB, c.Mb, c.Mh))
                                               * (1 + r_x(c.Mb, MB) ** 2 - r_x(c.Mh, MB) ** 2))))
        return kappa

    def get_xs_pp_QQ(self):
        mB = self.get_mB()
        xs_pp_BB = xs_pp_QQ_theo(mB)
        return xs_pp_BB

    def get_brBwt_BY(self):
        gamma_wb = self.B_decay_to_wb_BY()
        gamma_zt = self.B_decay_to_zt_BY()
        gamma_ht = self.B_decay_to_ht_BY()
        br_to_wb = gamma_wb / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_wb

    def get_brBzb_BY(self):
        gamma_wb = self.B_decay_to_wt_BY()
        gamma_zt = self.B_decay_to_zb_BY()
        gamma_ht = self.B_decay_to_hb_BY()
        br_to_zt = gamma_zt / (gamma_ht + gamma_wb + gamma_zt) # + gamma_wb
        return br_to_zt

    def get_brBhb_BY(self):
        gamma_wb = self.B_decay_to_wt_BY()
        gamma_zt = self.B_decay_to_zb_BY()
        gamma_ht = self.B_decay_to_hb_BY()
        br_to_ht = gamma_ht / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_ht

    def get_brBzb_TB(self):
        gamma_zt = self.B_decay_to_zb_TB()
        gamma_ht = self.B_decay_to_hb_TB()
        br_to_zt = gamma_zt / (gamma_ht + gamma_zt)
        return br_to_zt

    def get_brBhb_TB(self):
        gamma_zt = self.B_decay_to_zb_TB()
        gamma_ht = self.B_decay_to_hb_TB()
        br_to_ht = gamma_ht / (gamma_ht + gamma_zt)
        return br_to_ht

    def get_sin_right(self):
        if self.sin_r is not None:
            return abs(self.sin_r)
        else:
            if self.kappa is not None:
                return self.kappa
            else:
                if self.width_ratio is not None:
                    kappa = self.kappa_coupling_from_width()
                    return kappa

    def sin_left_calc(self, s_r):
        c_r = np.sqrt(1 - s_r ** 2)
        tg_r = s_r / c_r
        s_l = np.sqrt((r_x(c.Mt, self.mB_theo) * tg_r) ** 2 / (1 + ((r_x(c.Mt, self.mB_theo) * tg_r) ** 2)))
        return s_l

    def get_coupling_strength(self):
        if self.width_ratio is None:
            if self.kappa is None:
                if self.which_d == 'BY':
                    c_r = np.sqrt(1 - self.sin_r ** 2)
                    return self.sin_r * c_r
                else:
                    c_d_r = np.sqrt(1 - self.sin_d_r ** 2)
                    return self.sin_d_r * c_d_r
            else:
                return self.kappa
        else:
            kappa = self.kappa_coupling_from_width()
            return kappa


class PureDecay:

    def __init__(self):
        self.mB_theo = None
        self.__model = 'Pure'

    def set_mB(self, mB):
        self.mB_theo = mB

    def get_mB(self):
        return self.mB_theo

    def get_xs_pp_BB(self):
        mB = self.get_mB()
        xs_pp_BB = xs_pp_QQ_theo(mB)
        return xs_pp_BB

    def model(self):
        return self.__model
