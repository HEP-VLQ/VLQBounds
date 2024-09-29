from vlqBounds.utils.theory_XS import get_theo_xs_from_tables, get_data_from_files, interpolate2d
from vlqBounds.utils.decay_calc import *


class SingletT:

    def __init__(self):
        self.__model = 'Singlet'
        self.__mT_theo = None
        self.__sin_l = None
        self.__kappa = None
        self.__width_ratio = None

    def set_mT(self, mT):
        self.__mT_theo = mT

    def set_sin_l(self, s_l):
        self.__sin_l = s_l

    def set_coupling_strength(self, k):
        self.__kappa = k

    def set_width_mass_ratio(self, wr):
        self.__width_ratio = wr

    def model(self):
        return self.__model

    def get_mT(self):
        return self.__mT_theo

    def get_sin_left(self):
        if self.__sin_l is not None:
            return self.__sin_l
        else:
            if self.__kappa is not None:
                return self.__kappa / np.sqrt(2)
            else:
                if self.__width_ratio is not None:
                    kappa = kappa_coupling_from_width(self.get_mT(), self.__width_ratio)
                    return kappa / np.sqrt(2)

    def get_width_mass_ratio(self):
        if self.__width_ratio is None:
            g1 = self.T_decay_to_wb()
            g2 = self.T_decay_to_ht()
            g3 = self.T_decay_to_zt()
            gamma_mv_ratio = (g1 + g2 + g3) / self.__mT_theo
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
            k = kappa_coupling_from_width(self.get_mT(), self.__width_ratio)
            return k

    def get_xs_pp_QQ(self):
        mT = self.get_mT()
        xs_pp_TT = get_theo_xs_from_tables(mT, 'pp_QQ_NNLO.dat')
        return xs_pp_TT / 1000

    def get_xs_pp_Tbq_Wbbq(self, i):
        mT = self.get_mT()
        if i == 30:
            file = '1602.05606_ATLAS_Fig6_pp_T_Wb_singlet_theo.dat'
            xs_Tb_Wb = get_theo_xs_from_tables(mT, file)
            return xs_Tb_Wb
        elif i == 58:
            file = '1701.08328_CMS_fig5_pp_T_bW_singlet_C05_theo.dat'
            xs_Tb_Wb = get_theo_xs_from_tables(mT, file)
            return xs_Tb_Wb

    def get_xs_pp_Tj_Ztj_ts_channels(self, i):
        mT = self.get_mT()
        coupling_strength_value = self.get_coupling_strength()
        relative_width_arr = relative_width_value = None
        if i in [32, 33, 34]:
            MT_arr, coupling_strength_arr, xs_theo_arr = get_data_from_files('2305.03401', 'singlet')

            theo_input = (MT_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mT, relative_width_value, coupling_strength_value)

            xs_Tj_Zt = interpolate2d(expt_input=(None,), theo_input=theo_input, case='theo')

            return xs_Tj_Zt / 1000

        elif i in [43, 44, 45]:
            MT_arr, coupling_strength_arr, xs_theo_arr = get_data_from_files('2307.07584', 'singlet')

            theo_input = (MT_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mT, relative_width_value, coupling_strength_value)

            xs_Tj_Zt = interpolate2d(expt_input=(None,), theo_input=theo_input, case='theo')

            return xs_Tj_Zt

        elif i == 35:
            file = '2402.16561_ATLAS_fig9c_pp_T_Zt_singlet_k05_theo.dat'

            xs_Tj_Zt = get_theo_xs_from_tables(mT, file)

            return xs_Tj_Zt / 1000

    def get_xs_pp_Tbq_tHbq(self, i):
        mT = self.get_mT()
        s_l = self.get_sin_left()
        if i in [37, 38, 39, 40, 41, 42]:
            coupling_strength_value = self.get_coupling_strength()

            relative_width_arr = relative_width_value = None

            MT_arr, coupling_strength_arr, xs_theo_arr = get_data_from_files('2201.07045', 'Singlet')

            theo_input = (MT_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mT, relative_width_value, coupling_strength_value)

            xs_Tb_tH = interpolate2d(expt_input=(None,), theo_input=theo_input, case='theo')

            return xs_Tb_tH / 1000

        elif i == 17:
            file = '1612.00999_CMS_Fig10left_pp_T_tH_C05_singlet_theo.dat'

            xs_Tb_tH = get_theo_xs_from_tables(mT, file)

            return xs_Tb_tH

        elif i == 46:
            file = '1612.05336_CMS_fig4upperleft_pp_T_tH_c05_singlet_theo.dat'

            xs_Tb_tH = get_theo_xs_from_tables(mT, file)

            return xs_Tb_tH

        elif i == 16:
            relative_width_arr = relative_width_value = None

            MT_arr, s_l_arr, xs_theo_arr = get_data_from_files('2302.12802', 'singlet')

            theo_input = (MT_arr, relative_width_arr, s_l_arr, xs_theo_arr,
                          mT, relative_width_value, s_l)

            xs_Tb_tH = interpolate2d(expt_input=(None,), theo_input=theo_input, case='theo')

            return xs_Tb_tH / 1000

        elif i in [18, 19, 24, 25]:
            relative_width_value = self.get_width_mass_ratio()

            coupling_strength_arr = coupling_strength_value = None

            MT_arr, relative_width_arr, xs_theo_arr = get_data_from_files('2201.02227', 'Singlet')

            theo_input = (MT_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mT, relative_width_value, coupling_strength_value)

            xs_Tb_tH = interpolate2d(expt_input=(None,), theo_input=theo_input, case='theo')

            return xs_Tb_tH


    def get_xs_pp_Tbq_tZbq(self, i):
        mT = self.get_mT()
        relative_width_value = self.get_width_mass_ratio()
        if i == 57:
            file = '1806.10555_ATLAS_fig15_pp_T_Zt_Singlet_k05_theo.dat'
            xs_Tb_tZ = get_theo_xs_from_tables(mT, file)
            return xs_Tb_tZ
        elif i == 31:
            file = '1701.07409_CMS_Fig4left_pp_T_tZ_singlet_theo.dat'
            xs_Tb_tZ = get_theo_xs_from_tables(mT, file)
            return xs_Tb_tZ
        elif i == 14:
            file = '1708.01062_CMS_Fig5left_pp_T_tZ_singlet_C05_theo.dat'
            xs_Tb_tZ = get_theo_xs_from_tables(mT, file)
            return xs_Tb_tZ
        elif i == 36:
            file = '1812.09743_ATLAS_Fig4c_pp_T_tZ_Singlet_theo.dat'
            xs_Tb_tZ = get_theo_xs_from_tables(mT, file)
            return xs_Tb_tZ
        elif i in [10, 11, 12, 13]:
            coupling_strength_arr = coupling_strength_value = None

            MT_arr, relative_width_arr, xs_theo_arr = get_data_from_files('2201.02227', 'Singlet')

            theo_input = (MT_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mT, relative_width_value, coupling_strength_value)

            xs_Tb_tZ = interpolate2d(expt_input=(None,), theo_input=theo_input, case='theo')

            return xs_Tb_tZ

        elif i in [50, 51]:
            if i == 50:
                file = '2405.05071_CMS_Fig4ur_pp_T_Zt_singlet_theo.dat'

                xs_Tb_tZ = get_theo_xs_from_tables(mT, file)

                return xs_Tb_tZ
            else:
                file = '2405.05071_CMS_Fig4ul_pp_T_tH_singlet_theo.dat'
                xs_Tb_tZ = get_theo_xs_from_tables(mT, file)
                return xs_Tb_tZ
        elif i in [20, 21, 26, 27]:
            coupling_strength_arr = coupling_strength_value = None

            MT_arr, relative_width_arr, xs_theo_arr = get_data_from_files('2201.02227', 'Singlet')

            theo_input = (MT_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mT, relative_width_value, coupling_strength_value)

            xs_Tb_tZ = interpolate2d(expt_input=(None,), theo_input=theo_input, case='theo')

            return xs_Tb_tZ

    def get_xs_pp_Tbq_tZ_plus_TH(self, i):
        mT = self.get_mT()
        relative_width_value = self.get_width_mass_ratio()
        if i in [52, 53]:
            if i == 52:
                file = '2405.05071_CMS_Fig4ll_pp_T_ZttH_singlet_theo.dat'
                xs_Tb_tZ_tH = get_theo_xs_from_tables(mT, file)
                return xs_Tb_tZ_tH
            else:
                file = '2405.05071_CMS_Fig4lr_pp_T_ZttH_singlet_theo.dat'
                xs_Tb_tZ_tH = get_theo_xs_from_tables(mT, file)
                return xs_Tb_tZ_tH
        elif i in [22, 23, 28, 29]:
            coupling_strength_arr = coupling_strength_value = None

            MT_arr, relative_width_arr, xs_theo_arr = get_data_from_files('2201.02227', 'Singlet')

            theo_input = (MT_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mT, relative_width_value, coupling_strength_value)

            xs_Tb_tZ = interpolate2d(expt_input=(None,), theo_input=theo_input, case='theo')

            return xs_Tb_tZ * 2
    def get_xs_pp_Tbq(self, i):
        mT = self.get_mT()
        relative_width_value = self.get_width_mass_ratio()
        if i == 15:
            coupling_strength_arr = coupling_strength_value = None

            MT_arr, relative_width_arr, xs_theo_arr = get_data_from_files('2201.02227', 'Singlet')

            theo_input = (MT_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mT, relative_width_value, coupling_strength_value)

            xs_Tb_tZ = interpolate2d(expt_input=(None,), theo_input=theo_input, case='theo')

            xs_Tb = xs_Tb_tZ / 0.25

            return xs_Tb
    def T_decay_to_wb(self):
        mT = self.get_mT()
        s_l = self.get_sin_left()
        coupling = [s_l, 0]
        width = calculate_decay_width([mT, c.MW, c.Mb], self.__sin_l, self.__kappa,
                                      self.__width_ratio, coupling, c.Cst1)
        return width
    def T_decay_to_zt(self):
        mT = self.get_mT()
        s_l = self.get_sin_left()
        c_l = np.sqrt(1 - s_l ** 2)
        coupling = [s_l * c_l, 0]
        width = calculate_decay_width([mT, c.MZ, c.Mt], self.__sin_l, self.__kappa, self.__width_ratio, coupling, c.Cst2)
        return width
    def T_decay_to_ht(self):
        mT = self.get_mT()
        s_l = self.get_sin_left()
        c_l = np.sqrt(1 - s_l ** 2)
        coupling = s_l * c_l
        width = calculate_decay_width([mT, c.Mh, c.Mt], self.__sin_l, self.__kappa, self.__width_ratio,
                                      coupling, c.Cst3, to_higgs=True)
        return width

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

    def get_coupling_to_zt_or_ht(self):
        c_l = np.sqrt(1 - self.__sin_l ** 2)
        if self.__width_ratio is None:
            if self.__kappa is None:
                if self.__sin_l is not None:
                    return self.__sin_l * c_l
                else:
                    raise Exception("Width, universal coupling and mixing are all None.")
            else:
                return self.__kappa / np.sqrt(2)
        else:
            return kappa_coupling_from_width(self.get_mT(), self.__width_ratio) / np.sqrt(2)


class DoubletT:

    def __init__(self):
        self.__model = 'Doublet'
        self.__mT_theo = None
        self.__sin_r = None
        self.__sin_u_r = None
        self.__kappa = None
        self.__width_ratio = None
        self.__which_d = 'XT'

    def set_mT(self, mT):
        self.__mT_theo = mT

    def set_sin_r(self, s_r):
        self.__sin_r = s_r

    def set_sin_u_r(self, s_u_r):
        self.__sin_u_r = s_u_r

    def set_coupling_strength(self, k):
        self.__kappa = k

    def set_width_mass_ratio(self, wr):
        self.__width_ratio = wr

    def change_to_TB(self):
        self.__which_d = 'TB'

    def get_mT(self):
        return self.__mT_theo

    def get_which_doublet(self):
        return self.__which_d

    def get_coupling_strength(self):
        if self.__width_ratio is None:
            if self.__kappa is None:
                if self.__which_d == 'XT':
                    c_r = np.sqrt(1 - self.__sin_r ** 2)
                    return self.__sin_r * c_r
                else:
                    c_u_r = np.sqrt(1 - self.__sin_u_r ** 2)
                    return self.__sin_u_r * c_u_r
            else:
                return self.__kappa
        else:
            kappa = kappa_coupling_from_width(self.get_mT(), self.__width_ratio)
            return kappa

    def model(self):
        return self.__model

    def get_sin_up_right(self):
        if self.__sin_u_r is not None:
            return abs(self.__sin_u_r)
        else:
            return

    def get_sin_right(self):
        if self.__sin_r is not None:
            return abs(self.__sin_r)
        else:
            return

    def get_width_mass_ratio(self):
        if self.__width_ratio is None:
            if self.__which_d == 'XT':
                g2 = self.T_decay_to_zt_TX()
                g3 = self.T_decay_to_ht_TX()
                gamma_mv_ratio = (g2 + g3) / self.__mT_theo
                return gamma_mv_ratio
            else:
                g2 = self.T_decay_to_zt_TB()
                g3 = self.T_decay_to_ht_TB()
                gamma_mv_ratio = (g2 + g3) / self.__mT_theo
                return gamma_mv_ratio
        else:
            return self.__width_ratio

    def get_xs_pp_QQ(self):
        mT = self.get_mT()
        xs_pp_TT = get_theo_xs_from_tables(mT, 'pp_QQ_NNLO.dat')
        return xs_pp_TT

    def get_xs_pp_Tj_Ztj_ts_channels(self, i):
        mT = self.get_mT()
        coupling_strength_value = self.get_coupling_strength()
        if i in [23, 24, 25]:
            relative_width_arr = relative_width_value = None

            MT_arr, coupling_strength_arr, xs_theo_arr = get_data_from_files('2305.03401', 'doublet')

            theo_input = (MT_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mT, relative_width_value, coupling_strength_value)

            xs_Tj_Zt = interpolate2d(expt_input=(None,), theo_input=theo_input)

            return xs_Tj_Zt / 1000

        elif i in [26, 27, 28]:
            relative_width_arr = relative_width_value = None
            MT_arr, coupling_strength_arr, xs_theo_arr = get_data_from_files('2307.07584', 'doublet')

            theo_input = (MT_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mT, relative_width_value, coupling_strength_value)

            xs_Tj_Zt = interpolate2d(expt_input=(None,), theo_input=theo_input)
            return xs_Tj_Zt

    def get_xs_pp_Ttq_tZtq(self, i):
        mT = self.get_mT()
        relative_width_value = self.get_width_mass_ratio()

        if i == 21:
            file = '1701.07409_CMS_Fig4right_pp_T_tZ_doublet_C05_theo.dat'
            xs_pp_Ttq_tZtq = get_theo_xs_from_tables(mT, file)
            return xs_pp_Ttq_tZtq

        elif i == 7:
            file = '1708.01062_CMS_Fig5right_pp_T_tZ_doublet_C05_theo.dat'
            xs_pp_Ttq_tZtq = get_theo_xs_from_tables(mT, file)
            return xs_pp_Ttq_tZtq

        elif i in [11, 12, 17, 18]:
            coupling_strength_arr = coupling_strength_value = None

            MT_arr, relative_width_arr, xs_theo_arr = get_data_from_files('1909.04721', 'doublet')

            theo_input = (MT_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mT, relative_width_value, coupling_strength_value)

            xs_Tj_Zt = interpolate2d(expt_input=(None,), theo_input=theo_input)

            return xs_Tj_Zt / 2

    def get_xs_pp_Ttq_tHtq(self, i):
        mT = self.get_mT()
        relative_width_value = self.get_width_mass_ratio()
        if i == 5:
            file = '1701.07409_CMS_Fig4right_pp_T_tZ_doublet_C05_theo.dat'
            Ttq_tHtq = get_theo_xs_from_tables(mT, file)
            return Ttq_tHtq
        elif i == 29:
            file = '1612.05336_CMS_fig4lowerright_pp_T_tH_c05_doublet_theo_dat'
            Ttq_tHtq = get_theo_xs_from_tables(mT, file)
            return Ttq_tHtq

        elif i in [9, 10, 15, 16]:
            coupling_strength_arr = coupling_strength_value = None

            MT_arr, relative_width_arr, xs_theo_arr = get_data_from_files('1909.04721', 'doublet')

            theo_input = (MT_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mT, relative_width_value, coupling_strength_value)

            xs_Tj_tH = interpolate2d(expt_input=(None,), theo_input=theo_input)

            return xs_Tj_tH / 2

    def get_xs_pp_Ttq_tZ_plus_TH(self, i):
        mT = self.get_mT()
        relative_width_value = self.get_width_mass_ratio()
        if i in [13, 14, 19, 20]:
            coupling_strength_arr = coupling_strength_value = None

            MT_arr, relative_width_arr, xs_theo_arr = get_data_from_files('1909.04721', 'doublet')

            theo_input = (MT_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
                          mT, relative_width_value, coupling_strength_value)

            xs_Tj_tH_tZ = interpolate2d(expt_input=(None,), theo_input=theo_input)

            return xs_Tj_tH_tZ

    def T_decay_to_wb_TX(self):
        mT = self.get_mT()
        if self.__sin_r is not None:
            s_l = self.sin_left_calc(self.__sin_r)
            width = calculate_width(c.Cst1, mT, c.MW, [s_l, 0], c.Mb)
            return width
        else:
            raise Exception("Calculation error. 'sin_r' is None.")

    def T_decay_to_zt_TX(self):
        mT = self.get_mT()
        s_r = self.get_sin_right()
        c_r = np.sqrt(1 - s_r ** 2)
        s_l = self.sin_left_calc(s_r)
        c_l = np.sqrt(1 - s_l ** 2)
        coupling = [s_r * c_r, 2 * s_l * c_l]
        width = calculate_decay_width([mT, c.MZ, c.Mt], self.__sin_r, self.__kappa,
                                      self.__width_ratio, coupling, c.Cst2,  model='Doublet')
        return width

    def T_decay_to_ht_TX(self):
        mT = self.get_mT()
        s_r = self.get_sin_right()
        c_r = np.sqrt(1 - s_r ** 2)
        coupling = [s_r * c_r, 0]
        width = calculate_decay_width([mT, c.Mh, c.Mt], self.__sin_r, self.__kappa, self.__width_ratio,
                                      coupling, c.Cst3,  model='Doublet', to_higgs=True)
        return width

    def T_decay_to_zt_TB(self):
        mT = self.get_mT()
        if self.get_sin_up_right() is not None:
            s_u_r = self.get_sin_up_right()
            c_u_r = np.sqrt(1 - s_u_r ** 2)
            coupling = [s_u_r * c_u_r, 0]
        else:
            coupling = 0
        width = calculate_decay_width([mT, c.MZ, c.Mt], self.__sin_u_r, self.__kappa, self.__width_ratio,
                                      coupling, c.Cst2,  model='Doublet')
        return width

    def T_decay_to_ht_TB(self):
        mT = self.get_mT()
        if self.get_sin_up_right() is not None:
            s_u_r = self.get_sin_up_right()
            c_u_r = np.sqrt(1 - s_u_r ** 2)
            coupling = [s_u_r * c_u_r, 0]
        else:
            coupling = 0
        width = calculate_decay_width([mT, c.Mh, c.Mt], self.__sin_u_r, self.__kappa, self.__width_ratio,
                                      coupling, c.Cst3,  model='Doublet', to_higgs=True)
        return width

    def get_brTbw_XT(self):
        gamma_wb = self.T_decay_to_wb_TX()
        gamma_zt = self.T_decay_to_zt_TX()
        gamma_ht = self.T_decay_to_ht_TX()
        br_to_wb = gamma_wb / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_wb

    def get_brTzt_XT(self):
        gamma_wb = self.T_decay_to_wb_TX()
        gamma_zt = self.T_decay_to_zt_TX()
        gamma_ht = self.T_decay_to_ht_TX()
        br_to_zt = gamma_zt / (gamma_ht + gamma_wb + gamma_zt) # + gamma_wb
        return br_to_zt

    def get_brTht_XT(self):
        gamma_wb = self.T_decay_to_wb_TX()
        gamma_zt = self.T_decay_to_zt_TX()
        gamma_ht = self.T_decay_to_ht_TX()
        br_to_ht = gamma_ht / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_ht

    def get_brTzt_TB(self):
        gamma_zt = self.T_decay_to_zt_TB()
        gamma_ht = self.T_decay_to_ht_TB()
        br_to_zt = gamma_zt / (gamma_ht + gamma_zt)
        return br_to_zt

    def get_brTht_TB(self):
        gamma_zt = self.T_decay_to_zt_TB()
        gamma_ht = self.T_decay_to_ht_TB()
        br_to_ht = gamma_ht / (gamma_ht + gamma_zt)
        return br_to_ht

    def sin_left_calc(self, s_r):
        mT = self.get_mT()
        c_r = np.sqrt(1 - s_r ** 2)
        tg_r = s_r / c_r
        s_l = np.sqrt((r_x(c.Mt, mT) * tg_r) ** 2 / (1 + ((r_x(c.Mt, mT) * tg_r) ** 2)))
        return s_l


class PureTDecay:

    def __init__(self):
        self.__mT_theo = None
        self.__model = 'Pure'

    def set_mT(self, mv):
        self.__mT_theo = mv

    def get_mT(self):
        return self.__mT_theo

    def get_xs_pp_TT(self):
        mT = self.get_mT()
        xs_pp_TT = get_theo_xs_from_tables(mT, 'pp_QQ_NNLO.dat')
        return xs_pp_TT

    def model(self):
        return self.__model

