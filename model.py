import numpy as np
import constants as c
from initialize import Tables
from utils import *


class Singlet:
    def __init__(self, mv=None, pp_vv=None, pp_vbq=None, pp_vtq=None, sin=None):
        self.mv_theo = mv
        self.cs_pp_vv = pp_vv
        self.cs_pp_vbq = pp_vbq
        self.cs_pp_vtq = pp_vtq
        self.__model = 'Singlet'
        self.sin_l = sin

    def decay_to_wb(self):
        s_l = self.sin_l

        constant = c.G**2 / (64 * c.PI)

        gamma = (constant * self.mv_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mv_theo, c.Mb, c.MW))
                 * s_l ** 2 * (1 + r_x(c.MW, self.mv_theo) ** 2 - 2 * r_x(c.Mb, self.mv_theo) ** 2 -
                 2 * r_x(c.MW, self.mv_theo) ** 4 + r_x(c.Mb, self.mv_theo) ** 4
                 + r_x(c.Mb, self.mv_theo) ** 2 * r_x(c.MW, self.mv_theo) ** 2))
        return gamma, gamma / self.mv_theo

    def decay_to_zt(self):
        s_l = self.sin_l
        c_l = np.sqrt(1 - s_l ** 2)

        constant = c.G ** 2 / (128 * c.PI * c.C_W ** 2)

        gamma = (constant * self.mv_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mv_theo, c.Mt, c.MZ))
                 * (s_l * c_l) ** 2 * (1 + r_x(c.MZ, self.mv_theo) ** 2 - 2 * r_x(c.Mt, self.mv_theo) ** 2
                 - 2 * r_x(c.MZ, self.mv_theo) ** 4 + r_x(c.Mt, self.mv_theo) ** 4
                 + r_x(c.Mt, self.mv_theo) ** 2 * r_x(c.MZ, self.mv_theo) ** 2))

        return gamma, gamma / self.mv_theo

    def decay_to_ht(self):
        s_l = self.sin_l
        c_l = np.sqrt(1 - s_l ** 2)

        constant = c.G ** 2 / (128 * c.PI)

        gamma = (constant * self.mv_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mv_theo, c.Mt, c.MZ))
                 * (s_l * c_l) ** 2 * (1 + 6 * r_x(c.Mt, self.mv_theo) ** 2
                 - r_x(c.Mh, self.mv_theo) ** 2 + r_x(c.Mt, self.mv_theo) ** 4
                 - r_x(c.Mt, self.mv_theo) ** 2 * r_x(c.Mh, self.mv_theo) ** 2))

        return gamma, gamma / self.mv_theo

    def get_width_mass_ratio_from_wb(self):
        g, r = self.decay_to_wb()
        return r

    def get_width_mass_ratio_from_zt(self):
        g, r = self.decay_to_zt()
        return r

    def get_width_mass_ratio_from_ht(self):
        g, r = self.decay_to_ht()
        return r

    def mv(self):
        return self.mv_theo

    def vv(self):
        return self.cs_pp_vv

    def vbq(self):
        return self.cs_pp_vbq

    def vtq(self):
        return self.cs_pp_vtq

    def br_vbw(self):
        gamma_wb, r1 = self.decay_to_wb()
        gamma_zt, r2 = self.decay_to_zt()
        gamma_ht, r3 = self.decay_to_ht()
        br_to_wb = gamma_wb / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_wb

    def br_vzt(self):
        gamma_wb, r1 = self.decay_to_wb()
        gamma_zt, r2 = self.decay_to_zt()
        gamma_ht, r3 = self.decay_to_ht()
        br_to_zt = gamma_zt / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_zt

    def br_vht(self):
        gamma_wb, r1 = self.decay_to_wb()
        gamma_zt, r2 = self.decay_to_zt()
        gamma_ht, r3 = self.decay_to_ht()
        br_to_ht = gamma_ht / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_ht

    def sin_left(self):
        return abs(self.sin_l)

    def universal_coupling(self):
        return self.sin_left()

    def model(self):
        return self.__model


class Doublet:
    def __init__(self, mv=None, pp_vv=None, pp_vtq=None, sin_l=None):
        self.mv_theo = mv
        self.cs_pp_vv = pp_vv
        self.cs_pp_vtq = pp_vtq
        self.__model = 'Doublet'
        self.sin_l = sin_l
        self.sin_u_r = None
        self.sin_d_r = None

    def set_sin_up_right(self, sin_u_r):
        self.sin_u_r = sin_u_r

    def set_sin_down_right(self, sin_d_r):
        self.sin_d_r = sin_d_r

    def get_sin_up_right(self):
        return self.sin_u_r

    def get_sin_d_right(self):
        return self.sin_d_r

    def decay_to_wb(self):
        s_l = self.sin_l

        constant = c.G**2 / (64 * c.PI)

        gamma = (constant * self.mv_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mv_theo, c.Mb, c.MW))
                 * s_l ** 2 * (1 + r_x(c.MW, self.mv_theo) ** 2 - 2 * r_x(c.Mb, self.mv_theo) ** 2 -
                 2 * r_x(c.MW, self.mv_theo) ** 4 + r_x(c.Mb, self.mv_theo) ** 4
                 + r_x(c.Mb, self.mv_theo) ** 2 * r_x(c.MW, self.mv_theo) ** 2))
        return gamma, gamma / self.mv_theo

    def decay_to_zt(self):
        s_l = self.sin_l
        c_l = np.sqrt(1 - s_l ** 2)
        s_r = self.sin_right()
        c_r = np.sqrt(1 - s_r ** 2)

        constant = c.G ** 2 / (128 * c.PI * c.C_W ** 2)

        gamma = (constant * self.mv_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mv_theo, c.Mt, c.MZ))
                 * ((2 * s_l * c_l) ** 2 + (s_r * c_r) ** 2) * ((1 + r_x(c.MZ, self.mv_theo) ** 2
                                                                 - 2 * r_x(c.Mt, self.mv_theo) ** 2
                                                                 - 2 * r_x(c.MZ, self.mv_theo) ** 4
                                                                 + r_x(c.Mt, self.mv_theo) ** 4
                                                                 + r_x(c.Mt, self.mv_theo) ** 2
                                                                 * r_x(c.MZ, self.mv_theo) ** 2)
                                                                 - 12 * r_x(c.MZ, self.mv_theo) ** 2
                                                                 * r_x(c.Mt, self.mv_theo) * 2
                                                                 * s_l * c_l * s_r * c_r))

        return gamma, gamma / self.mv_theo

    def decay_to_ht(self):
        s_r = self.sin_right()
        c_r = np.sqrt(1 - s_r ** 2)

        constant = c.G ** 2 / (128 * c.PI)

        gamma = (constant * self.mv_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mv_theo, c.Mt, c.Mh))
                 * (s_r * c_r) ** 2 * (1 + 6 * r_x(c.Mt, self.mv_theo) ** 2
                 - r_x(c.Mh, self.mv_theo) ** 2 + r_x(c.Mt, self.mv_theo) ** 4
                 - r_x(c.Mt, self.mv_theo) ** 2 * r_x(c.Mh, self.mv_theo) ** 2))

        return gamma, gamma / self.mv_theo

    def decay_to_wb_tb_doublet(self):
        s_u_r = self.get_sin_up_right()
        c_u_r = np.sqrt(1 - s_u_r ** 2)
        s_d_r = self.get_sin_d_right()
        c_d_r = np.sqrt(1 - s_d_r ** 2)

        constant = c.G**2 / (64 * c.PI)

        gamma = (constant * self.mv_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mv_theo, c.Mb, c.MW))
                 * (c_u_r * s_d_r) ** 2 * (1 + r_x(c.MW, self.mv_theo) ** 2 - 2 * r_x(c.Mb, self.mv_theo) ** 2 -
                 2 * r_x(c.MW, self.mv_theo) ** 4 + r_x(c.Mb, self.mv_theo) ** 4
                 + r_x(c.Mb, self.mv_theo) ** 2 * r_x(c.MW, self.mv_theo) ** 2))
        return gamma, gamma / self.mv_theo

    def decay_to_zt_tb_doublet(self):
        s_u_r = self.get_sin_up_right()
        c_u_r = np.sqrt(1 - s_u_r ** 2)
        s_d_r = self.get_sin_d_right()
        c_d_r = np.sqrt(1 - s_d_r ** 2)

        constant = c.G ** 2 / (128 * c.PI * c.C_W ** 2)

        gamma = (constant * self.mv_theo / (c.MZ ** 2) * np.sqrt(lambda_func(self.mv_theo, c.Mt, c.MZ))
                 * (s_u_r * c_u_r) ** 2 * ((1 + r_x(c.MZ, self.mv_theo) ** 2 -
                                          2 * r_x(c.Mt, self.mv_theo) ** 2 - 2 * r_x(c.MZ, self.mv_theo) ** 4 +
                                          r_x(c.Mt, self.mv_theo) ** 4 + r_x(c.Mt, self.mv_theo) ** 2
                                          * r_x(c.MZ, self.mv_theo) ** 2)))

        return gamma, gamma / self.mv_theo

    def decay_to_ht_tb_doublet(self):
        s_u_r = self.get_sin_up_right()
        c_u_r = np.sqrt(1 - s_u_r ** 2)
        s_d_r = self.get_sin_d_right()
        c_d_r = np.sqrt(1 - s_d_r ** 2)

        constant = c.G ** 2 / (128 * c.PI)

        gamma = (constant * self.mv_theo / (c.MW ** 2) * np.sqrt(lambda_func(self.mv_theo, c.Mt, c.Mh))
                 * ((s_u_r * c_u_r) ** 2 + (r_x(c.Mt,self.mv_theo)*s_u_r * c_u_r) ** 2)
                 * (1 + 6 * r_x(c.Mt, self.mv_theo) ** 2
                 - r_x(c.Mh, self.mv_theo) ** 2 + r_x(c.Mt, self.mv_theo) ** 4
                 - r_x(c.Mt, self.mv_theo) ** 2 * r_x(c.Mh, self.mv_theo) ** 2))

        return gamma, gamma / self.mv_theo

    def get_width_mass_ratio_from_wb(self):
        g, r = self.decay_to_wb()
        return r

    def get_width_mass_ratio_from_zt(self):
        g, r = self.decay_to_zt()
        return r

    def get_width_mass_ratio_from_ht(self):
        g, r = self.decay_to_ht()
        return r

    def mv(self):
        return self.mv_theo

    def vv(self):
        return self.cs_pp_vv

    def vtq(self):
        return self.cs_pp_vtq

    def br_vbw(self):
        gamma_wb, r1 = self.decay_to_wb()
        gamma_zt, r2 = self.decay_to_zt()
        gamma_ht, r3 = self.decay_to_ht()
        br_to_wb = gamma_wb / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_wb

    def br_vzt(self):
        gamma_wb, r1 = self.decay_to_wb()
        gamma_zt, r2 = self.decay_to_zt()
        gamma_ht, r3 = self.decay_to_ht()
        br_to_zt = gamma_zt / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_zt

    def br_vht(self):
        gamma_wb, r1 = self.decay_to_wb()
        gamma_zt, r2 = self.decay_to_zt()
        gamma_ht, r3 = self.decay_to_ht()
        br_to_ht = gamma_ht / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_ht

    def br_vbw_tb_doublet(self):
        gamma_wb, r1 = self.decay_to_wb_tb_doublet()
        gamma_zt, r2 = self.decay_to_zt_tb_doublet()
        gamma_ht, r3 = self.decay_to_ht_tb_doublet()
        br_to_wb = gamma_wb / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_wb

    def br_vzt_tb_doublet(self):
        gamma_wb, r1 = self.decay_to_wb_tb_doublet()
        gamma_zt, r2 = self.decay_to_zt_tb_doublet()
        gamma_ht, r3 = self.decay_to_ht_tb_doublet()
        br_to_zt = gamma_zt / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_zt

    def br_vht_tb_doublet(self):
        gamma_wb, r1 = self.decay_to_wb_tb_doublet()
        gamma_zt, r2 = self.decay_to_zt_tb_doublet()
        gamma_ht, r3 = self.decay_to_ht_tb_doublet()
        br_to_ht = gamma_ht / (gamma_ht + gamma_wb + gamma_zt)
        return br_to_ht

    def sin_left(self):
        return abs(self.sin_l)

    def sin_right(self):
        s_l = self.sin_l
        c_l = np.sqrt(1 - s_l ** 2)
        tg_l = s_l / c_l
        s_r = np.sqrt((r_x(c.Mt, self.mv_theo) * tg_l) ** 2 / (1 + (r_x(c.Mt, self.mv_theo) * tg_l) ** 2))
        return s_r

    def universal_coupling(self):
        return  abs(self.sin_l)

    def model(self):
        return self.__model


class PureDecay:
    def __init__(self, mv, pp_vv, pp_vbq, pp_vtq):
        self.mv_theo = mv
        self.cs_pp_vv = pp_vv
        self.cs_pp_vbq = pp_vbq
        self.cs_pp_vtq = pp_vtq
        self.br_v_bW = 1
        self.br_v_tz = 1
        self.br_v_th = 1
        self.__model = 'Pure'

    def mv(self):
        return self.mv_theo

    def vv(self):
        return self.cs_pp_vv

    def vbq(self):
        return self.cs_pp_vbq

    def vtq(self):
        return self.cs_pp_vtq

    def br_vbw(self):
        return self.br_v_bW

    def br_vzt(self):
        return self.br_v_tz

    def br_vht(self):
        return self.br_v_th

    def model(self):
        return self.__model


def check_mass_range(m):
    s = Singlet()
    t = Tables(s)
    t.initialize_tables_cms_and_atlas()
    minimum = 1000000
    maximum = -1
    for i in range(len(t.key)):
        if min(t.MT[i]) < minimum:
            minimum = min(t.MT[i])
        if max(t.MT[i]) > maximum:
            maximum = max(t.MT[i])
    if m < minimum or m > maximum:
        raise Exception(f"Error in mass range. It must between {minimum} and {maximum}")
