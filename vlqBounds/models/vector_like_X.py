from vlqBounds.utils.decay_calc import *
from vlqBounds.utils.theory_XS import get_theo_xs_from_tables, get_data_from_files


class DoubletX:

    def __init__(self):
        self.__model = 'Doublet'
        self.__mX_theo = None
        self.__sin_r = None
        self.__kappa = None
        self.__width_ratio = None
        self.__which_d = 'XT'

    def set_mX(self, mx):
        self.__mX_theo = mx

    def set_sin_r(self, s_r):
        self.__sin_r = s_r

    def set_coupling_strength(self, k):
        self.__kappa = k

    def set_width_mass_ratio(self, wr):
        self.__width_ratio = wr

    def get_mX(self):
        return self.__mX_theo

    def get_which_doublet(self):
        return self.__which_d

    def get_coupling_strength(self):
        if self.__width_ratio is None:
            if self.__kappa is None:
                return self.__sin_r

            else:
                return self.__kappa
        else:
            k_x = kappa_coupling_from_width(self.get_mX(), self.__width_ratio)
            return k_x

    def model(self):
        return self.__model

    def get_sin_right(self):
        if self.__sin_r is not None:
            return abs(self.__sin_r)
        elif self.__kappa is not None:
            return self.__kappa
        elif self.__width_ratio is not None:
            k_x = kappa_coupling_from_width(self.get_mX(), self.__width_ratio)
            return k_x

    def sin_left_calc(self, s_r):
        mx = self.get_mX()
        c_r = np.sqrt(1 - s_r ** 2)
        tg_r = s_r / c_r
        s_l = np.sqrt((r_x(c.Mt, mx) * tg_r) ** 2 / (1 + ((r_x(c.Mt, mx) * tg_r) ** 2)))
        return s_l

    def x_decay_to_wt(self):
        mx = self.get_mX()
        s_r = self.get_sin_right()
        s_l = self.sin_left_calc(s_r)
        coupling = [s_r, 0]
        width = calculate_decay_width([mx, c.MW, c.Mt], self.__sin_r, self.__kappa,
                                      self.__width_ratio, coupling, c.Cst1, model='Doublet')
        return width

    def get_width_mass_ratio(self):
        mx = self.get_mX()
        if self.__width_ratio is None:
            return self.x_decay_to_wt() / mx
        else:
            return self.__width_ratio

    def get_xs_pp_Xtq_twtq(self, i):
        mX = self.get_mX()
        file = '1809.08597_Fig8_upper_right_pp_X_Wt_gamma_M1.dat'
        if i == 14:
            xs_pp_Xt_tW = get_theo_xs_from_tables(mX, file, vlq='X')
            return xs_pp_Xt_tW


    def get_xs_pp_QQ(self):
        mX = self.get_mX()
        xs_pp_XX = get_theo_xs_from_tables(mX, 'pp_QQ_NNLO.dat')
        return xs_pp_XX / 1000




