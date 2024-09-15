from decay_calc import *
from theory_XS import *


class DoubletY:

    def __init__(self):
        self.__model = 'Doublet'
        self.__mY_theo = None
        self.__sin_r = None
        self.__kappa = None
        self.__width_ratio = None
        self.__which_d = 'BY'

    def set_mY(self, my):
        self.__mY_theo = my

    def set_sin_r(self, s_r):
        self.__sin_r = s_r

    def set_coupling_strength(self, k):
        self.__kappa = k

    def set_width_mass_ratio(self, wr):
        self.__width_ratio = wr

    def get_mY(self):
        return self.__mY_theo

    def get_which_doublet(self):
        return self.__which_d

    def get_coupling_strength(self):
        if self.__width_ratio is None:
            if self.__kappa is None:
                return self.__sin_r
            else:
                return self.__kappa
        else:
            k_x = kappa_coupling_from_width(self.get_mY(), self.__width_ratio)
            return k_x

    def model(self):
        return self.__model

    def get_sin_right(self):
        if self.__sin_r is not None:
            return abs(self.__sin_r)
        elif self.__kappa is not None:
            return self.__kappa
        elif self.__width_ratio:
            k_y = kappa_coupling_from_width(self.get_mY(), self.__width_ratio)
            return k_y

    def sin_left_calc(self, s_r):
        mx = self.get_mY()
        c_r = np.sqrt(1 - s_r ** 2)
        tg_r = s_r / c_r
        s_l = np.sqrt((r_x(c.Mb, mx) * tg_r) ** 2 / (1 + ((r_x(c.Mb, mx) * tg_r) ** 2)))
        return s_l

    def y_decay_to_wb(self):
        my = self.get_mY()
        s_r = self.get_sin_right()
        s_l = self.sin_left_calc(s_r)
        coupling = [s_r, s_l]
        width = calculate_decay_width([my, c.MW, c.Mb], self.__sin_r, self.__kappa,
                                      self.__width_ratio, coupling, c.Cst1, model='Doublet')
        return width

    def get_width_mass_ratio(self):
        my = self.get_mY()
        if self.__width_ratio is None:
            return self.y_decay_to_wb() / my
        else:
            return self.__width_ratio

    def get_xs_pp_QQ(self):
        mY = self.get_mY()
        xs_pp_YY = get_theo_xs_from_tables(mY, 'pp_QQ_NNLO.dat')
        return xs_pp_YY / 1000


class TripletY:

    def __init__(self):
        self.__model = 'Triplet'
        self.__mY_theo = None
        self.__s_d_l = None
        self.__kappa = None
        self.__width_ratio = None
        self.__which_d = 'TBY'

    def set_mY(self, my):
        self.__mY_theo = my

    def set_sin_down_left(self, s_d_l):
        self.__s_d_l = s_d_l

    def set_coupling_strength(self, k):
        self.__kappa = k

    def set_width_mass_ratio(self, wr):
        self.__width_ratio = wr

    def get_mY(self):
        return self.__mY_theo

    def get_which_doublet(self):
        return self.__which_d

    def get_coupling_strength(self):
        if self.__width_ratio is None:
            if self.__kappa is None:
                return np.sqrt(2) * self.__s_d_l
            else:
                return self.__kappa
        else:
            k_y = kappa_coupling_from_width(self.get_mY(), self.__width_ratio)
            return k_y

    def model(self):
        return self.__model

    def get_sin_down_left(self):
        if self.__s_d_l is not None:
            return abs(self.__s_d_l)
        elif self.__kappa is not None:
            return self.__kappa
        elif self.__width_ratio:
            k_y = kappa_coupling_from_width(self.get_mY(), self.__width_ratio)
            return k_y

    def sin_right_down_calc(self, s_d_l):
        my = self.get_mY()
        c_d_l = np.sqrt(1 - s_d_l ** 2)
        tg_d_l = s_d_l / c_d_l
        s_r = np.sqrt((r_x(c.Mb, my) * tg_d_l) ** 2 / (1 + ((r_x(c.Mb, my) * tg_d_l) ** 2)))
        return s_r

    def y_decay_to_wb(self):
        my = self.get_mY()
        s_d_l = self.get_sin_down_left()
        s_d_r = self.sin_right_down_calc(s_d_l)
        coupling = [s_d_l, 0]
        width = calculate_decay_width([my, c.MW, c.Mb], self.__s_d_l, self.__kappa,
                                      self.__width_ratio, coupling, c.Cst1, model='Triplet')
        return width

    def get_width_mass_ratio(self):
        my = self.get_mY()
        if self.__width_ratio is None:
            return self.y_decay_to_wb() / my
        else:
            return self.__width_ratio

    def get_xs_pp_QQ(self):
        mY = self.get_mY()
        xs_pp_YY = get_theo_xs_from_tables(mY, 'pp_QQ_NNLO.dat')
        return xs_pp_YY / 1000
