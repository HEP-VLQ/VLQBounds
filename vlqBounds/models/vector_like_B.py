from vlqBounds.utils.theory_XS import get_theo_xs_from_tables, get_data_from_files, interpolate2d
from vlqBounds.utils.decay_calc import *


class SingletB:

    def __init__(self):
        self.__model = 'Singlet'
        self.__mB_theo = None
        self.__sin_l = None
        self.__kappa = None
        self.__width_ratio = None

    def set_mB(self, mB):
        self.__mB_theo = mB

    def set_sin_l(self, s_l):
        self.__sin_l = s_l

    def set_coupling_strength(self, k):
        self.__kappa = k

    def set_width_mass_ratio(self, wr):
        self.__width_ratio = wr

    def model(self):
        return self.__model

    def get_mB(self):
        return self.__mB_theo

    def get_sin_left(self):
        if self.__sin_l is not None:
            return self.__sin_l
        else:
            if self.__kappa is not None:
                return self.__kappa / np.sqrt(2)
            else:
                if self.__width_ratio is not None:
                    kappa = kappa_coupling_from_width(self.get_mB(), self.__width_ratio)
                    return kappa / np.sqrt(2)

    def get_width_mass_ratio(self):
        if self.__width_ratio is None:
            g1 = self.B_decay_to_wt()
            g2 = self.B_decay_to_hb()
            g3 = self.B_decay_to_zb()
            gamma_mv_ratio = (g1 + g2 + g3) / self.__mB_theo
            return gamma_mv_ratio
        else:
            return self.__width_ratio

    def get_coupling_strength(self):
        if self.__width_ratio is None:
            if self.__kappa is None:
                return np.sqrt(2) * self.get_sin_left()
            else:
                return self.__kappa
        else:
            k = kappa_coupling_from_width(self.get_mB(), self.__width_ratio)
            return k

    def get_xs_pp_QQ(self):
        mB = self.get_mB()
        xs_pp_BB = get_theo_xs_from_tables(mB, 'pp_QQ_NNLO.dat')
        return xs_pp_BB / 1000

    def get_xs_pp_Bbq_tWbq(self, i):
        if i == 20:
            mB = self.get_mB()
            xs_pp_Bb_tW = get_theo_xs_from_tables(mB, '2111.10216_Fig4_left_pp_B_Wt_singlet_theo.dat', vlq='B')
            return xs_pp_Bb_tW

    def get_xs_pp_Btq_tWtq(self, i):
        if i == 21:
            mB = self.get_mB()
            xs_pp_Bb_tW = get_theo_xs_from_tables(mB, '2111.10216_Fig4_right_pp_Bt_Wt_singlet_theo.dat', vlq='B')
            return xs_pp_Bb_tW

    def get_xs_pp_Bj_bHj_ts_channels(self, i):
        if i in [15, 16, 17]:
            mB = self.get_mB()
            relative_width_arr = relative_width_value = None
            coupling_strength_value = self.get_coupling_strength()
            MB_arr, coupling_strength_arr, xs_theo_arr = get_data_from_files('2308.02595', 'singlet', 'B')
            theo_input = (MB_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mB, relative_width_value, coupling_strength_value)
            xs_pp_Bb_bH = interpolate2d(expt_input=(None,), theo_input=theo_input, case='theo')
            return xs_pp_Bb_bH


    def get_xs_pp_Bbq_bHbq(self, i):
        if i in [4, 5, 6, 7]:
            mB = self.get_mB()

            coupling_strength_arr = coupling_strength_value = None

            relative_width_value = self.get_width_mass_ratio()

            MB_arr, relative_width_arr, xs_theo_arr = get_data_from_files('1802.01486', 'singlet', 'B')

            theo_input = (MB_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mB, relative_width_value, coupling_strength_value)

            xs_pp_Bb_bH = interpolate2d(expt_input=(None,), theo_input=theo_input, case='theo')

            return xs_pp_Bb_bH

    def get_xs_pp_Bbq_bZbq(self, i):
        if i == 19:
            mB = self.get_mB()
            file = '1701.07409_Fig5_right_pp_Bt_bZ_cbZ05_singlet_theo.dat'
            xs_pp_Bb_bZ = get_theo_xs_from_tables(mB, file, vlq='B')
            return xs_pp_Bb_bZ

    def get_xs_pp_Btq_bZtq(self, i):
        if i == 18:
            mB = self.get_mB()
            file = '1701.07409_Fig5_left_pp_Bt_bZ_cWt05_singlet_theo.dat'
            xs_pp_Bt_bZ = get_theo_xs_from_tables(mB, file, vlq='B')
            return xs_pp_Bt_bZ

    def B_decay_to_wt(self):
        mB = self.get_mB()
        s_l = self.get_sin_left()
        coupling = [s_l, 0]
        width = calculate_decay_width([mB, c.MW, c.Mt], self.__sin_l, self.__kappa,
                                      self.__width_ratio, coupling, c.Cst1)
        return width

    def B_decay_to_zb(self):
        mB = self.get_mB()
        s_l = self.get_sin_left()
        c_l = np.sqrt(1 - s_l ** 2)
        coupling = [s_l * c_l, 0]
        width = calculate_decay_width([mB, c.MZ, c.Mb], self.__sin_l, self.__kappa,
                                      self.__width_ratio, coupling, c.Cst2)
        return width

    def B_decay_to_hb(self):
        mB = self.get_mB()
        s_l = self.get_sin_left()
        c_l = np.sqrt(1 - s_l ** 2)
        coupling = s_l * c_l
        width = calculate_decay_width([mB, c.Mh, c.Mb], self.__sin_l, self.__kappa,
                                      self.__width_ratio, coupling, c.Cst3, to_higgs=True)
        return width

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
        if self.__width_ratio is None:
            if self.__kappa is None:
                if self.__sin_l is not None:
                    return self.__sin_l * c_l
                else:
                    raise Exception("Width, universal coupling and mixing are all None.")
            else:
                return self.__kappa / np.sqrt(2)
        else:
            return kappa_coupling_from_width(self.get_mB(), self.__width_ratio) / np.sqrt(2)


class DoubletB:
    """indexes must be checked"""
    def __init__(self):
        self.__model = 'Doublet'
        self.__mB_theo = None
        self.__sin_r = None
        self.__sin_d_r = None
        self.__kappa = None
        self.__width_ratio = None
        self.__which_d = 'BY'

    def set_mB(self, mB):
        self.__mB_theo = mB

    def set_sin_r(self, s_r):
        self.__sin_r = s_r

    def set_sin_d_r(self, s_d_r):
        self.__sin_d_r = s_d_r

    def set_coupling_strength(self, k):
        self.__kappa = k

    def set_width_mass_ratio(self, wr):
        self.__width_ratio = wr

    def change_to_TB(self):
        self.__which_d = 'TB'

    def get_mB(self):
        return self.__mB_theo

    def get_which_doublet(self):
        return self.__which_d

    def model(self):
        return self.__model

    def get_sin_down_right(self):
        if self.__sin_d_r is not None:
            return self.__sin_d_r

    def get_coupling_strength(self):
        if self.__width_ratio is None:
            if self.__kappa is None:
                if self.__which_d == 'BY':
                    c_r = np.sqrt(1 - self.__sin_r ** 2)
                    return self.__sin_r * c_r
                else:
                    c_d_r = np.sqrt(1 - self.__sin_d_r ** 2)
                    return self.__sin_d_r * c_d_r
            else:
                return self.__kappa
        else:
            kappa = kappa_coupling_from_width(self.get_mB(), self.__width_ratio)
            return kappa

    def get_width_mass_ratio(self):
        if self.__width_ratio is None:
            if self.__which_d == 'BY':
                g2 = self.B_decay_to_zb_BY()
                g3 = self.B_decay_to_hb_BY()
                gamma_mB_ratio = (g2 + g3) / self.__mB_theo
                return gamma_mB_ratio
            else:
                g2 = self.B_decay_to_zb_TB()
                g3 = self.B_decay_to_hb_TB()
                gamma_mB_ratio = (g2 + g3) / self.__mB_theo
                return gamma_mB_ratio
        else:
            return self.__width_ratio

    def get_sin_right(self):
        if self.__sin_r is not None:
            return abs(self.__sin_r)

    def get_xs_pp_QQ(self):
        mB = self.get_mB()
        xs_pp_BB = get_theo_xs_from_tables(mB, 'pp_QQ_NNLO.dat')
        return xs_pp_BB / 1000

    def get_xs_pp_Bbq_bHbq(self, i):
        if i in [3, 4, 5, 6]:
            mB = self.get_mB()
            coupling_strength_arr = coupling_strength_value = None
            relative_width_value = self.get_width_mass_ratio()
            MB_arr, relative_width_arr, xs_theo_arr = get_data_from_files('1802.01486', 'doublet', 'B')
            theo_input = (MB_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mB, relative_width_value, coupling_strength_value)
            xs_pp_Bb_bH = interpolate2d(expt_input=(None,), theo_input=theo_input, case='theo')
            return xs_pp_Bb_bH

    def get_xs_pp_Bj_bHj_ts_channels(self, i):
        if i in [13, 14, 15]:
            mB = self.get_mB()
            relative_width_arr = relative_width_value = None
            coupling_strength_value = self.get_coupling_strength()
            MB_arr, coupling_strength_arr, xs_theo_arr = get_data_from_files('2308.02595', 'doublet', 'B')
            theo_input = (MB_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mB, relative_width_value, coupling_strength_value)
            xs_pp_Bb_bH = interpolate2d(expt_input=(None,), theo_input=theo_input, case='theo')
            return xs_pp_Bb_bH

    def get_xs_pp_Bbq_tWbq(self, i):
        if i == 18:
            mB = self.get_mB()
            xs_pp_Bb_tW = get_theo_xs_from_tables(mB, '2111.10216_Fig4_left_pp_B_Wt_doublet_theo.dat', vlq='B')
            return xs_pp_Bb_tW

    def B_decay_to_wt_BY(self):
        mB = self.get_mB()
        if self.__sin_r is not None:
            s_l = self.sin_left_calc(self.__sin_r)
            width = calculate_width(c.Cst1, mB, c.MW, [s_l, 0], c.MW)
            return width
        else:
            raise Exception("Calculation error: Width, universal coupling and mixing are all None.")

    def B_decay_to_zb_BY(self):
        mB = self.get_mB()
        s_l = self.sin_left_calc(self.get_sin_right())
        c_l = np.sqrt(1 - s_l ** 2)
        s_r = self.get_sin_right()
        c_r = np.sqrt(1 - s_r ** 2)
        coupling = [s_r * c_r, 0]
        width = calculate_decay_width([mB, c.MZ, c.Mb], self.__sin_r, self.__kappa,
                                      self.__width_ratio, coupling, c.Cst2, model='Doublet')
        return width

    def B_decay_to_hb_BY(self):
        mB = self.get_mB()
        s_r = self.get_sin_right()
        c_r = np.sqrt(1 - s_r ** 2)
        coupling = [s_r * c_r, 0]
        width = calculate_decay_width([mB, c.Mh, c.Mb], self.__sin_r, self.__kappa,
                                      self.__width_ratio, coupling, c.Cst3, model='Doublet', to_higgs=True)
        return width

    def B_decay_to_zb_TB(self):
        mB = self.get_mB()
        s_d_r = self.get_sin_down_right()
        c_d_r = np.sqrt(1 - s_d_r ** 2)
        coupling = [s_d_r * c_d_r, 0]
        width = calculate_decay_width([mB, c.MZ, c.Mb], self.__sin_d_r, self.__kappa,
                                      self.__width_ratio, coupling, c.Cst2,  model='Doublet')
        return width

    def B_decay_to_hb_TB(self):
        mB = self.get_mB()
        s_d_r = self.get_sin_down_right()
        c_d_r = np.sqrt(1 - s_d_r ** 2)
        coupling = [s_d_r * c_d_r, 0]
        width = calculate_decay_width([mB, c.Mh, c.Mb], self.__sin_d_r, self.__kappa,
                                      self.__width_ratio, coupling, c.Cst3,  model='Doublet', to_higgs=True)
        return width

    def get_brBwt_BY(self):
        gamma_wb = self.B_decay_to_wt_BY()
        gamma_zt = self.B_decay_to_zb_BY()
        gamma_ht = self.B_decay_to_hb_BY()
        br_to_wb = gamma_wb / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_wb

    def get_brBzb_BY(self):
        gamma_wb = self.B_decay_to_wt_BY()
        gamma_zb = self.B_decay_to_zb_BY()
        gamma_hb = self.B_decay_to_hb_BY()
        br_to_zb = gamma_zb / (gamma_hb + gamma_zb)
        return br_to_zb

    def get_brBhb_BY(self):
        gamma_wb = self.B_decay_to_wt_BY()
        gamma_zb = self.B_decay_to_zb_BY()
        gamma_hb = self.B_decay_to_hb_BY()
        br_to_hb = gamma_hb / (gamma_hb + gamma_zb)
        return br_to_hb

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

    def sin_left_calc(self, s_r):
        c_r = np.sqrt(1 - s_r ** 2)
        tg_r = s_r / c_r
        s_l = np.sqrt((r_x(c.Mb, self.__mB_theo) * tg_r) ** 2 / (1 + ((r_x(c.Mb, self.__mB_theo) * tg_r) ** 2)))
        return s_l


class PureB:

    def __init__(self):
        self.mB_theo = None
        self.__model = 'Pure'

    def set_mB(self, mB):
        self.mB_theo = mB

    def get_mB(self):
        return self.mB_theo

    def get_xs_pp_QQ(self):
        mB = self.get_mB()
        xs_pp_BB = get_theo_xs_from_tables(mB, 'pp_QQ_NNLO.dat')
        return xs_pp_BB / 1000

    def model(self):
        return self.__model
