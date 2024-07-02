import numpy as np
from scipy.interpolate import interp1d, LinearNDInterpolator, CloughTocher2DInterpolator
from initialize import Tables
from output import Result
import constants as c
from model import *
import sys


class TheoryCalc(Tables, Result):
    def __init__(self, m):
        Tables.__init__(self, m)
        Result.__init__(self)
        self.m = m

    def get_ratio_and_universal_coupling(self):
        if self.m.model() == 'Singlet' or self.m.model() == 'Doublet':
            r = self.m.get_width_mass_ratio()
            kappa = self.m.universal_coupling()
            return r, kappa
        else:
            return None, None

    def singlet_single_prod_calc(self):
        """single production of T associated with bq or tq (pp->Tb(t)q)"""

        pp_vbq_bwbq = self.m.vbq() * self.m.br_vbw()
        pp_vbq_tzbq = self.m.vbq() * self.m.br_vzt()
        pp_vbq_thbq = self.m.vbq() * self.m.br_vht()

        pp_vtq_tztq = self.m.vtq() * self.m.br_vzt()

        combination_1 = pp_vbq_tzbq + pp_vbq_thbq
        combination_2 = pp_vbq_tzbq + pp_vtq_tztq

        return pp_vbq_bwbq, pp_vbq_tzbq, pp_vbq_thbq, combination_1, combination_2

    def doublet_tb_single_prod_calc(self):
        if self.m.get_sin_up_right() is not None:
            pp_vtq_tztq = self.m.vtq() * self.m.br_vzt_tb_doublet()
            pp_vtq_thtq = self.m.vtq() * self.m.br_vht_tb_doublet()
            combination = pp_vtq_tztq + pp_vtq_thtq
            return pp_vtq_tztq, pp_vtq_thtq, combination
        else:
            raise Exception("Error, (T, B) can not be checked if sin^u_R is not set.")

    def doublet_single_prod_calc(self):
        pp_vtq_tztq = self.m.vtq() * self.m.br_vzt()
        pp_vtq_thtq = self.m.vtq() * self.m.br_vht()
        combination = pp_vtq_tztq + pp_vtq_thtq
        return pp_vtq_tztq, pp_vtq_thtq, combination

    def pair_prod_calc(self):
        return self.m.vv()

    def get_process(self, k, r, pr, kappa):
        if self.m.model() == 'Singlet':
            if k in self.cs_keys['pair_prod']:
                if pr in self.process:
                    index = self.key.index(k)
                    return self.process[index]
                else:
                    raise Exception("pair productions are not calculated")

            elif k in self.cs_keys['single_prod']:
                if kappa is not None:
                    if k in c.Kappa_keys['0.1<=k<=1.1']["Singlet"]:
                        if 0.1 <= kappa <= 1.1:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.Kappa_keys['0.2<=k<=0.6']["Singlet"]:
                        if 0.2 <= kappa <= 0.6:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.Kappa_keys['0.3<=k<=0.7']["Singlet"]:
                        if 0.3 <= kappa <= 0.7:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                else:
                    print("universal coupling is None")
                if r is not None:
                    if k in c.Ratio_keys['r<=0.05']["Singlet"]:
                        if r <= 0.05:
                            if k[:5] == "05071":
                                if abs(r - 0.01) < c.Threshold:
                                    index = self.key.index(k)
                                    return self.process[index]
                                else:
                                    return ''
                            else:
                                index = self.key.index(k)
                                return self.process[index]
                        else:
                            return ''
                    elif k in c.Ratio_keys['0.05<=r<=0.3']["Singlet"]:
                        if r <= 0.05 and (k == '02227fa' or k == '04721f8a' or k == '04721f9a'):
                            index = self.key.index(k)
                            return self.process[index]
                        elif 0.05 <= r <= 0.3:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.Ratio_keys['r<=0.1']["Singlet"]:
                        if r <= 0.1:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k == '072f8':
                        if self.m.br_vbw() >= 0.99:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    else:
                        index = self.key.index(k)
                        return self.process[index]
                else:
                    print("Width to mass ratio is None")

            else:
                raise Exception("Error. Single productions and pair production are not tested in the Doublet model")

        elif self.m.model() == 'Doublet':
            if k in self.cs_keys['pair_prod']:
                index = self.key.index(k)
                return self.process[index]

            elif k in self.cs_keys['single_prod']:
                if kappa is not None:
                    if k in c.Kappa_keys['0.2<=k<=0.6']["Doublet"]:
                        if 0.2 <= kappa <= 0.6:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.Kappa_keys['0.3<=k<=0.7']["Doublet"]:
                        if 0.3 <= kappa <= 0.7:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                else:
                    print("universal coupling is None")

                if r is not None:
                    if k in c.Ratio_keys['r<=0.05']["Doublet"]:
                        if r <= 0.05:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.Ratio_keys['0.05<=r<=0.3']["Doublet"]:
                        if r <= 0.05 and (k == '04721f10a' or k == '04721f11a'):
                            index = self.key.index(k)
                            return self.process[index]
                        elif 0.05 <= r <= 0.3:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.Ratio_keys['r<=0.1']["Doublet"]:
                        if r <= 0.1:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    else:
                        index = self.key.index(k)
                        return self.process[index]
                else:
                    print("Width to mass ratio is None")

            else:
                raise Exception("Error. Single productions and pair production are not tested in the Doublet model")
     
        elif self.m.model() == 'Pure':
            if k in self.cs_keys['pair_prod']:
                index = self.key.index(k)
                return self.process[index]
            elif k in self.cs_keys['single_prod']:
                index = self.key.index(k)
                return self.process[index]
            else:
                raise Exception(f"Error. Single production and pair production of {self.m.model()} are not calculated")
        else:
            raise Exception("Error in model name")

    def numerator(self, i):
        pp_vvbar = self.pair_prod_calc()
        r, kappa = self.get_ratio_and_universal_coupling()

        if self.m.model() == 'Singlet':
            if self.get_process(self.key[i], r, self.process[i], kappa) == "pp --> Tbq --> tZbq":
                return self.m.vbq() * self.m.br_vzt()
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Tbq --> tZbq':
                return self.m.vbq() * self.m.br_vzt()
            elif self.get_process(self.key[i], r, self.process[i], kappa) == "pp --> Tbq --> tHbq":
                return self.m.vbq() * self.m.br_vht()
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Tbq --> tHbq'):
                return self.m.vbq() * self.m.br_vht()
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Tbq --> tHbq'):
                return self.m.vbq() * self.m.br_vht()
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Tbq --> tZbq':
                return self.m.vbq() * self.m.br_vzt()
            elif self.get_process(self.key[i], r, self.process[i], kappa) == "pp --> Tbq --> tZbq --> tbbbq":
                return self.m.vbq() * self.m.br_vzt() * c.BR_Z_bb
            elif self.get_process(self.key[i], r, self.process[i], kappa) == "pp --> Tbq --> tHbq --> tbbbq":
                return self.m.vbq() * self.m.br_vht() * c.BR_h_bb
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Tbq --> bWbq'):
                return self.m.vbq() * self.m.br_vbw()
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Tbq --> (tZ + tH)bq':
                return self.m.vbq() * self.m.br_vzt() + self.m.vbq() * self.m.br_vht()
            elif self.get_process(self.key[i], r, self.process[i], kappa) == "pp --> Tbq --> (tH + tZ)bq --> tbbbq":
                return self.m.vbq() * self.m.br_vzt() * c.BR_Z_bb + self.m.vbq() * self.m.br_vht() * c.BR_h_bb
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Tbq --> tZ(H)bq'):
                return self.m.vbq() * self.m.br_vht()
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  "pp --> Tb(t)q --> tZbq"):
                return self.m.vbq() * self.m.br_vzt() + self.m.vtq() * self.m.br_vzt()
            elif self.get_process(self.key[i], r, self.process[i], kappa)[:9] == 'pp --> TT':
                return pp_vvbar
            elif self.get_process(self.key[i], r, self.process[i], kappa) == '':
                return -1

        elif self.m.model() == 'Doublet':
            if self.m.get_which_doublet() == 'TB':
                cs_pp_vtq_tztq_tb, cs_pp_vtq_thtq_tb, tz_th_combination_tb = self.doublet_tb_single_prod_calc()
                if self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Ttq --> tZtq':
                    if self.key[i] in self.TB_XT_keys['(T,B)']:
                        return cs_pp_vtq_tztq_tb
                    else:
                        return -1
                elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Ttq --> tHtq':
                    if self.key[i] in self.TB_XT_keys['(T,B)']:
                        return cs_pp_vtq_thtq_tb
                    else:
                        return -1
                elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Ttq --> (tZ + tH)tq':
                    if self.key[i] in self.TB_XT_keys['(T,B)']:
                        return tz_th_combination_tb
                    else:
                        return -1
                elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                      'pp --> Ttq --> tZ(H)tq'):
                    if self.key[i] in self.TB_XT_keys['(T,B)']:
                        return cs_pp_vtq_thtq_tb
                    else:
                        return -1
                elif self.get_process(self.key[i], r, self.process[i], kappa)[:9] == 'pp --> TT':
                    if self.key[i] in self.TB_XT_keys['(T,B)']:
                        return self.m.vv()
                    else:
                        return -1
                elif self.get_process(self.key[i], r, self.process[i], kappa) == '':
                    return -1
            else:
                cs_pp_vtq_tztq, cs_pp_vtq_thtq, tz_th_combination = self.doublet_single_prod_calc()
                if self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Ttq --> tZtq':
                    if self.key[i] in self.TB_XT_keys['(X,T)']:
                        return cs_pp_vtq_tztq
                    else:
                        return -1
                elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Ttq --> tHtq':
                    if self.key[i] in self.TB_XT_keys['(X,T)']:
                        return cs_pp_vtq_thtq
                    else:
                        return -1
                elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Ttq --> (tZ + tH)tq':
                    if self.key[i] in self.TB_XT_keys['(X,T)']:
                        return tz_th_combination
                    else:
                        return -1
                elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                      'pp --> Ttq --> tZ(H)tq'):
                    if self.key[i] in self.TB_XT_keys['(X,T)']:
                        return cs_pp_vtq_thtq
                    else:
                        return -1
                elif self.get_process(self.key[i], r, self.process[i], kappa)[:9] == 'pp --> TT':
                    if self.key[i] in self.TB_XT_keys['(X,T)']:
                        return self.m.vv()
                    else:
                        return -1
                elif self.get_process(self.key[i], r, self.process[i], kappa) == '':
                    return -1
        elif self.m.model() == 'Pure':
            if self.process[i][:9] == 'pp --> TT':
                return pp_vvbar
        else:
            raise Exception("Error in model name")


    def one_dim_interp(self, mass, interpoled):
        interp = interp1d(mass, interpoled, "linear")
        m_array = np.linspace(np.min(mass), np.max(mass),100)
        return interp(m_array)
    def two_dim_interpolation_2201_07(self, index, coupling, mass, obs_exp):
        k1 = 0.1 * np.ones(len(self.MT[index]))
        k2 = 0.3 * np.ones(len(self.MT[index + 1]))
        k3 = 0.5 * np.ones(len(self.MT[index + 2]))
        k4 = 0.7 * np.ones(len(self.MT[index + 3]))
        k5 = 0.9 * np.ones(len(self.MT[index + 4]))
        k6 = 1.1 * np.ones(len(self.MT[index + 5]))

        t1 = obs_exp[index]
        t2 = obs_exp[index + 1]
        t3 = obs_exp[index + 2]
        t4 = obs_exp[index + 3]
        t5 = obs_exp[index + 4]
        t6 = obs_exp[index + 5]

        m1 = self.MT[index]
        m2 = self.MT[index + 1]
        m3 = self.MT[index + 2]
        m4 = self.MT[index + 3]
        m5 = self.MT[index + 4]
        m6 = self.MT[index + 5]

        m = np.concatenate([m1, m2, m3, m4, m5, m6], axis=None)
        t_tot = np.concatenate([t1, t2, t3, t4, t5, t6], axis=None)
        k = np.concatenate([k1, k2, k3, k4, k5, k6], axis=None)

        interp = LinearNDInterpolator(list(zip(m, k)), t_tot)
        return interp(mass, coupling)

    def two_dim_interpolation_2307(self, index, coupling, mass, obs_exp):
        k1 = 0.3 * np.ones(len(self.MT[index]))
        k2 = 0.5 * np.ones(len(self.MT[index + 1]))
        k3 = 0.7 * np.ones(len(self.MT[index + 2]))

        t1 = obs_exp[index]
        t2 = obs_exp[index + 1]
        t3 = obs_exp[index + 2]

        m1 = self.MT[index]
        m2 = self.MT[index + 1]
        m3 = self.MT[index + 2]

        m = np.concatenate([m1, m2, m3], axis=None)
        t_tot = np.concatenate([t1, t2, t3], axis=None)
        k = np.concatenate([k1, k2, k3], axis=None)

        interp = LinearNDInterpolator(list(zip(m, k)), t_tot)
        return interp(mass, coupling)

    def two_dim_interpolation_2305(self, index, coupling, mass, obs_exp):
        k1 = 0.2 * np.ones(len(self.MT[index]))
        k2 = 0.4 * np.ones(len(self.MT[index + 1]))
        k3 = 0.6 * np.ones(len(self.MT[index + 2]))

        t1 = obs_exp[index]
        t2 = obs_exp[index + 1]
        t3 = obs_exp[index + 2]

        m1 = self.MT[index]
        m2 = self.MT[index + 1]
        m3 = self.MT[index + 2]

        m = np.concatenate([m1, m2, m3], axis=None)
        t_tot = np.concatenate([t1, t2, t3], axis=None)
        k = np.concatenate([k1, k2, k3], axis=None)

        interp = LinearNDInterpolator(list(zip(m, k)), t_tot)
        return interp(mass, coupling)

    def two_dim_interpolation_1909(self, index, width_mass_ratio, mass, obs_exp):
        if width_mass_ratio >= 0.05:
            width_to_mass = 0.05 * np.ones(len(self.MT[index]))
            width_to_mass2 = 0.1 * np.ones(len(self.MT[index + 1]))
            width_to_mass3 = 0.2 * np.ones(len(self.MT[index + 6]))
            width_to_mass4 = 0.3 * np.ones(len(self.MT[index + 7]))

            t1 = obs_exp[index]
            t2 = obs_exp[index + 1]
            t3 = obs_exp[index + 6]
            t4 = obs_exp[index + 7]

            m1 = self.MT[index]
            m2 = self.MT[index + 1]
            m3 = self.MT[index + 6]
            m4 = self.MT[index + 7]

            m = np.concatenate([m1, m2, m3, m4], axis=None)
            t_tot = np.concatenate([t1, t2, t3, t4], axis=None)
            k = np.concatenate([width_to_mass, width_to_mass2, width_to_mass3, width_to_mass4], axis=None)

            interp = LinearNDInterpolator(list(zip(m, k)), t_tot)
            return interp(mass, width_mass_ratio)
        else:
            expected_or_observed = interp1d(self.MT[index], obs_exp[index], 'linear')
            denom = expected_or_observed(self.m.mv())
            return denom

    def two_dim_interpolation_2201_02(self, index, width_mass_ratio, mass, obs_exp):
        if width_mass_ratio >= 0.05:
            width_to_mass = 0.05 * np.ones(len(np.linspace(np.min(self.MT[index]), np.max(self.MT[index]), 100)))
            width_to_mass2 = 0.1 * np.ones(len(np.linspace(np.min(self.MT[index+1]), np.max(self.MT[index+1]), 100)))
            width_to_mass3 = 0.2 * np.ones(len(np.linspace(np.min(self.MT[index+2]), np.max(self.MT[index+2]), 100)))
            width_to_mass4 = 0.3 * np.ones(len(np.linspace(np.min(self.MT[index+3]), np.max(self.MT[index+3]), 100)))

            t1 = obs_exp[index]
            t2 = obs_exp[index + 1]
            t3 = obs_exp[index + 2]
            t4 = obs_exp[index + 3]
            t1 = self.one_dim_interp(self.MT[index], t1)
            t2 = self.one_dim_interp(self.MT[index+1], t2)
            t3 = self.one_dim_interp(self.MT[index+2], t3)
            t4 = self.one_dim_interp(self.MT[index+3], t4)

            m1 = np.linspace(np.min(self.MT[index]), np.max(self.MT[index]), 100)
            m2 = np.linspace(np.min(self.MT[index+1]), np.max(self.MT[index+1]), 100)
            m3 = np.linspace(np.min(self.MT[index+2]), np.max(self.MT[index+2]), 100)
            m4 = np.linspace(np.min(self.MT[index+3]), np.max(self.MT[index+3]), 100)

            m = np.concatenate([m1, m2, m3, m4], axis=None)
            t_tot = np.concatenate([t1, t2, t3, t4], axis=None)
            w = np.concatenate([width_to_mass, width_to_mass2, width_to_mass3, width_to_mass4], axis=None)

            interp = LinearNDInterpolator(list(zip(m, w)), t_tot)
            return interp(mass, width_mass_ratio)
        else:
            expected_or_observed = interp1d(self.MT[index], obs_exp[index], 'linear')
            denom = expected_or_observed(self.m.mv())
            return denom

    def denominator(self, num, index, t):
        if 0 <= num:
            if min(self.MT[index]) <= self.m.mv() <= max(self.MT[index]):
                if self.m.model() == 'Singlet':
                    if index in [37, 38, 39, 40, 41, 42]:
                        denom = self.two_dim_interpolation_2201_07(37, self.m.universal_coupling(), self.m.mv(), t)
                        return denom
                    elif index in [42, 43, 44]:
                        denom = self.two_dim_interpolation_2307(43, self.m.universal_coupling(), self.m.mv(), t)
                        return denom
                    elif index in [32, 33, 34]:
                        denom = self.two_dim_interpolation_2305(32, self.m.universal_coupling(), self.m.mv(), t)
                        return denom
                    elif index in [18, 19, 24, 25]:
                        denom = self.two_dim_interpolation_1909(18, self.m.get_width_mass_ratio(), self.m.mv(), t)
                        return denom
                    elif index in [20, 21, 26, 27]:
                        denom = self.two_dim_interpolation_1909(20, self.m.get_width_mass_ratio(), self.m.mv(), t)
                        return denom
                    elif index in [22, 23, 28, 29]:
                        denom = self.two_dim_interpolation_1909(22, self.m.get_width_mass_ratio(), self.m.mv(), t)
                        return denom
                    elif index in [10, 11, 12, 13]:
                        denom = self.two_dim_interpolation_2201_02(10, self.m.get_width_mass_ratio(), self.m.mv(), t)
                        return denom
                    else:
                        expected_or_observed = interp1d(self.MT[index], t[index], 'linear')
                        denom = expected_or_observed(self.m.mv())
                        return denom
                elif self.m.model() == 'Doublet':
                    if index in [26, 27, 28]:
                        denom = self.two_dim_interpolation_2307(26, self.m.universal_coupling(), self.m.mv(), t)
                        return denom
                    elif index in [23, 24, 25]:
                        denom = self.two_dim_interpolation_2305(23, self.m.universal_coupling(), self.m.mv(), t)
                        return denom
                    elif index in [9, 10, 15, 16]:
                        denom = self.two_dim_interpolation_1909(9, self.m.get_width_mass_ratio(), self.m.mv(), t)
                        return denom
                    elif index in [11, 12, 17, 18]:
                        denom = self.two_dim_interpolation_1909(11, self.m.get_width_mass_ratio(), self.m.mv(), t)
                        return denom
                    elif index in [13, 14, 19, 20]:
                        denom = self.two_dim_interpolation_1909(13, self.m.get_width_mass_ratio(), self.m.mv(), t)
                        return denom
                    else:
                        expected_or_observed = interp1d(self.MT[index], t[index], 'linear')
                        denom = expected_or_observed(self.m.mv())
                        return denom
                else:
                    expected_or_observed = interp1d(self.MT[index], t[index], 'linear')
                    denom = expected_or_observed(self.m.mv())
                    return denom

            else:
                d = -1
                return d
        else:
            d = 1
            return d

    def expected_ratio_calc(self):
        try:
            maximum = -1000000
            pos = -1
            for index, k in enumerate(self.key):
                n = self.numerator(index)
                d = self.denominator(n, index, self.obs)
                if d == -1:
                    continue
                elif n == -1:
                    continue
                elif n != -1 and d != -1:
                    rat = n/d
                    if rat >= maximum:
                        maximum = rat
                        pos = index

            return pos
        except UnboundLocalError:
            sys.exit(f"The mass {self.m.MT()} is not in the range of included experiment files")
    
    def check_channel(self):
        position = self.expected_ratio_calc()
        numerator = self.numerator(position)
        deno = self.denominator(numerator, position, self.obs)
        observed_ratio = numerator / deno
        self.model_observed_ratio = observed_ratio
        if self.model_observed_ratio >= 1:
            self.allowed_or_excluded = 0
            self.channel = position
        elif self.model_observed_ratio < 0:
            self.allowed_or_excluded = -1
            self.channel = position
        else:
            self.allowed_or_excluded = 1
            self.channel = position
