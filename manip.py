import numpy as np
from scipy.interpolate import interp1d, LinearNDInterpolator
from initialize import Tables
from output import Result
import constants as c
from Bmodel import *
from model import *


class TheoryCalc(Tables, Result):
    def __init__(self, m):
        Tables.__init__(self, m)
        Result.__init__(self)
        self.m = m

    def get_ratio_and_universal_coupling(self):
        if self.m.model() == 'Singlet' or self.m.model() == 'Doublet':
            r = self.m.get_width_mass_ratio()
            kappa = self.m.get_coupling_strength()
            return r, kappa
        else:
            return None, None

    def get_channel(self, k, r, pr, kappa):
        if self.VLB:
            if self.m.model() == 'Singlet':
                if k in self.cs_keys['pair_prod']:
                    if pr in self.process:
                        index = self.key.index(k)
                        return index
                    else:
                        raise Exception("pair productions are not calculated")
                elif k in self.cs_keys['single_prod']:
                    if kappa is not None:
                        if k in c.B_kappa_keys['0.3<=k<=0.5']["Singlet"]:
                            if 0.3 <= kappa <= 0.5:
                                index = self.key.index(k)
                                return index
                            else:
                                return ''
                    else:
                        raise Exception("Error. Coupling strength is None")
                    if r is not None:
                        if k in c.T_width_mass_ratio_keys['r<=0.1']["Singlet"]:
                            if r <= 0.1:
                                index = self.key.index(k)
                                return index
                            else:
                                return ''
                    else:
                        raise Exception("Error. Width-to-mass ratio is None")
            elif self.m.model() == 'Doublet':
                if k in self.cs_keys['pair_prod']:
                    if pr in self.process:
                        index = self.key.index(k)
                        return index
                    else:
                        raise Exception("pair productions are not calculated")
                elif k in self.cs_keys['single_prod']:
                    if kappa is not None:
                        if k in c.B_kappa_keys['0.3<=k<=0.5']["Singlet"]:
                            if 0.3 <= kappa <= 0.5:
                                index = self.key.index(k)
                                return index
                            else:
                                return ''
                    else:
                        raise Exception("Error. Coupling strength is None")
                    if r is not None:
                        if k in c.T_width_mass_ratio_keys['r<=0.1']["Singlet"]:
                            if r <= 0.1:
                                index = self.key.index(k)
                                return index
                            else:
                                return ''
                    else:
                        raise Exception("Error. Width-to-mass ratio is None")

        else:
            if self.m.model() == 'Singlet':
                if k in self.cs_keys['pair_prod']:
                    if pr in self.process:
                        index = self.key.index(k)
                        return index
                    else:
                        raise Exception("pair productions are not calculated")

                elif k in self.cs_keys['single_prod']:
                    if kappa is not None:
                        if k in c.T_kappa_keys['0.1<=k<=1.1']["Singlet"]:
                            if 0.1 <= kappa <= 1.1:
                                index = self.key.index(k)
                                return index
                            else:
                                return ''
                        elif k in c.T_kappa_keys['0.2<=k<=0.6']["Singlet"]:
                            if 0.2 <= kappa <= 0.6:
                                index = self.key.index(k)
                                return index
                            else:
                                return ''
                        elif k in c.T_kappa_keys['0.3<=k<=0.7']["Singlet"]:
                            if 0.3 <= kappa <= 0.7:
                                index = self.key.index(k)
                                return index
                            else:
                                return ''
                        elif k in c.T_kappa_keys['k==0.5']["Singlet"]:
                            if abs(kappa - 0.5) <= c.Threshold:
                                index = self.key.index(k)
                                return index
                            else:
                                return ''
                    else:
                        raise Exception("Error. Coupling strength is None")
                    if r is not None:
                        if k in c.T_width_mass_ratio_keys['r==0.01']["Singlet"]:
                            if abs(r - 0.01) <= c.Threshold:
                                index = self.key.index(k)
                                return index
                            else:
                                return ''
                        elif k in c.T_width_mass_ratio_keys['r<=0.05']["Singlet"]:
                            if r <= 0.05:
                                index = self.key.index(k)
                                return index
                            else:
                                return ''
                        elif k in c.T_width_mass_ratio_keys['r<=0.1']["Singlet"]:
                            if r <= 0.1:
                                index = self.key.index(k)
                                return index
                            else:
                                return ''
                        elif k in c.T_width_mass_ratio_keys['0.05<r<=0.3']["Singlet"]:
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
        if self.VLB:
            if self.m.model() == 'Singlet':
                j = self.get_channel(self.key[i], r, self.process[i], kappa)
                if j == 21:
                    return self.m.get_xs_pp_Bbq_tWbq(j) / 1000
                elif j == 22:
                    return self.m.get_xs_pp_Btq_tWtq(j) / 1000
                elif j in [15, 16, 17]:
                    return self.m.get_xs_pp_Bj_bHj_ts_channels(j) / 1000
                elif j in [4, 5, 6, 7]:
                    return self.m.get_xs_pp_Bbq_bHbq(j) / 1000
                elif j == 19:
                    return self.m.get_xs_pp_Bbq_bZbq(j) / 1000
                elif j == 18:
                    return self.m.get_xs_pp_Btq_bZtq(j) / 1000
                else:
                    return self.m.get_xs_pp_QQ() / 1000
            else:
                j = self.get_channel(self.key[i], r, self.process[i], kappa)
                if j == 20:
                    return self.m.get_xs_pp_Bbq_tWbq(j) / 1000
                elif j == 21:
                    return self.m.get_xs_pp_Btq_tWtq(j) / 1000
                elif j in [15, 16, 17]:
                    return self.m.get_xs_pp_Bj_bHj_ts_channels(j) / 1000
                elif j in [5, 6, 7, 8]:
                    return self.m.get_xs_pp_Bbq_bHbq(j) / 1000
                else:
                    return self.m.get_xs_pp_QQ() / 1000
        else:
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

    def denominator(self, num, index, t):
        if self.process[index][:9] == 'pp --> Bb' or self.process[index][:9] == 'pp --> Bt':
        #if index in [10, 11, 12, 13]:
            if 0 <= num:
                if self.VLB:
                    if min(self.MB[index]) <= self.m.get_mB() <= max(self.MB[index]):
                        if self.m.model() == 'Singlet':
                            if index in [4, 5, 6, 7]:
                                indexes = [4, 5, 6, 7]
                                width_ratio_array = [0.01, 0.1, 0.2, 0.3]
                                width_ratio = self.m.get_width_mass_ratio()
                                mB = self.m.get_mB()
                                d = interpolate2d(indexes, None, width_ratio, self.MB, mB, t, width_ratio_array, None)
                                return d
                            elif index in [15, 16, 17]:
                                indexes = [15, 16, 17]
                                coupling_array = [0.3, 0.4, 0.5]
                                kappa = self.m.get_coupling_strength()
                                mB = self.m.get_mB()
                                d = interpolate2d(indexes, kappa, None, self.MB, mB, t, None, coupling_array)
                                return d
                            else:
                                expected_or_observed = interp1d(self.MB[index], t[index], 'linear')
                                d = expected_or_observed(self.m.get_mB())
                                return d
                        elif self.m.model() == 'Doublet':
                            if index in [5, 6, 7, 8]:
                                indexes = [5, 6, 7, 8]
                                width_ratio_array = [0.01, 0.1, 0.2, 0.3]
                                width_ratio = self.m.get_width_mass_ratio()
                                mB = self.m.get_mB()
                                d = interpolate2d(indexes, None, width_ratio, self.MB, mB, t, width_ratio_array, None)
                                return d
                            elif index in [15, 16, 17]:
                                indexes = [15, 16, 17]
                                coupling_array = [0.3, 0.4, 0.5]
                                kappa = self.m.get_coupling_strength()
                                mB = self.m.get_mB()
                                d = interpolate2d(indexes, kappa, None, self.MB, mB, t, None, coupling_array)
                                return d
                            else:
                                expected_or_observed = interp1d(self.MB[index], t[index], 'linear')
                                d = expected_or_observed(self.m.get_mB())
                                return d
                    else:
                        return -1
                else:
                    if min(self.MT[index]) <= self.m.get_mT() <= max(self.MT[index]):
                        if self.m.model() == 'Singlet':
                            if index in [37, 38, 39, 40, 41, 42]:
                                indexes = [37, 38, 39, 40, 41, 42]
                                coupling_array = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1]
                                kappa = self.m.get_coupling_strength()
                                mT = self.m.get_mT()
                                d = interpolate2d(indexes, kappa, None, self.MT, mT, t, None, coupling_array)
                                return d
                            elif index in [43, 44, 45]:
                                indexes = [43, 44, 45]
                                coupling_array = [0.3, 0.5, 0.7]
                                kappa = self.m.get_coupling_strength()
                                mT = self.m.get_mT()
                                d = interpolate2d(indexes, kappa, None, self.MT, mT, t, None, coupling_array)
                                return d
                            elif index in [32, 33, 34]:
                                indexes = [32, 33, 34]
                                coupling_array = [0.2, 0.4, 0.6]
                                kappa = self.m.get_coupling_strength()
                                mT = self.m.get_mT()
                                d = interpolate2d(indexes, kappa, None, self.MT, mT, t, None, coupling_array)
                                return d
                            elif index in [18, 19, 24, 25]:
                                indexes = [18, 19, 24, 25]
                                width_ratio_array = [0.05, 0.1, 0.2, 0.3]
                                width_ratio = self.m.get_width_mass_ratio()
                                mT = self.m.get_mT()
                                d = interpolate2d(indexes, None, width_ratio, self.MT, mT, t, width_ratio_array, None)
                                return d
                            elif index in [20, 21, 26, 27]:
                                indexes = [20, 21, 26, 27]
                                width_ratio_array = [0.05, 0.1, 0.2, 0.3]
                                width_ratio = self.m.get_width_mass_ratio()
                                mT = self.m.get_mT()
                                d = interpolate2d(indexes, None, width_ratio, self.MT, mT, t, width_ratio_array, None)
                                return d
                            elif index in [22, 23, 28, 29]:
                                indexes = [22, 23, 28, 29]
                                width_ratio_array = [0.05, 0.1, 0.2, 0.3]
                                width_ratio = self.m.get_width_mass_ratio()
                                mT = self.m.get_mT()
                                d = interpolate2d(indexes, None, width_ratio, self.MT, mT, t, width_ratio_array, None)
                                return d
                            elif index in [10, 11, 12, 13]:
                                indexes = [10, 11, 12, 13]
                                width_ratio_array = [0.05, 0.1, 0.2, 0.3]
                                width_ratio = self.m.get_width_mass_ratio()
                                mT = self.m.get_mT()
                                d = interpolate2d(indexes, None, width_ratio, self.MT, mT, t, width_ratio_array, None)
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
                                d = interpolate2d(indexes, kappa, None, self.MT, mT, t, None, coupling_arr)
                                return d
                            elif index in [23, 24, 25]:
                                indexes = [23, 24, 25]
                                coupling_arr = [0.2, 0.4, 0.6]
                                kappa = self.m.get_coupling_strength()
                                mT = self.m.get_mT()
                                d = interpolate2d(indexes, kappa, None, self.MT, mT, t, None, coupling_arr)
                                return d
                            elif index in [9, 10, 15, 16]:
                                indexes = [9, 10, 15, 16]
                                width_ratio_arr = [0.05, 0.1, 0.2, 0.3]
                                width_ratio = self.m.get_width_mass_ratio()
                                mT = self.m.get_mT()
                                d = interpolate2d(indexes, None, width_ratio, mT, t, width_ratio_arr, None)
                                return d
                            elif index in [11, 12, 17, 18]:
                                indexes = [11, 12, 27, 18]
                                width_ratio_arr = [0.05, 0.1, 0.2, 0.3]
                                width_ratio = self.m.get_width_mass_ratio()
                                mT = self.m.get_mT()
                                d = interpolate2d(indexes, None, width_ratio, self.MT, mT, t, width_ratio_arr, None)
                                return d
                            elif index in [13, 14, 19, 20]:
                                indexes = [13, 14, 19, 20]
                                width_ratio_arr = [0.05, 0.1, 0.2, 0.3]
                                width_ratio = self.m.get_width_mass_ratio()
                                mT = self.m.get_mT()
                                d = interpolate2d(indexes, None, width_ratio, mT, self.MT, t, width_ratio_arr, None)
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
            d = self.denominator(n, index, self.obs)
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
        print("xs result:", self.result, self.obs_ratio, self.exp_ratio, self.channel)
        return self.result, self.obs_ratio, self.exp_ratio, self.channel

