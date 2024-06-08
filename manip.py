import numpy as np
from scipy.interpolate import interp1d, LinearNDInterpolator
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

    def doublet_single_prod_calc(self):
        # single production of T associated with tq (pp->Ttq)
        pp_vtq_tztq = self.m.vtq() * self.m.br_vzt()
        pp_vtq_thtq = self.m.vtq() * self.m.br_vht()
        combination = pp_vtq_thtq + pp_vtq_tztq

        return pp_vtq_tztq, pp_vtq_thtq, combination

    def doublet_tb_single_prod_calc(self):
        if self.m.get_sin_up_right() is not None:
            pp_vtq_tztq = self.m.vtq() * self.m.br_vzt_tb_doublet()
            pp_vtq_thtq = self.m.vtq() * self.m.br_vht_tb_doublet()
            combination = pp_vtq_tztq + pp_vtq_thtq

            return pp_vtq_tztq, pp_vtq_thtq, combination
        else:
            return -1, -1, -1

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
                    if k in c.kappa_keys['k=0.1']["Singlet"]:
                        if k == '07045f8a':
                            if 0.1 <= kappa <= 1.1:
                                index = self.key.index(k)
                                return self.process[index]
                            else:
                                return ''
                        else:
                            if abs(kappa - 0.1) < c.Threshold:
                                index = self.key.index(k)
                                return self.process[index]
                    elif k in c.kappa_keys['k=0.2']["Singlet"]:
                        if abs(kappa - 0.4) < c.Threshold:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.kappa_keys['k=0.3']["Singlet"]:
                        if k == '07045f8b':
                            if 0.1 <= kappa <= 1.1:
                                index = self.key.index(k)
                                return self.process[index]
                            else:
                                return ''
                        elif k == '07584f8a':
                            if abs(kappa - 0.3) < c.Threshold:
                                index = self.key.index(k)
                                return self.process[index]
                            else:
                                return ''
                        else:
                            return ''
                    elif k in c.kappa_keys['k=0.4']["Singlet"]:
                        if abs(kappa - 0.4) < c.Threshold:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.kappa_keys['k=0.5']["Singlet"]:
                        if k == '07045f8c':
                            if 0.1 <= kappa <= 1.1:
                                index = self.key.index(k)
                                return self.process[index]
                            else:
                                return ''
                        else:
                            if abs(kappa - 0.5) < c.Threshold:
                                index = self.key.index(k)
                                return self.process[index]
                            else:
                                return ''
                    elif k in c.kappa_keys['k=0.6']["Singlet"]:
                        if abs(kappa - 0.6) < c.Threshold:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.kappa_keys['k=0.7']["Singlet"]:
                        if k == '07045f8d':
                            if 0.1 <= kappa <= 1.1:
                                index = self.key.index(k)
                                return self.process[index]
                            else:
                                return ''
                        else:
                            if abs(kappa - 0.7) < c.Threshold:
                                index = self.key.index(k)
                                return self.process[index]
                            else:
                                return ''
                    elif k in c.kappa_keys['k=0.9']["Singlet"]:
                        if k == '07045f8e':
                            if 0.1 <= kappa <= 1.1:
                                index = self.key.index(k)
                                return self.process[index]
                            else:
                                return ''
                        else:
                            if abs(kappa - 0.9) < c.Threshold:
                                index = self.key.index(k)
                                return self.process[index]
                    elif k in c.kappa_keys['k=1.1']["Singlet"]:
                        if k == '07045f8f':
                            if 0.1 <= kappa <= 1.1:
                                index = self.key.index(k)
                                return self.process[index]
                            else:
                                return ''
                        else:
                            if abs(kappa - 1.1) < c.Threshold:
                                index = self.key.index(k)
                                return self.process[index]
                else:
                    print("universal coupling is None")
                if r is not None:
                    if k in c.ratio_keys['r<=0.05']["Singlet"]:
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
                    elif k in c.ratio_keys['r=0.1']["Singlet"]:
                        if abs(r - 0.1) < c.Threshold:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.ratio_keys['r<=0.1']["Singlet"]:
                        if r <= 0.1:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.ratio_keys['r=0.2']["Singlet"]:
                        if abs(r - 0.2) < c.Threshold:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.ratio_keys['r=0.3']["Singlet"]:
                        if abs(r - 0.3) < c.Threshold:
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
                    if k in c.kappa_keys['k=0.2']["Doublet"]:
                        if abs(kappa - 0.2) < c.Threshold:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.kappa_keys['k=0.3']["Doublet"]:
                        if abs(kappa - 0.3) < c.Threshold:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.kappa_keys['k=0.4']["Doublet"]:
                        if abs(kappa - 0.4) < c.Threshold:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.kappa_keys['k=0.5']["Doublet"]:
                        if abs(kappa - 0.5) < c.Threshold:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.kappa_keys['k=0.6']["Doublet"]:
                        if abs(kappa - 0.6) < c.Threshold:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.kappa_keys['k=0.7']["Doublet"]:
                        if abs(kappa - 0.7) < c.Threshold:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    else:
                        index = self.key.index(k)
                        return self.process[index]
                else:
                    print("universal coupling is None")

                if r is not None:
                    if k in c.ratio_keys['r<=0.05']["Doublet"]:
                        if r <= 0.05:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.ratio_keys['r=0.1']["Doublet"]:
                        if abs(r - 0.1) < c.Threshold:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.ratio_keys['r<=0.1']["Doublet"]:
                        if r <= 0.1:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.ratio_keys['r=0.2']["Doublet"]:
                        if abs(r - 0.2) < c.Threshold:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    elif k in c.ratio_keys['r=0.3']["Doublet"]:
                        if abs(r - 0.3) < c.Threshold:
                            index = self.key.index(k)
                            return self.process[index]
                        else:
                            return ''
                    else:
                        index = self.key.index(k)
                        return self.process[index]
                else:
                    print("width to mass ratio is None")

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
            if self.get_process(self.key[i], r, self.process[i], kappa) == "pp --> Tbq --> tZbq --> E_T + j":
                return self.m.vbq() * self.m.br_vzt()
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Tbq --> tZbq --> l+l- + j':
                return self.m.vbq() * self.m.br_vzt()
            elif self.get_process(self.key[i], r, self.process[i], kappa) == "pp --> Tbq --> tHbq --> j":
                return self.m.vbq() * self.m.br_vht()
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Tbq --> tHbq --> l+ + E_T + j'):
                return self.m.vbq() * self.m.br_vht()
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Tbq --> tHbq --> l+ + gamma + E_T + j'):
                return self.m.vbq() * self.m.br_vht()
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Tbq --> tZbq --> j':
                return self.m.vbq() * self.m.br_vzt()
            elif self.get_process(self.key[i], r, self.process[i], kappa) == "pp --> Tbq --> tZbq --> bbj":
                return self.m.vbq() * self.m.br_vzt() * c.BR_Z_bb
            elif self.get_process(self.key[i], r, self.process[i], kappa) == "pp --> Tbq --> tHbq --> bbj":
                return self.m.vbq() * self.m.br_vht() * c.BR_h_bb
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Tbq --> bWbq --> l+ + E_T + j'):
                return self.m.vbq() * self.m.br_vbw()
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Tbq --> (tZ + tH)bq --> j':
                return self.m.vbq() * self.m.br_vzt() + self.m.vbq() * self.m.br_vht()
            elif self.get_process(self.key[i], r, self.process[i], kappa) == "pp --> Tbq --> (tH + tZ)bq --> bbj":
                return self.m.vbq() * self.m.br_vzt() * c.BR_Z_bb + self.m.vbq() * self.m.br_vht() * c.BR_h_bb
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Tbq --> tZ(H)bq --> l+ + E_T + j'):
                return self.m.vbq() * self.m.br_vht()
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  "pp --> Tb(t)q --> tZbq --> l+l- + l+l+l-"):
                return self.m.vbq() * self.m.br_vzt() + self.m.vtq() * self.m.br_vzt()
            elif self.get_process(self.key[i], r, self.process[i], kappa)[:9] == 'pp --> TT':
                return pp_vvbar
            elif self.get_process(self.key[i], r, self.process[i], kappa) == '':
                return -1

        elif self.m.model() == 'Doublet':
            #vt_th_lnub, vt_z_l, vt_h_b, vt_z_q, combined3, combined4 = self.doublet_single_prod_calc()
            cs_pp_vtq_tztq, cs_pp_vtq_thtq, th_plus_tz_combination = self.doublet_single_prod_calc()

            #vtj_h_b, vtj_z_q, combined_3, vtj_th_lnub = self.doublet_tb_single_prod_calc()
            cs_pp_vtq_tztq_tb, cs_pp_vtq_thtq_tb, tz_th_combination_tb = self.doublet_tb_single_prod_calc()

            if self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Ttq --> tZtq --> l+l- + j':
                return cs_pp_vtq_tztq
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Ttq --> tHtq --> j':
                if self.key[i] in c.Doublet_TB:
                    return cs_pp_vtq_thtq_tb
                else:
                    return cs_pp_vtq_thtq
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Ttq --> tHtq --> l+ + E_T + j'):
                return cs_pp_vtq_thtq
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Ttq --> tZtq --> j':
                if self.key[i] in c.Doublet_TB:
                    return cs_pp_vtq_tztq_tb
                else:
                    return cs_pp_vtq_tztq
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Ttq --> (tZ + tH)tq --> j':
                if self.key[i] in c.Doublet_TB:
                    return tz_th_combination_tb
                else:
                    return th_plus_tz_combination
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Ttq --> tZ(H)tq --> l+ + E_T + j'):
                if self.key[i] in c.Doublet_TB:
                    return cs_pp_vtq_thtq_tb
                else:
                    return cs_pp_vtq_thtq
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  "pp --> Ttq --> tZtq --> l+l- + l+l-l"):
                return cs_pp_vtq_tztq
            elif self.get_process(self.key[i], r, self.process[i], kappa) == '':
                return -1
            elif self.get_process(self.key[i], r, self.process[i], kappa)[:9] == 'pp --> TT':
                return pp_vvbar

        elif self.m.model() == 'Pure':
            if self.process[i][:9] == 'pp --> TT':
                return pp_vvbar
            elif self.process[i][:10] == 'pp --> Tbq':
                return self.m.vbq()
        else:
            raise Exception("Error in model name")

    def two_dim_interpolation(self, index, coupling, mass, obs_exp):
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

    def denominator(self, num, index, t):
        if 0 <= num:
            if min(self.MT[index]) <= self.m.mv() <= max(self.MT[index]):
                if index in [37, 38, 39, 40, 41, 42]:
                    denom = self.two_dim_interpolation(37, self.m.universal_coupling(), self.m.mv(), t)
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
