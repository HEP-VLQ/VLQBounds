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
        self.NWA_input = True

    def get_ratio_and_universal_coupling(self):
        if self.m.model() == 'Singlet' or self.m.model() == 'Doublet':
            r = self.m.get_width_mass_ratio()
            kappa = self.m.get_coupling_strength()
            return r, kappa
        else:
            return None, None

    def get_channel(self, k, r, pr, kappa):
        if self.m.model() == 'Singlet':
            if k in self.cs_keys['pair_prod']:
                if pr in self.process:
                    index = self.key.index(k)
                    return index
                else:
                    raise Exception("pair productions are not calculated")

            elif k in self.cs_keys['single_prod']:
                if kappa is not None:
                    if k in c.Kappa_keys['0.1<=k<=1.1']["Singlet"]:
                        if 0.1 <= kappa <= 1.1:
                            index = self.key.index(k)
                            return index
                        else:
                            return ''
                    elif k in c.Kappa_keys['0.2<=k<=0.6']["Singlet"]:
                        if 0.2 <= kappa <= 0.6:
                            index = self.key.index(k)
                            return index
                        else:
                            return ''
                    elif k in c.Kappa_keys['0.3<=k<=0.7']["Singlet"]:
                        if 0.3 <= kappa <= 0.7:
                            index = self.key.index(k)
                            return index
                        else:
                            return ''
                    elif k in c.Kappa_keys['k==0.5']["Singlet"]:
                        if abs(kappa - 0.5) <= c.Threshold:
                            index = self.key.index(k)
                            return index
                        else:
                            return ''
                else:
                    raise Exception("Error. Coupling strength is None")
                if r is not None:
                    if k in c.Ratio_keys['r==0.01']["Singlet"]:
                        if abs(r - 0.01) <= c.Threshold:
                            index = self.key.index(k)
                            return index
                        else:
                            return ''
                    elif k in c.Ratio_keys['r<=0.05']["Singlet"]:
                        if r <= 0.05:
                            index = self.key.index(k)
                            return index
                        else:
                            return ''
                    elif k in c.Ratio_keys['r<=0.1']["Singlet"]:
                        if r <= 0.1:
                            index = self.key.index(k)
                            return index
                        else:
                            return ''
                    elif k in c.Ratio_keys['0.05<r<=0.3']["Singlet"]:
                        if 0.05 < r <= 0.3:
                            index = self.key.index(k)
                            return index
                        else:
                            return ''
                    else:
                        index = self.key.index(k)
                        return index
                else:
                    raise Exception("Error. Width-to-mass ratio is None")

            else:
                raise Exception("Error. Single productions and pair production are not tested in the Doublet model")

        elif self.m.model() == 'Doublet':
            if k in self.cs_keys['pair_prod']:
                index = self.key.index(k)
                return index

            elif k in self.cs_keys['single_prod']:
                if kappa is not None:
                    if k in c.Kappa_keys['0.2<=k<=0.6']["Doublet"]:
                        if 0.2 <= kappa <= 0.6:
                            index = self.key.index(k)
                            return index
                        else:
                            return ''
                    elif k in c.Kappa_keys['0.3<=k<=0.7']["Doublet"]:
                        if 0.3 <= kappa <= 0.7:
                            index = self.key.index(k)
                            return index
                        else:
                            return ''
                else:
                    Exception("Error. Coupling strength is None")

                if r is not None:
                    if k in c.Ratio_keys['r<=0.05']["Doublet"]:
                        if r <= 0.05:
                            index = self.key.index(k)
                            return index
                        else:
                            return ''
                    elif k in c.Ratio_keys['r<=0.1']["Doublet"]:
                        if r <= 0.1:
                            index = self.key.index(k)
                            return index
                        else:
                            return ''
                    elif k in c.Ratio_keys['0.05<r<=0.3']["Doublet"]:
                        if 0.05 < r <= 0.3:
                            index = self.key.index(k)
                            return index
                        else:
                            return ''
                    else:
                        index = self.key.index(k)
                        return index
                else:
                    raise Exception("Error. Width-to-mass ratio is None")

            else:
                raise Exception("Error. Single productions and pair production are not tested in the Doublet model")
     
        elif self.m.model() == 'Pure':
            if k in self.cs_keys['pair_prod']:
                index = self.key.index(k)
                return index
        else:
            raise Exception("Error in model name")

    def numerator(self, i):
        r, kappa = self.get_ratio_and_universal_coupling()

        if self.m.model() == 'Singlet':
            j = self.get_channel(self.key[i], r, self.process[i], kappa)
            if j in [32, 33, 34, 35, 43, 44, 45]:
                return self.m.get_xs_pp_Tj_Ztj_ts_channels(j) / 1000

            elif j in [37, 38, 39, 40, 41, 42, 17, 46, 16, 18, 19, 24, 25]:
                return self.m.get_xs_pp_Tbq_tHbq(j) / 1000

            elif j in [58, 31, 36, 14, 10, 11, 12, 13, 50, 51, 20, 21, 26, 27]:
                return self.m.get_xs_pp_Tbq_tZbq(j) / 1000

            elif j in [57, 30, 59]:
                return self.m.get_xs_pp_Tbq_Wbbq(j) / 1000

            elif j == 15:
                return self.m.get_xs_pp_Tbq(j) / 1000

            elif j in [52, 53, 22, 23, 28, 29]:
                return self.m.get_xs_pp_Tbq_tZ_plus_TH(j) / 1000

            elif j in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 47, 48, 49, 54, 55, 56]:
                return self.m.get_xs_pp_QQ() / 1000

            else:
                return -1
            '''
            elif self.get_process(self.key[i], r, self.process[i], kappa) == "pp --> Tbq --> tHbq":
                if self.nwa[i]:
                    if self.NWA_input:
                        return -1#self.m.get_xsec_pp_Tbq() * self.m.get_brTht()
                    else:
                        return -1
                else:
                    if not self.NWA_input:
                        return -1#self.m.get_xsec_pp_htbq()
                    else:
                        return -1
            elif self.get_process(self.key[i], r, self.process[i], kappa) == "pp --> Tbq --> tZbq --> tbbbq":
                if self.nwa[i]:
                    if self.NWA_input:
                        return -1#self.m.Tbq() * self.m.brTzt() * c.BR_Z_bb
                    else:
                        return -1
                else:
                    if not self.NWA_input:
                        return -1#self.m.get_xsec_pp_ztbq * c.BR_Z_bb
                    else:
                        return -1
            elif self.get_process(self.key[i], r, self.process[i], kappa) == "pp --> Tbq --> tHbq --> tbbbq":
                if self.nwa[i]:
                    if self.NWA_input:
                        return -1#self.m.get_xsec_pp_Tbq() * self.m.get_brTht() * c.BR_h_bb
                    else:
                        return -1
                else:
                    if not self.NWA_input:
                        return -1#self.m.get_xsec_pp_htbq() * c.BR_h_bb
                    else:
                        return -1
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Tbq --> bWbq'):
                if self.nwa[i]:
                    if self.NWA_input:
                        return -1#self.m.get_xsec_pp_Tbq() * self.m.get_brTbw()
                    else:
                        return -1
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Tbq --> (tZ + tH)bq':
                if self.nwa[i]:
                    if self.NWA_input:
                        return -1 #(self.m.get_xsec_pp_Tbq() * self.m.get_brTzt()
                                #+ self.m.get_xsec_pp_Tbq() * self.m.get_brTht())
                    else:
                        return -1
                else:
                    if not self.NWA_input:
                        return -1#self.m.get_xsec_pp_ztbq() + self.m.get_xsec_pp_htbq()
                    else:
                        return -1
            elif self.get_process(self.key[i], r, self.process[i], kappa) == "pp --> Tbq --> (tH + tZ)bq --> tbbbq":
                if self.nwa[i] and self.NWA_input:
                    return -1#(self.m.get_xsec_pp_Tbq() * self.m.get_brTzt() * c.BR_Z_bb
                            #+ self.m.get_xsec_pp_Tbq() * self.m.get_brTht() * c.BR_h_bb)
                else:
                    return -1
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  "pp --> Tb(t)q --> tZbq"):
                if self.nwa[i]:
                    if self.NWA_input:
                        return -1#(self.m.get_xsec_pp_Tbq() * self.m.get_brTzt()
                                #+ self.m.get_xsec_pp_Ttq() * self.m.get_brTzt())
                    else:
                        return -1
                else:
                    if not self.NWA_input:
                        return -1#self.m.get_xsec_pp_ztbq() + self.m.get_xsec_pp_zttq()
                    else:
                        return -1
            
            elif self.get_process(self.key[i], r, self.process[i], kappa) == '':
                return -1
        '''
        elif self.m.model() == 'Doublet':
            if self.m.get_which_doublet() == 'TB' or self.m.get_which_doublet() == 'XT':
                j = self.get_channel(self.key[i], r, self.process[i], kappa)
                if j in [23, 24, 25, 26, 27, 28]:
                    return self.m.get_xs_pp_Tj_Ztj_ts_channels(j) / 1000

                elif j in [5, 29, 9, 10, 15, 16]:
                    return self.m.get_xs_pp_Ttq_tHtq(j) / 1000

                elif j in [21, 7, 11, 12, 17, 18]:
                    return self.m.get_xs_pp_Ttq_tZtq(j) / 1000

                elif j in [13, 14, 19, 20]:
                    return self.m.get_xs_pp_Ttq_tZ_plus_TH(j) / 1000

                elif j in [0, 1, 2, 3, 4, 6, 8, 22, 30, 31, 32]:
                    return self.m.get_xs_pp_QQ() / 1000
                else:
                    return -1

        elif self.m.model() == 'Pure':
            if self.process[i][:9] == 'pp --> TT':
                return self.m.get_xs_pp_QQ() / 1000
        else:
            raise Exception("Error in model name")

    def interpolate2d(self, indexes, kappa, width_ratio, mass, obs_exp, width_ratio_array, coupling_array):
        if coupling_array is None:
            if width_ratio >= 0.05:
                interp = create_2d_interpolator(self.MT, width_ratio_array, obs_exp, indexes)
                return interp(mass, width_ratio)
            else:
                expected_or_observed = interp1d(self.MT[indexes[0]], obs_exp[indexes[0]], 'linear')
                denominator = expected_or_observed(self.m.get_mT())
                return denominator
        else:
            interp = create_2d_interpolator(self.MT, coupling_array, obs_exp, indexes)
            return interp(mass, kappa)

    def denominator(self, num, index, t):
        if index in [10, 11, 12, 13]:
            if 0 <= num:
                if min(self.MT[index]) <= self.m.get_mT() <= max(self.MT[index]):
                    if self.m.model() == 'Singlet':
                        if index in [37, 38, 39, 40, 41, 42]:
                            indexes = [37, 38, 39, 40, 41, 42]
                            coupling_array = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1]
                            kappa = self.m.get_coupling_strength()
                            mT = self.m.get_mT()
                            d = self.interpolate2d(indexes, kappa, None, mT, t, None, coupling_array)
                            return d
                        elif index in [43, 44, 45]:
                            indexes = [43, 44, 45]
                            coupling_array = [0.3, 0.5, 0.7]
                            kappa = self.m.get_coupling_strength()
                            mT = self.m.get_mT()
                            d = self.interpolate2d(indexes, kappa, None, mT, t, None, coupling_array)
                            return d
                        elif index in [32, 33, 34]:
                            indexes = [32, 33, 34]
                            coupling_array = [0.2, 0.4, 0.6]
                            kappa = self.m.get_coupling_strength()
                            mT = self.m.get_mT()
                            d = self.interpolate2d(indexes, kappa, None, mT, t, None, coupling_array)
                            return d
                        elif index in [18, 19, 24, 25]:
                            indexes = [18, 19, 24, 25]
                            width_ratio_array = [0.05, 0.1, 0.2, 0.3]
                            width_ratio = self.m.get_width_mass_ratio()
                            mT = self.m.get_mT()
                            d = self.interpolate2d(indexes, None, width_ratio, mT, t, width_ratio_array, None)
                            return d
                        elif index in [20, 21, 26, 27]:
                            indexes = [20, 21, 26, 27]
                            width_ratio_array = [0.05, 0.1, 0.2, 0.3]
                            width_ratio = self.m.get_width_mass_ratio()
                            mT = self.m.get_mT()
                            d = self.interpolate2d(indexes, None, width_ratio, mT, t, width_ratio_array, None)
                            return d
                        elif index in [22, 23, 28, 29]:
                            indexes = [22, 23, 28, 29]
                            width_ratio_array = [0.05, 0.1, 0.2, 0.3]
                            width_ratio = self.m.get_width_mass_ratio()
                            mT = self.m.get_mT()
                            d = self.interpolate2d(indexes, None, width_ratio, mT, t, width_ratio_array, None)
                            return d
                        elif index in [10, 11, 12, 13]:
                            indexes = [10, 11, 12, 13]
                            width_ratio_array = [0.05, 0.1, 0.2, 0.3]
                            width_ratio = self.m.get_width_mass_ratio()
                            mT = self.m.get_mT()
                            d = self.interpolate2d(indexes, None, width_ratio, mT, t, width_ratio_array, None)
                            return d
                        else:
                            expected_or_observed = interp1d(self.MT[index], t[index], 'linear')
                            d = expected_or_observed(self.m.get_mT())
                            return d
                    elif self.m.model() == 'Doublet':
                        if index in [26, 27, 28]:
                            indexes = [26, 27, 28]
                            coupling_arr = [0.3, 0.5, 0.7]
                            kappa = self.m.get_coupling_strength()
                            mT = self.m.get_mT()
                            d = self.interpolate2d(indexes, kappa, None, mT, t, None, coupling_arr)
                            return d
                        elif index in [23, 24, 25]:
                            indexes = [23, 24, 25]
                            coupling_arr = [0.2, 0.4, 0.6]
                            kappa = self.m.get_coupling_strength()
                            mT = self.m.get_mT()
                            d = self.interpolate2d(indexes, kappa, None, mT, t, None, coupling_arr)
                            return d
                        elif index in [9, 10, 15, 16]:
                            indexes = [9, 10, 15, 16]
                            width_ratio_arr = [0.05, 0.1, 0.2, 0.3]
                            width_ratio = self.m.get_width_mass_ratio()
                            mT = self.m.get_mT()
                            d = self.interpolate2d(indexes, None, width_ratio, mT, t, width_ratio_arr, None)
                            return d
                        elif index in [11, 12, 17, 18]:
                            indexes = [11, 12, 27, 18]
                            width_ratio_arr = [0.05, 0.1, 0.2, 0.3]
                            width_ratio = self.m.get_width_mass_ratio()
                            mT = self.m.get_mT()
                            d = self.interpolate2d(indexes, None, width_ratio, mT, t, width_ratio_arr, None)
                            return d
                        elif index in [13, 14, 19, 20]:
                            indexes = [13, 14, 19, 20]
                            width_ratio_arr = [0.05, 0.1, 0.2, 0.3]
                            width_ratio = self.m.get_width_mass_ratio()
                            mT = self.m.get_mT()
                            d = self.interpolate2d(indexes, None, width_ratio, mT, t, width_ratio_arr, None)
                            return d
                        else:
                            expected_or_observed = interp1d(self.MT[index], t[index], 'linear')
                            d = expected_or_observed(self.m.get_mT())
                            return d
                    else:
                        expected_or_observed = interp1d(self.MT[index], t[index], 'linear')
                        d = expected_or_observed(self.m.get_mT())
                        return d

                else:
                    d = -1
                    return d
            else:
                d = 1
                return d
        else:
            return -1

    def expected_ratio_calc(self):
        maxi = float('-inf')
        pos = -1
        for index, k in enumerate(self.key):
            n = self.numerator(index)
            d = self.denominator(n, index, self.exp)
            if d == -1 or n == -1:
                continue
            else:
                rat = n / d
                if rat >= maxi:
                    maxi = rat
                    pos = index
        self.exp_ratio = maxi
        return pos

    def check_channel(self):
        position = self.expected_ratio_calc()
        numerator = self.numerator(position)
        d = self.denominator(numerator, position, self.obs)
        observed_ratio = numerator / d
        self.obs_ratio = observed_ratio
        if self.obs_ratio >= 1:
            self.result = 0
            self.channel = position
        elif self.obs_ratio < 0:
            self.result = -1
            self.channel = position
        else:
            self.result = 1
            self.channel = position
