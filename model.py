import math
import numpy as np
import constants as c
from initialize import Tables
from utils import *


class Singlet:

    def __init__(self):
        self.__model = 'Singlet'
        self.mT_theo = None
        self.mB_theo = None
        self.sin_l = None
        self.kappa = None
        self.width_ratio = None

    def set_mT(self, mT):
        self.mT_theo = mT

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

    def get_mT(self):
        return self.mT_theo

    def get_mB(self):
        return self.mB_theo

    def get_sin_left(self, from_B_width=False):
        if self.sin_l is not None:
            return self.sin_l
        else:
            if self.kappa is not None:
                return self.kappa / np.sqrt(2)
            else:
                if self.width_ratio is not None:
                    if from_B_width:
                        kappa = self.kappa_coupling_from_width(from_B_width=True, mB=self.get_mB())
                        return kappa / np.sqrt(2)
                    else:
                        kappa = self.kappa_coupling_from_width()
                        return kappa / np.sqrt(2)

    def get_width_mass_ratio(self, return_B=False):
        if self.width_ratio is None:
            if return_B:
                g1 = self.B_decay_to_wt()
                g2 = self.B_decay_to_hb()
                g3 = self.B_decay_to_zb()
                gamma_mv_ratio = (g1 + g2 + g3) / self.mT_theo
                return gamma_mv_ratio
            else:
                g1 = self.T_decay_to_wb()
                g2 = self.T_decay_to_ht()
                g3 = self.T_decay_to_zt()
                gamma_mv_ratio = (g1 + g2 + g3) / self.mT_theo
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
        mT = self.get_mT()
        xsec_pp_TT = xsec_pp_TT_from_pred(mT)
        return xsec_pp_TT

    def get_xs_pp_Tbq_Wbbq(self, i):
        if i == 57:
            mT = self.get_mT()
            xsec_pp_TbW = xsec_pp_Tbq_bWbq(mT, 'ATLAS-CONF-2016-072_fig8_pp_T_Wb_singlet_theo.dat')
            return xsec_pp_TbW * 1000
        elif i == 30:
            mT = self.get_mT()
            linear_interp = interp2d_xs_theo('1602.05606', 'singlet', mT, 1)
            return linear_interp * 1000
        elif i == 59:
            mT = self.get_mT()
            linear_interp = interp2d_xs_theo('1701.08328', 'singlet', mT, 0.5)
            return linear_interp * 1000

    def get_xs_pp_Tj_Ztj_ts_channels(self, i):
        if i in [32, 33, 34]:
            mT = self.get_mT()
            k = self.get_coupling_strength()
            linear_interp = interp2d_xs_theo('2305.03401', 'singlet', mT, k)
            return linear_interp
        elif i in [43, 44, 45]:
            mT = self.get_mT()
            k = self.get_coupling_strength()
            linear_interp = interp2d_xs_theo('2307.07584', 'singlet', mT, k)
            return linear_interp * 1000
        elif i == 35:
            mT = self.get_mT()
            linear_interp = interp2d_xs_theo('2402.16561', 'singlet', mT, 0.5)
            return linear_interp

    def get_xs_pp_Tbq_tHbq(self, i):
        if i in [37, 38, 39, 40, 41, 42]:
            mT = self.get_mT()
            k = self.get_coupling_strength()
            interp = interp2d_xs_theo('2201.07045', 'Singlet', mT, k)
            return interp
        elif i == 17:
            mT = self.get_mT()
            interp = interp2d_xs_theo('1612.00999', 'singlet', mT, 0.5)
            return interp * 1000
        elif i == 46:
            mT = self.get_mT()
            interp = interp2d_xs_theo('1612.05336', 'singlet', mT, 0.5)
            return interp * 1000
        elif i == 16:
            mT = self.get_mT()
            k = self.get_coupling_strength() / np.sqrt(2)
            interp = interp2d_xs_theo('2302.12802', 'singlet', mT, k)
            return interp
        elif i in [18, 19, 24, 25]:
            mT = self.get_mT()
            w = self.get_width_mass_ratio()
            interp = interp2d_xs_theo('2201.02227', 'Singlet', mT, w)
            return interp * 1000

    def get_xs_pp_Tbq_tZbq(self, i):
        if i == 58:
            mT = self.get_mT()
            interp = interp2d_xs_theo('1806.10555', 'Singlet', mT, 0.5)
            return interp * 1000
        elif i == 31:
            mT = self.get_mT()
            interp = interp2d_xs_theo('1701.07409', 'singlet', mT, 0.5)
            return interp * 1000
        elif i == 14:
            mT = self.get_mT()
            interp = interp2d_xs_theo('1708.01062', 'singlet', mT, 0.5)
            return interp * 1000
        elif i == 36:
            mT = self.get_mT()
            interp = xsec_pp_Tbq_Ztbq(mT, '1812.09743_ATLAS_Fig4c_pp_T_tZ_Singlet_theo.dat')#interp2d_xs_theo('1812.09743', 'Singlet', mT, 0.5)
            return interp * 1000
        elif i in [10, 11, 12, 13]:
            mT = self.get_mT()
            w = self.get_width_mass_ratio()
            interp = interp2d_xs_theo('2201.02227', 'Singlet', mT, w)
            return interp * 1000
        elif i in [50, 51]:
            if i == 50:
                mT = self.get_mT()
                interp = interp2d_xs_theo('2405.05071_CMS_Fig4ur', 'singlet', mT, 0.01)
                return interp * 1000
            else:
                mT = self.get_mT()
                interp = interp2d_xs_theo('2405.05071_CMS_Fig4ul', 'singlet', mT, 0.01)
                return interp * 1000
        elif i in [20, 21, 26, 27]:
            mT = self.get_mT()
            w = self.get_width_mass_ratio()
            interp = interp2d_xs_theo('2201.02227', 'Singlet', mT, w)
            return interp * 1000

    def get_xs_pp_Tbq_tZ_plus_TH(self, i):
        if i in [52, 53]:
            if i == 52:
                mT = self.get_mT()
                interp = interp2d_xs_theo('2405.05071_CMS_Fig4ll', 'singlet', mT, 0.01)
                return interp * 1000
            else:
                mT = self.get_mT()
                interp = interp2d_xs_theo('2405.05071_CMS_Fig4lr', 'singlet', mT, 0.01)
                return interp * 1000
        elif i in [22, 23, 28, 29]:
            mT = self.get_mT()
            w = self.get_width_mass_ratio()
            interp = interp2d_xs_theo('2201.02227', 'Singlet', mT, w)
            return interp * 1000 * 2

    def get_xs_pp_Tbq(self, i):
        if i == 15:
            mT = self.get_mT()
            w = self.get_width_mass_ratio()
            interp = interp2d_xs_theo('2201.02227', 'Singlet', mT, w)
            return (interp * 1000) / 0.25

    def T_decay_to_wb(self):
        constant = c.G ** 2 / (64 * c.PI)
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_l is not None:
                    s_l = self.sin_l

                    gamma = (constant * self.mT_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mb, c.MW))
                             * s_l ** 2 * (1 + r_x(c.MW, self.mT_theo) ** 2 - 2 * r_x(c.Mb, self.mT_theo) ** 2
                             - 2 * r_x(c.MW, self.mT_theo) ** 4 + r_x(c.Mb, self.mT_theo) ** 4
                             + r_x(c.Mb, self.mT_theo) ** 2 * r_x(c.MW, self.mT_theo) ** 2))
                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")
            else:
                gamma = (constant * self.mT_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mb, c.MW))
                         * (self.kappa / np.sqrt(2)) ** 2 * (1 + r_x(c.MW, self.mT_theo) ** 2
                                                             - 2 * r_x(c.Mb, self.mT_theo) ** 2
                                                             - 2 * r_x(c.MW, self.mT_theo) ** 4
                                                             + r_x(c.Mb, self.mT_theo) ** 4
                                                             + r_x(c.Mb, self.mT_theo) ** 2
                                                             * r_x(c.MW, self.mT_theo) ** 2))
                return gamma
        else:
            kappa = self.kappa_coupling_from_width()
            gamma = (constant * self.mT_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mb, c.MW))
                     * (kappa / np.sqrt(2)) ** 2 * (1 + r_x(c.MW, self.mT_theo) ** 2
                                                    - 2 * r_x(c.Mb, self.mT_theo) ** 2
                                                    - 2 * r_x(c.MW, self.mT_theo) ** 4
                                                    + r_x(c.Mb, self.mT_theo) ** 4
                                                    + r_x(c.Mb, self.mT_theo) ** 2
                                                    * r_x(c.MW, self.mT_theo) ** 2))
            return gamma

    def T_decay_to_zt(self):
        constant = c.G ** 2 / (128 * c.PI * c.C_W ** 2)
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_l is not None:
                    s_l = self.sin_l
                    c_l = np.sqrt(1 - s_l ** 2)

                    gamma = (constant * self.mT_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.MZ))
                             * (s_l * c_l) ** 2 * (1 + r_x(c.MZ, self.mT_theo) ** 2 - 2 * r_x(c.Mt, self.mT_theo) ** 2
                             - 2 * r_x(c.MZ, self.mT_theo) ** 4 + r_x(c.Mt, self.mT_theo) ** 4
                             + r_x(c.Mt, self.mT_theo) ** 2 * r_x(c.MZ, self.mT_theo) ** 2))

                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")
            else:
                gamma = (constant * self.mT_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.MZ))
                         * (self.kappa / np.sqrt(2)) ** 2 * (1 + r_x(c.MZ, self.mT_theo) ** 2
                                                             - 2 * r_x(c.Mt, self.mT_theo) ** 2
                                                             - 2 * r_x(c.MZ, self.mT_theo) ** 4
                                                             + r_x(c.Mt, self.mT_theo) ** 4
                                                             + r_x(c.Mt, self.mT_theo) ** 2
                                                             * r_x(c.MZ, self.mT_theo) ** 2))
                return gamma
        else:
            kappa = self.kappa_coupling_from_width()
            gamma = (constant * self.mT_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.MZ))
                     * (kappa / np.sqrt(2)) ** 2 * (1 + r_x(c.MZ, self.mT_theo) ** 2
                                                    - 2 * r_x(c.Mt, self.mT_theo) ** 2
                                                    - 2 * r_x(c.MZ, self.mT_theo) ** 4
                                                    + r_x(c.Mt, self.mT_theo) ** 4
                                                    + r_x(c.Mt, self.mT_theo) ** 2
                                                    * r_x(c.MZ, self.mT_theo) ** 2))
            return gamma

    def T_decay_to_ht(self):
        constant = c.G ** 2 / (128 * c.PI)
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_l is not None:
                    s_l = self.sin_l
                    c_l = np.sqrt(1 - s_l ** 2)
                    gamma = (constant * self.mT_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.Mh))
                             * (s_l * c_l) ** 2 * (1 + 6 * r_x(c.Mt, self.mT_theo) ** 2
                             - r_x(c.Mh, self.mT_theo) ** 2 + r_x(c.Mt, self.mT_theo) ** 4
                             - r_x(c.Mt, self.mT_theo) ** 2 * r_x(c.Mh, self.mT_theo) ** 2))

                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")
            else:
                gamma = (constant * self.mT_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.Mh))
                         * (self.kappa / np.sqrt(2)) ** 2 * (1 + r_x(c.Mt, self.mT_theo) ** 2
                                                             - r_x(c.Mh, self.mT_theo) ** 2))
                return gamma
        else:
            kappa = self.kappa_coupling_from_width()
            gamma = (constant * self.mT_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.Mh))
                     * (kappa / np.sqrt(2)) ** 2 * (1 + r_x(c.Mt, self.mT_theo) ** 2
                                                    - r_x(c.Mh, self.mT_theo) ** 2))
            return gamma

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
                gamma = (constant * self.mT_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.Mh))
                         * (self.kappa / np.sqrt(2)) ** 2 * (1 + r_x(c.Mb, self.mB_theo) ** 2
                                                             - r_x(c.Mh, self.mT_theo) ** 2))
                return gamma
        else:
            kappa = self.kappa_coupling_from_width()
            gamma = (constant * self.mB_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.Mh))
                     * (kappa / np.sqrt(2)) ** 2 * (1 + r_x(c.Mb, self.mB_theo) ** 2
                                                    - r_x(c.Mh, self.mB_theo) ** 2))
            return gamma

    def get_brTbw(self):
        gamma_wb = self.T_decay_to_wb()
        gamma_zt = self.T_decay_to_zt()
        gamma_ht = self.T_decay_to_ht()
        br_to_wb = gamma_wb / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_wb

    def get_brTzt(self):
        gamma_wb = self.T_decay_to_wb()
        gamma_zt = self.T_decay_to_zt()
        gamma_ht = self.T_decay_to_ht()
        br_to_zt = gamma_zt / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_zt

    def get_brTht(self):
        gamma_wb = self.T_decay_to_wb()
        gamma_zt = self.T_decay_to_zt()
        gamma_ht = self.T_decay_to_ht()
        br_to_ht = gamma_ht / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_ht

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

    def kappa_coupling_from_width(self, mT=None, wr=None, from_B_width=False, mB=None):
        if from_B_width:
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
        else:
            if wr is None:
                width_ratio = self.width_ratio
            else:
                width_ratio = wr
            if mT is None:
                MT = self.get_mT()
            else:
                MT = mT

            kappa = np.sqrt(2) * np.sqrt(width_ratio * MT / ((c.Cst1 * MT / (c.MW ** 2) * np.sqrt(
                lambda_func(self.mT_theo, c.Mb, c.MW)) * (1 + r_x(c.MW, MT) ** 2
                                                          - 2 * r_x(c.Mb, MT) ** 2
                                                          - 2 * r_x(c.MW, MT) ** 4 + r_x(c.Mb, MT) ** 4
                                                          + r_x(c.Mb, MT) ** 2 * r_x(c.MW, MT) ** 2))
                                                      + (c.Cst2 * MT / (c.MZ ** 2)
                                                         * np.sqrt(lambda_func(MT, c.Mt, c.MZ))
                                                         * (1 + r_x(c.MZ, MT) ** 2
                                                            - 2 * r_x(c.Mt, MT) ** 2
                                                            - 2 * r_x(c.MZ, MT) ** 4
                                                            + r_x(c.Mt, MT) ** 4 + r_x(c.Mt, MT) ** 2
                                                            * r_x(c.MZ, MT) ** 2))
                                                      + (c.Cst3 * MT / (c.MW ** 2)
                                                         * np.sqrt(lambda_func(MT, c.Mt, c.Mh))
                                                         * (1 + r_x(c.Mt, MT) ** 2
                                                            - r_x(c.Mh, MT) ** 2))))
            return kappa


class Doublet:

    def __init__(self):
        self.__model = 'Doublet'
        self.mT_theo = None
        self.mB_theo = None
        self.sin_r = None
        self.sin_u_r = None
        self.sin_d_r = None
        self.kappa = None
        self.width_ratio = None
        self.which_d = 'XT'

    def set_mT(self, mT):
        self.mT_theo = mT

    def set_mB(self, mB):
        self.mT_theo = mB

    def set_sin_r(self, s_r):
        self.sin_r = s_r

    def set_sin_u_r(self, s_u_r):
        self.sin_u_r = s_u_r

    def set_sin_d_r(self, s_d_r):
        self.sin_d_r = s_d_r

    def set_coupling_strength(self, k):
        self.kappa = k

    def set_width_mass_ratio(self, wr):
        self.width_ratio = wr

    def change_to_TB(self):
        self.which_d = 'TB'

    def get_mT(self):
        return self.mT_theo

    def get_mB(self):
        return self.mB_theo

    def get_which_doublet(self):
        return self.which_d

    def model(self):
        return self.__model

    def get_sin_up_right(self):
        if self.sin_u_r is not None:
            return self.sin_u_r
        else:
            return

    def get_sin_down_right(self):
        return self.sin_d_r

    def get_width_mass_ratio(self):
        if self.width_ratio is None:
            if self.which_d == 'XT':
                g2 = self.T_decay_to_zt_TX()
                g3 = self.T_decay_to_ht_TX()
                gamma_mv_ratio = (g2 + g3) / self.mT_theo
                return gamma_mv_ratio
            else:
                g2 = self.T_decay_to_zt_TB()
                g3 = self.T_decay_to_ht_TB()
                gamma_mv_ratio = (g2 + g3) / self.mT_theo
                return gamma_mv_ratio
        else:
            return self.width_ratio

    def get_xs_pp_Tj_Ztj_ts_channels(self, i):
        if i in [23, 24, 25]:
            mT = self.get_mT()
            k = self.get_coupling_strength()
            linear_interp = interp2d_xs_theo('2305.03401', 'doublet', mT, k)
            return linear_interp
        elif i in [26, 27, 28]:
            mT = self.get_mT()
            k = self.get_coupling_strength()
            linear_interp = interp2d_xs_theo('2307.07584', 'doublet', mT, k)
            return linear_interp * 1000

    def get_xs_pp_Ttq_tZtq(self, i):
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

    def get_xs_pp_Ttq_tHtq(self, i):
        if i == 5:
            mT = self.get_mT()
            interp = interp2d_xs_theo('1701.07409', 'doublet', mT, 0.5)
            return interp * 1000
        elif i == 29:
            mT = self.get_mT()
            interp = interp2d_xs_theo('1612.05336', 'doublet', mT, 0.5)
            return interp * 1000
        elif i in [9, 10, 15, 16]:
            mT = self.get_mT()
            w = self.get_width_mass_ratio()
            interp = interp2d_xs_theo('1909.04721', 'doublet', mT, w)
            return (interp * 1000) / 2

    def get_xs_pp_Ttq_tZ_plus_TH(self, i):
        if i in [13, 14, 19, 20]:
            mT = self.get_mT()
            w = self.get_width_mass_ratio()
            interp = interp2d_xs_theo('1909.04721', 'doublet', mT, w)
            return interp * 1000

    def T_decay_to_wb_TX(self):
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_r is not None:
                    s_l = self.sin_left_calc(self.sin_r)
                    gamma = (c.Cst1 * self.mT_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mb, c.MW))
                             * s_l ** 2 * (1 + r_x(c.MW, self.mT_theo) ** 2 - 2 * r_x(c.Mb, self.mT_theo) ** 2 -
                                           2 * r_x(c.MW, self.mT_theo) ** 4 + r_x(c.Mb, self.mT_theo) ** 4
                                           + r_x(c.Mb, self.mT_theo) ** 2 * r_x(c.MW, self.mT_theo) ** 2))
                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")
            else:
                gamma = (c.Cst1 * self.mT_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mb, c.MW))
                         * self.kappa ** 2 * (1 + r_x(c.MW, self.mT_theo) ** 2 - 2 * r_x(c.Mb, self.mT_theo) ** 2 -
                                              2 * r_x(c.MW, self.mT_theo) ** 4 + r_x(c.Mb, self.mT_theo) ** 4
                                              + r_x(c.Mb, self.mT_theo) ** 2 * r_x(c.MW, self.mT_theo) ** 2))
                return gamma
        else:
            kappa = self.kappa_coupling_from_width()
            gamma = (c.Cst1 * self.mT_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mb, c.MW))
                     * kappa ** 2 * (1 + r_x(c.MW, self.mT_theo) ** 2 - 2 * r_x(c.Mb, self.mT_theo) ** 2
                                     - 2 * r_x(c.MW, self.mT_theo) ** 4 + r_x(c.Mb, self.mT_theo) ** 4
                                     + r_x(c.Mb, self.mT_theo) ** 2 * r_x(c.MW, self.mT_theo) ** 2))
            return gamma

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

    def T_decay_to_zt_TX(self):
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_r is not None:
                    s_l = self.sin_left_calc(self.sin_r)
                    c_l = np.sqrt(1 - s_l ** 2)
                    s_r = self.get_sin_right()
                    c_r = np.sqrt(1 - s_r ** 2)

                    gamma = (c.Cst2 * self.mT_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.MZ))
                             * ((s_r * c_r) ** 2 + (2 * s_l * c_l) ** 2) * ((1 + r_x(c.MZ, self.mT_theo) ** 2
                                                                             - 2 * r_x(c.Mt, self.mT_theo) ** 2
                                                                             - 2 * r_x(c.MZ, self.mT_theo) ** 4
                                                                             + r_x(c.Mt, self.mT_theo) ** 4
                                                                             + r_x(c.Mt, self.mT_theo) ** 2
                                                                             * r_x(c.MZ, self.mT_theo) ** 2)
                                                                            - 12 * r_x(c.MZ, self.mT_theo) ** 2
                                                                            * r_x(c.Mt, self.mT_theo) * 2
                                                                            * s_l * c_l * s_r * c_r))
                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")
            else:
                gamma = (c.Cst2 * self.mT_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.MZ))
                         * (self.kappa ** 2) * ((1 + r_x(c.MZ, self.mT_theo) ** 2 - 2 * r_x(c.Mt, self.mT_theo) ** 2
                                                - 2 * r_x(c.MZ, self.mT_theo) ** 4 + r_x(c.Mt, self.mT_theo) ** 4
                                                + r_x(c.Mt, self.mT_theo) ** 2 * r_x(c.MZ, self.mT_theo) ** 2)))
                return gamma
        else:
            kappa = self.kappa_coupling_from_width()
            gamma = (c.Cst2 * self.mT_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.MZ))
                     * (kappa ** 2) * ((1 + r_x(c.MZ, self.mT_theo) ** 2 - 2 * r_x(c.Mt, self.mT_theo) ** 2
                                             - 2 * r_x(c.MZ, self.mT_theo) ** 4 + r_x(c.Mt, self.mT_theo) ** 4
                                             + r_x(c.Mt, self.mT_theo) ** 2 * r_x(c.MZ, self.mT_theo) ** 2)))
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
            gamma = (c.Cst2 * self.mB_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.MZ))
                     * (kappa ** 2) * ((1 + r_x(c.MZ, self.mB_theo) ** 2 - 2 * r_x(c.Mb, self.mB_theo) ** 2
                                        - 2 * r_x(c.MZ, self.mB_theo) ** 4 + r_x(c.Mb, self.mB_theo) ** 4
                                        + r_x(c.Mb, self.mB_theo) ** 2 * r_x(c.MZ, self.mB_theo) ** 2)))
            return gamma

    def T_decay_to_ht_TX(self):
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_u_r is not None:
                    s_r = self.get_sin_right()
                    c_r = np.sqrt(1 - s_r ** 2)

                    gamma = (c.Cst3 * self.mT_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.Mh))
                             * (s_r * c_r) ** 2 * (1 + 6 * r_x(c.Mt, self.mT_theo) ** 2
                             - r_x(c.Mh, self.mT_theo) ** 2 + r_x(c.Mt, self.mT_theo) ** 4
                             - r_x(c.Mt, self.mT_theo) ** 2 * r_x(c.Mh, self.mT_theo) ** 2))

                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")
            else:
                gamma = (c.Cst3 * self.mT_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.Mh))
                         * self.kappa ** 2 * (1 + r_x(c.Mt, self.mT_theo) ** 2 - r_x(c.Mh, self.mT_theo) ** 2))
                return gamma
        else:
            kappa = self.kappa_coupling_from_width()
            gamma = (c.Cst3 * self.mT_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.Mh))
                     * kappa ** 2 * (1 + r_x(c.Mt, self.mT_theo) ** 2 - r_x(c.Mh, self.mT_theo) ** 2))
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

    def T_decay_to_zt_TB(self):
        constant = c.G ** 2 / (128 * c.PI * c.C_W ** 2)
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_u_r is not None:
                    s_u_r = self.get_sin_up_right()
                    c_u_r = np.sqrt(1 - s_u_r ** 2)

                    gamma = (constant * self.mT_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.MZ))
                             * (s_u_r * c_u_r) ** 2 * ((1 + r_x(c.MZ, self.mT_theo) ** 2
                                                       - 2 * r_x(c.Mt, self.mT_theo) ** 2
                                                        - 2 * r_x(c.MZ, self.mT_theo) ** 4
                                                        + r_x(c.Mt, self.mT_theo) ** 4 + r_x(c.Mt, self.mT_theo) ** 2
                                                        * r_x(c.MZ, self.mT_theo) ** 2)))

                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")

            else:
                gamma = (constant * self.mT_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.MZ))
                         * self.kappa ** 2 * ((1 + r_x(c.MZ, self.mT_theo) ** 2
                                              - 2 * r_x(c.Mt, self.mT_theo) ** 2 - 2 * r_x(c.MZ, self.mT_theo) ** 4
                                              + r_x(c.Mt, self.mT_theo) ** 4 + r_x(c.Mt, self.mT_theo) ** 2
                                              * r_x(c.MZ, self.mT_theo) ** 2)))

                return gamma
        else:
            kappa = self.kappa_coupling_from_width()
            gamma = (constant * self.mT_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.MZ))
                     * kappa ** 2 * ((1 + r_x(c.MZ, self.mT_theo) ** 2 - 2 * r_x(c.Mt, self.mT_theo) ** 2
                                      - 2 * r_x(c.MZ, self.mT_theo) ** 4 + r_x(c.Mt, self.mT_theo) ** 4
                                      + r_x(c.Mt, self.mT_theo) ** 2 * r_x(c.MZ, self.mT_theo) ** 2)))

            return gamma
    def B_decay_to_zb_TB(self):
        constant = c.G ** 2 / (128 * c.PI * c.C_W ** 2)
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_d_r is not None:
                    s_d_r = self.get_sin_down_right()
                    c_d_r = np.sqrt(1 - s_d_r ** 2)

                    gamma = (constant * self.mB_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.MZ))
                             * (s_d_r * c_d_r) ** 2 * ((1 + r_x(c.MZ, self.mB_theo) ** 2
                                                       - 2 * r_x(c.Mb, self.mB_theo) ** 2
                                                        - 2 * r_x(c.MZ, self.mB_theo) ** 4
                                                        + r_x(c.Mb, self.mB_theo) ** 4 + r_x(c.Mb, self.mB_theo) ** 2
                                                        * r_x(c.MZ, self.mB_theo) ** 2)))

                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")

            else:
                gamma = (constant * self.mT_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.MZ))
                         * self.kappa ** 2 * ((1 + r_x(c.MZ, self.mB_theo) ** 2
                                              - 2 * r_x(c.Mb, self.mB_theo) ** 2 - 2 * r_x(c.MZ, self.mB_theo) ** 4
                                              + r_x(c.Mt, self.mB_theo) ** 4 + r_x(c.Mt, self.mB_theo) ** 2
                                              * r_x(c.MZ, self.mB_theo) ** 2)))

                return gamma
        else:
            kappa = self.kappa_coupling_from_width(from_Bwidth=True, mB=self.get_mB())
            gamma = (constant * self.mB_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mB_theo, c.Mb, c.MZ))
                     * kappa ** 2 * ((1 + r_x(c.MZ, self.mB_theo) ** 2 - 2 * r_x(c.Mb, self.mB_theo) ** 2
                                      - 2 * r_x(c.MZ, self.mB_theo) ** 4 + r_x(c.Mb, self.mB_theo) ** 4
                                      + r_x(c.Mb, self.mB_theo) ** 2 * r_x(c.MZ, self.mB_theo) ** 2)))

            return gamma

    def T_decay_to_ht_TB(self):
        constant = c.G ** 2 / (128 * c.PI)
        if self.width_ratio is None:
            if self.kappa is None:
                if self.sin_u_r is not None:
                    s_u_r = self.get_sin_up_right()
                    c_u_r = np.sqrt(1 - s_u_r ** 2)

                    gamma = (constant * self.mT_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.Mh))
                             * (s_u_r * c_u_r ** 2) * (1 + 6 * r_x(c.Mt, self.mT_theo) ** 2
                             - r_x(c.Mh, self.mT_theo) ** 2 + r_x(c.Mt, self.mT_theo) ** 4
                             - r_x(c.Mt, self.mT_theo) ** 2 * r_x(c.Mh, self.mT_theo) ** 2))

                    return gamma
                else:
                    raise Exception("Calculation error: Width, universal coupling and mixing are all None.")
            else:
                gamma = (constant * self.mT_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.Mh))
                         * self.kappa ** 2 * (1 + r_x(c.Mt, self.mT_theo) ** 2 - r_x(c.Mh, self.mT_theo) ** 2))
                return gamma
        else:
            kappa = self.kappa_coupling_from_width()
            gamma = (constant * self.mT_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mT_theo, c.Mt, c.Mh))
                     * kappa ** 2 * (1 + r_x(c.Mt, self.mT_theo) ** 2 - r_x(c.Mh, self.mT_theo) ** 2))
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

    def kappa_coupling_from_width(self, mT=None, wr=None, from_Bwidth=False, mB=None):
        if from_Bwidth:
            if wr is None:
                width_ratio = self.width_ratio
            else:
                width_ratio = wr
            if mT is None:
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
        else:
            if wr is None:
                width_ratio = self.width_ratio
            else:
                width_ratio = wr
            if mT is None:
                MT = self.get_mT()
            else:
                MT = mT

            kappa = np.sqrt(width_ratio * MT / ((c.Cst2 * MT / (c.MZ ** 2)
                                                 * np.sqrt(lambda_func(MT, c.Mt, c.MZ))
                                                 * (1 + r_x(c.MZ, MT) ** 2
                                                    - 2 * r_x(c.Mt, MT) ** 2
                                                    - 2 * r_x(c.MZ, MT) ** 4 + r_x(c.Mt, MT) ** 4
                                                    + r_x(c.Mt, MT) ** 2 * r_x(c.MZ, MT) ** 2))
                                                + (c.Cst3 * MT / (c.MW ** 2)
                                                * np.sqrt(lambda_func(MT, c.Mt, c.Mh))
                                                * (1 + r_x(c.Mt, MT) ** 2 - r_x(c.Mh, MT) ** 2))))
            return kappa



    def get_xs_pp_TT(self):
        mT = self.get_mT()
        xs_pp_TT = xsec_pp_TT_from_pred(mT)
        return xs_pp_TT

    def get_brTbw_XT(self):
        gamma_wb = self.T_decay_to_wb_TX()
        gamma_zt = self.T_decay_to_zt_TX()
        gamma_ht = self.T_decay_to_ht_TX()
        br_to_wb = gamma_wb / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_wb

    def get_brBwt_BY(self):
        gamma_wb = self.B_decay_to_wb_BY()
        gamma_zt = self.B_decay_to_zt_BY()
        gamma_ht = self.B_decay_to_ht_BY()
        br_to_wb = gamma_wb / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_wb

    def get_brTzt_XT(self):
        gamma_wb = self.T_decay_to_wb_TX()
        gamma_zt = self.T_decay_to_zt_TX()
        gamma_ht = self.T_decay_to_ht_TX()
        br_to_zt = gamma_zt / (gamma_ht + gamma_wb + gamma_zt) # + gamma_wb
        return br_to_zt

    def get_brBzb_BY(self):
        gamma_wb = self.B_decay_to_wt_BY()
        gamma_zt = self.B_decay_to_zb_BY()
        gamma_ht = self.B_decay_to_hb_BY()
        br_to_zt = gamma_zt / (gamma_ht + gamma_wb + gamma_zt) # + gamma_wb
        return br_to_zt

    def get_brTht_XT(self):
        gamma_wb = self.decay_to_wb_TX()
        gamma_zt = self.decay_to_zt_TX()
        gamma_ht = self.decay_to_ht_TX()
        br_to_ht = gamma_ht / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_ht

    def get_brBhb_BY(self):
        gamma_wb = self.B_decay_to_wt_BY()
        gamma_zt = self.B_decay_to_zb_BY()
        gamma_ht = self.B_decay_to_hb_BY()
        br_to_ht = gamma_ht / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_ht

    def get_brTzt_TB(self):
        gamma_zt = self.T_decay_to_zt_TB()
        gamma_ht = self.T_decay_to_ht_TB()
        br_to_zt = gamma_zt / (gamma_ht + gamma_zt)
        return br_to_zt

    def get_brBzb_TB(self):
        gamma_zt = self.B_decay_to_zb_TB()
        gamma_ht = self.B_decay_to_hb_TB()
        br_to_zt = gamma_zt / (gamma_ht + gamma_zt)
        return br_to_zt

    def get_brTht_TB(self):
        gamma_zt = self.T_decay_to_zt_TB()
        gamma_ht = self.T_decay_to_ht_TB()
        br_to_ht = gamma_ht / (gamma_ht + gamma_zt)
        return br_to_ht

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
        s_l = np.sqrt((r_x(c.Mt, self.mT_theo) * tg_r) ** 2 / (1 + ((r_x(c.Mt, self.mT_theo) * tg_r) ** 2)))
        return s_l

    def get_coupling_strength(self):
        if self.width_ratio is None:
            if self.kappa is None:
                if self.which_d == 'XT':
                    c_r = np.sqrt(1 - self.sin_r ** 2)
                    return self.sin_r * c_r
                elif self.which_d == 'BY':
                    c_r = np.sqrt(1 - self.sin_r ** 2)
                    return self.sin_r * c_r
                else:
                    c_u_r = np.sqrt(1 - self.sin_u_r ** 2)
                    return self.sin_u_r * c_u_r
            else:
                return self.kappa
        else:
            kappa = self.kappa_coupling_from_width()
            return kappa


class PureDecay:

    def __init__(self):
        self.mT_theo = None
        self.xs_pp_TT = None
        self.__model = 'Pure'

    def set_mT(self, mv):
        self.mT_theo = mv

    def set_xsec_pp_TT(self, cs_pp_TT):
        self.xs_pp_TT = cs_pp_TT

    def get_mT(self):
        return self.mT_theo

    def get_xs_pp_TT(self):
        return self.xs_pp_TT

    def model(self):
        return self.__model


def check_mass_range(m):
    s = Singlet()
    t = Tables(s)
    t.initialize_tables_cms_and_atlas()
    mini = float("inf")
    maxi = float("-inf")
    for i, k in enumerate(t.key):
        if min(t.MT[i]) < mini:
            mini = min(t.MT[i])
        if max(t.MT[i]) > maxi:
            maxi = max(t.MT[i])
    if m < mini or m > maxi:
        raise Exception(f"Error in mass range. It must between {mini} and {maxi}")
