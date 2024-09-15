from scipy.interpolate import interp1d
from initialize import Tables
from output import Result
from vector_like_T import *
from params_constraints import *


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

    def get_pair_prod_channels(self, key: str):
        if key in self.cs_keys['pair_prod']:
            index = self.key.index(key)
            return index

    def process_condition(self, channel_key, condition_dict, parameter, model, condition_type):
        index = ''
        for condition, keys in condition_dict.items():
            values_from_condition, from_equal = which_equivalence(condition)
            if channel_key in self.cs_keys['single_prod']:
                if channel_key in condition_dict[condition][model]:
                    if len(values_from_condition) == 2:
                        min_value, max_value = values_from_condition
                        if min_value <= parameter <= max_value:
                            index = self.key.index(channel_key)

                    elif len(values_from_condition) == 1:
                        max_value = values_from_condition[0]
                        if from_equal:
                            if abs(parameter - max_value) <= c.Threshold:
                                index = self.key.index(channel_key)

                        else:
                            if parameter <= max_value:
                                index = self.key.index(channel_key)

            else:
                index = self.get_pair_prod_channels(channel_key)
        return index

    def get_channels_from_limit_condition(self, k, width_ratio, coupling, model):
        channel = self.process_condition(k, T_width_mass_ratio_keys, width_ratio, model, "width_to_mass_ratio")
        if channel != '':
            return channel
        channel = self.process_condition(k, T_kappa_keys, coupling, model, "coupling_strength")
        return channel

    def get_channel(self, k, r, kappa):
        if self.VLB:
            if self.m.model() == 'Singlet':
                channel = self.get_channels_from_limit_condition(k, r, kappa, self.m.model())
                return channel

            elif self.m.model() == 'Doublet':
                channel = self.get_channels_from_limit_condition(k, r, kappa, self.m.model())
                return channel

        elif self.VLX:
            channel = self.get_channels_from_limit_condition(k, r, kappa, self.m.model())
            return channel
        elif self.VLY:
            channel = self.get_channels_from_limit_condition(k, r, kappa, self.m.model())
            return channel
        else:
            if self.m.model() == 'Singlet':
                channel = self.get_channels_from_limit_condition(k, r, kappa, self.m.model())
                return channel

            elif self.m.model() == 'Doublet':
                channel = self.get_channels_from_limit_condition(k, r, kappa, self.m.model())
                return channel

            elif self.m.model() == 'Pure':
                return self.get_pair_prod_channels(k)
            else:
                raise Exception("Error in model name")

    def numerator(self, i):
        r, kappa = self.get_ratio_and_universal_coupling()
        if self.VLB:
            if self.m.model() == 'Singlet':
                j = self.get_channel(self.key[i], r, kappa)

                if j == 20:
                    return self.m.get_xs_pp_Bbq_tWbq(j)
                elif j == 21:
                    return self.m.get_xs_pp_Btq_tWtq(j)
                elif j in [15, 16, 17]:
                    return self.m.get_xs_pp_Bj_bHj_ts_channels(j)
                elif j in [4, 5, 6, 7]:
                    return self.m.get_xs_pp_Bbq_bHbq(j)
                elif j == 19:
                    return self.m.get_xs_pp_Bbq_bZbq(j)
                elif j == 18:
                    return self.m.get_xs_pp_Btq_bZtq(j)
                else:
                    return self.m.get_xs_pp_QQ()

            elif self.m.model() == 'Doublet':
                j = self.get_channel(self.key[i], r, kappa)
                if j == 20:
                    return self.m.get_xs_pp_Bbq_tWbq(j)
                elif j in [15, 16, 17]:
                    return self.m.get_xs_pp_Bj_bHj_ts_channels(j)
                elif j in [5, 6, 7, 8]:
                    return self.m.get_xs_pp_Bbq_bHbq(j)
                else:
                    return self.m.get_xs_pp_QQ()
            else:
                if self.process[i][:9] == 'pp --> BB':
                    return self.m.get_xs_pp_QQ()
        elif self.VLX:
            if self.process[i][:9] == 'pp --> XX':
                return self.m.get_xs_pp_QQ()
            else:
                return -1
        elif self.VLY:
            if self.process[i][:9] == 'pp --> YY':
                return self.m.get_xs_pp_QQ() 
            else:
                return -1
        else:
            if self.m.model() == 'Singlet':

                j = self.get_channel(self.key[i], r, kappa)

                if j in [32, 33, 34, 35, 43, 44, 45]:
                    return self.m.get_xs_pp_Tj_Ztj_ts_channels(j)

                elif j in [37, 38, 39, 40, 41, 42, 17, 46, 16, 18, 19, 24, 25]:
                    return self.m.get_xs_pp_Tbq_tHbq(j)

                elif j in [57, 31, 36, 14, 10, 11, 12, 13, 50, 51, 20, 21, 26, 27]:
                    return self.m.get_xs_pp_Tbq_tZbq(j)

                elif j in [58, 30]:
                    return self.m.get_xs_pp_Tbq_Wbbq(j)

                elif j == 15:
                    return self.m.get_xs_pp_Tbq(j)

                elif j in [52, 53, 22, 23, 28, 29]:
                    return self.m.get_xs_pp_Tbq_tZ_plus_TH(j)

                elif j in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 47, 48, 49, 54, 55, 56]:
                    return self.m.get_xs_pp_QQ()

                else:
                    return -1

            elif self.m.model() == 'Doublet':
                if self.m.get_which_doublet() == 'TB' or self.m.get_which_doublet() == 'XT':
                    j = self.get_channel(self.key[i], r, kappa)
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

    def denominator(self, num, index, t):
        print("num:" + str(num) + "index:" + str(index))
        if 0 <= num:
            if self.VLB:
                if min(self.MB[index]) <= self.m.get_mB() <= max(self.MB[index]):
                    def get_xs_from_relative_width_interpolation(tables_indexes):
                        t_indexes = tables_indexes
                        relative_width_values = [0.01, 0.1, 0.2, 0.3]
                        relative_width_value = self.m.get_width_mass_ratio()
                        mB = self.m.get_mB()
                        coupling_strength_arr = coupling_strength_value = None
                        expt_input = (t_indexes, self.MB, relative_width_values, coupling_strength_arr, t,
                                      mB, relative_width_value, coupling_strength_value)

                        expt_xs = interpolate2d(expt_input, theo_input=(None,), case='expt')
                        return expt_xs

                    def get_xs_from_coupling_strength_interpolation(tables_indexes):
                        t_indexes = tables_indexes
                        coupling_strength_arr = [0.3, 0.4, 0.5]
                        coupling_strength_value = self.m.get_coupling_strength()
                        mB = self.m.get_mB()
                        relative_width_values = relative_width_value = None
                        expt_input = (t_indexes, self.MB, relative_width_values, coupling_strength_arr, t,
                                      mB, relative_width_value, coupling_strength_value)
                        expt_xs = interpolate2d(expt_input, theo_input=(None,), case='expt')
                        return expt_xs

                    if self.m.model() == 'Singlet':
                        if index in [4, 5, 6, 7]:
                            return get_xs_from_relative_width_interpolation([4, 5, 6, 7])
                        elif index in [15, 16, 17]:
                            return get_xs_from_coupling_strength_interpolation([15, 16, 17])
                        else:
                            expected_or_observed = interp1d(self.MB[index], t[index], 'linear')
                            expt_xs = expected_or_observed(self.m.get_mB())
                            return expt_xs
                    elif self.m.model() == 'Doublet':
                        if index in [5, 6, 7, 8]:
                            return get_xs_from_relative_width_interpolation([5, 6, 7, 8])
                        elif index in [13, 14, 15]:
                            return get_xs_from_coupling_strength_interpolation([13, 14, 15])
                        else:
                            expected_or_observed = interp1d(self.MB[index], t[index], 'linear')
                            expt_xs = expected_or_observed(self.m.get_mB())
                            return expt_xs
                else:
                    return -1
            elif self.VLX:
                if min(self.MX[index]) <= self.m.get_mX() <= max(self.MX[index]):
                    expected_or_observed = interp1d(self.MX[index], t[index], 'linear')
                    d = expected_or_observed(self.m.get_mX())
                    return d
                else:
                    return -1
            elif self.VLY:
                if min(self.MY[index]) <= self.m.get_mY() <= max(self.MY[index]):
                    expected_or_observed = interp1d(self.MY[index], t[index], 'linear')
                    d = expected_or_observed(self.m.get_mY())
                    return d
                else:
                    return -1
            else:
                return self.get_expt_xs_from_2d_interpolation(index, t)
        else:
            d = 1
            return d

    def expected_ratio_calc(self):
        maxi = float('-inf')
        pos = -1
        for index, k in enumerate(self.key):
            n = self.numerator(index)
            d_obs = self.denominator(n, index, self.obs)
            print("denom:", d_obs, index)
            print("num:", n, index)
            if d_obs == -1 or n == -1:
                continue
            else:
                obs_rat = n / d_obs
                if obs_rat >= maxi:
                    maxi = obs_rat
                    pos = index
        return pos

    def check_channel(self):
        position = self.expected_ratio_calc()
        predicted_xs = self.numerator(position)
        observed_xs = self.denominator(predicted_xs, position, self.obs)
        expected_xs = self.denominator(predicted_xs, position, self.exp)
        if predicted_xs == -1 or observed_xs == -1:
            observed_ratio = float('-inf')
            expected_ratio = float('-inf')
        else:
            observed_ratio = predicted_xs / observed_xs
            expected_ratio = predicted_xs / expected_xs
        self.obs_ratio = observed_ratio
        self.exp_ratio = expected_ratio
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

    def get_expt_xs_from_2d_interpolation(self, index, expt_table):
        def interpolation_based_on_kappa_keys(desired_key):
            if '==' not in desired_key:
                t_indexes = [self.key.index(k) for k in T_kappa_keys[desired_key][self.m.model()]
                             if k in self.key]

                min_kappa, max_kappa = [float(st) for st in desired_key.split('<=') if st != 'k']
                coupling_strength_arr = np.linspace(min_kappa, max_kappa, len(t_indexes))
                print("coupling_array:", coupling_strength_arr)
                print("indexes:", t_indexes)
                coupling_strength_value = self.m.get_coupling_strength()
                mT = self.m.get_mT()
                relative_width_values = relative_width_value = None
                expt_input = (t_indexes, self.MT, relative_width_values, coupling_strength_arr,
                              expt_table, mT, relative_width_value, coupling_strength_value)
                expt_xsec = interpolate2d(expt_input, theo_input=(None,), case='expt')
                return expt_xsec
            else:
                expect_or_observ = interp1d(self.MT[index], expt_table[index], 'linear')
                expt_xsec = expect_or_observ(self.m.get_mT())
                return expt_xsec

        def interpolation_based_on_width_keys():
            relative_width_values = [0.05, 0.1, 0.2, 0.3]
            indexes = []
            t_indexes = []
            for k in T_width_mass_ratio_keys['0.05<=r<=0.3'][self.m.model()]:
                indexes.append(self.key.index(k))
                if len(indexes) % 3 == 0:
                    indexes.insert(0, indexes[0] - 1)
                    t_indexes = indexes.copy()
                    print("table_indexes:", t_indexes)
                    indexes.clear()
            print("Final table_indexes:", t_indexes)
            print("table", relative_width_values)
            relative_width_value = self.m.get_width_mass_ratio()
            mT = self.m.get_mT()
            coupling_strength_arr = coupling_strength_value = None
            expt_input = (t_indexes, self.MT, relative_width_values, coupling_strength_arr,
                          expt_table, mT, relative_width_value, coupling_strength_value)
            expt_xsec = interpolate2d(expt_input, theo_input=(None,), case='expt')
            return expt_xsec

        if min(self.MT[index]) <= self.m.get_mT() <= max(self.MT[index]):
            if self.m.model() == 'Singlet':
                for key1 in T_kappa_keys.keys():
                    if self.key[index] in T_kappa_keys[key1][self.m.model()]:
                        expt_xs = interpolation_based_on_kappa_keys(key1)
                        return expt_xs

                if self.key[index] in T_width_mass_ratio_keys['0.05<=r<=0.3'][self.m.model()]:
                    expt_xs = interpolation_based_on_width_keys()
                    return expt_xs
                else:
                    expected_or_observed = interp1d(self.MT[index], expt_table[index], 'linear')
                    expt_xs = expected_or_observed(self.m.get_mT())
                    return expt_xs

            elif self.m.model() == 'Doublet':
                for key1 in T_kappa_keys.keys():
                    if self.key[index] in T_kappa_keys[key1][self.m.model()]:
                        expt_xs = interpolation_based_on_kappa_keys(key1)
                        return expt_xs

                if self.key[index] in T_width_mass_ratio_keys['0.05<=r<=0.3'][self.m.model()]:
                    if self.key[index] in T_width_mass_ratio_keys['0.05<=r<=0.3'][self.m.model()]:
                        expt_xs = interpolation_based_on_width_keys()
                        return expt_xs

                else:
                    expected_or_observed = interp1d(self.MT[index], expt_table[index], 'linear')
                    expt_xs = expected_or_observed(self.m.get_mT())
                    return expt_xs
            else:
                expected_or_observed = interp1d(self.MT[index], expt_table[index], 'linear')
                expt_xs = expected_or_observed(self.m.get_mT())
                return expt_xs

        else:
            expt_xs = -1
            return expt_xs
