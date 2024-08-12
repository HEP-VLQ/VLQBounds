from model import *
from Bmodel import *
from manip import TheoryCalc
from initialize import Tables
from scipy.interpolate import interp1d


class Coupling(TheoryCalc):
    def __init__(self, m):
        super().__init__(m)
        if isinstance(m, Singlet) or isinstance(m, Doublet) or isinstance(m, SingletB) or isinstance(m, DoubletB):
            self.m = m
        else:
            raise Exception('Invalid model. Must be a singlet or Doublet')
        self.sin_l_keys = []
        self.sin_r_keys = []
        self.k_keys = []
        self.width_keys = []
        self.mass_ratio = None
        self.initialize_coupling_data()

    def initialize_coupling_lists(self, number_of_atlas_cms_tables):
        self.coupling_file_name = [None] * number_of_atlas_cms_tables
        self.coupling_key = [None] * number_of_atlas_cms_tables
        self.coupling_label = [None] * number_of_atlas_cms_tables
        self.coupling_expt = [None] * number_of_atlas_cms_tables
        self.coupling_MT_obs = [None] * number_of_atlas_cms_tables
        self.coupling_MT_exp = [None] * number_of_atlas_cms_tables
        self.coupling_MB_obs = [None] * number_of_atlas_cms_tables
        self.coupling_MB_exp = [None] * number_of_atlas_cms_tables
        self.coupling_obs_upper = [None] * number_of_atlas_cms_tables
        self.coupling_exp_upper = [None] * number_of_atlas_cms_tables
        self.coupling_obs_lower = [None] * number_of_atlas_cms_tables
        self.coupling_exp_lower = [None] * number_of_atlas_cms_tables
        self.coupling_process = [None] * number_of_atlas_cms_tables
        self.which_coupling = [None] * number_of_atlas_cms_tables
        self.coupling_energy = [None] * number_of_atlas_cms_tables
        self.coupling_luminosity = [None] * number_of_atlas_cms_tables

    def get_number_of_tables(self, vlq='T'):
        if vlq == 'B':
            if self.m.model() == 'Singlet':
                return 6
            elif self.m.model() == 'Doublet':
                return 2
            else:
                print(f"Warning. There is no coupling limits for this model {self.m.model()}")
                return 0
        else:
            if self.m.model() == 'Singlet':
                return 13
            elif self.m.model() == 'Doublet':
                return 3
            else:
                print(f"Warning. There is no coupling limits for this model {self.m.model()}")
                return 0

    def initialize_coupling_data(self):
        if isinstance(self.m, SingletB) or isinstance(self.m, DoubletB):
            number_of_atlas_cms_tables = self.get_number_of_tables(vlq='B')
            if number_of_atlas_cms_tables > 0:
                self.initialize_coupling_lists(number_of_atlas_cms_tables)
        else:
            number_of_atlas_cms_tables = self.get_number_of_tables()
            if number_of_atlas_cms_tables > 0:
                self.initialize_coupling_lists(number_of_atlas_cms_tables)

    def fill_coupling_tables(self):
        if self.VLB:
            if self.m.model() == 'Singlet':
                self.coupling_key[0] = '02595f9a'
                self.coupling_label[0] = 'arXiv:2308.02595'
                self.coupling_expt[0] = 'ATLAS'
                self.coupling_file_name[0] = '2308.02595_ATLAS_Fig9a_pp_B_bH_k_singlet.dat'
                self.coupling_process[0] = 'pp --> Bbq --> bHbq --> b,bb,bq'
                self.which_coupling[0] = "k_B"
                self.coupling_energy[0] = 13
                self.coupling_luminosity[0] = 139

                self.coupling_key[1] = '01486f43'
                self.coupling_label[1] = 'arXiv:1802.01486'
                self.coupling_expt[1] = 'CMS'
                self.coupling_file_name[1] = '2405.17605_Fig43_upper_pp_B_bH_singlet_1802.01486_cf.dat'
                self.coupling_process[1] = 'pp --> Bq --> bHq --> b,bb,bq'
                self.which_coupling[1] = "s_l"
                self.coupling_energy[1] = 13
                self.coupling_luminosity[1] = 35.9

                self.coupling_key[2] = '01486f43'
                self.coupling_label[2] = 'arXiv:1809.08597'
                self.coupling_expt[2] = 'CMS'
                self.coupling_file_name[2] = '2405.17605_Fig43_upper_pp_Bbq_tW_singlet_1809.08597_cf.dat'
                self.coupling_process[2] = 'pp --> Bbq --> tWbq --> bqq,lnu/blnu,bq'
                self.which_coupling[2] = "s_l"
                self.coupling_energy[2] = 13
                self.coupling_luminosity[2] = 35.9

                self.coupling_key[3] = '10216f43'
                self.coupling_label[3] = 'arXiv:2111.10216'
                self.coupling_expt[3] = 'CMS'
                self.coupling_file_name[3] = '2405.17605_Fig43_upper_pp_Bbq_tW_singlet_2111.10216_cf.dat'
                self.coupling_process[3] = 'pp --> Bbq --> tWbq'
                self.which_coupling[3] = "s_l"
                self.coupling_energy[3] = 13
                self.coupling_luminosity[3] = 138

                self.coupling_key[4] = '01486f43'
                self.coupling_label[4] = 'arXiv:1809.08597'
                self.coupling_expt[4] = 'CMS'
                self.coupling_file_name[4] = '2405.17605_Fig43_upper_pp_Btq_tW_singlet_1809.08597_cf.dat'
                self.coupling_process[4] = 'pp --> Bbq --> tW'
                self.which_coupling[4] = "s_l"
                self.coupling_energy[4] = 13
                self.coupling_luminosity[4] = 35.9

                self.coupling_key[5] = '10216f43t'
                self.coupling_label[5] = 'arXiv:2111.10216'
                self.coupling_expt[5] = 'CMS'
                self.coupling_file_name[5] = '2405.17605_Fig43_upper_pp_Btq_tW_singlet_2111.10216_cf.dat'
                self.coupling_process[5] = 'pp --> Bbq --> tWbq'
                self.which_coupling[5] = "s_l"
                self.coupling_energy[5] = 13
                self.coupling_luminosity[5] = 138

                expected = [self.coupling_exp_upper, self.coupling_exp_lower]
                observed = [self.coupling_obs_lower, self.coupling_obs_upper]
                mass = [self.coupling_MB_obs, self.coupling_MB_exp]
                coupling_data_loading(self.coupling_file_name, len(self.coupling_key), mass, expected,
                                      observed, self.coupling_expt, self.m.model(), vlq='B')

            else:
                self.coupling_key[0] = '02595f9b'
                self.coupling_label[0] = 'arXiv:2308.02595'
                self.coupling_expt[0] = 'ATLAS'
                self.coupling_file_name[0] = '2308.02595_ATLAS_Fig9b_pp_B_bH_k_doublet.dat'
                self.coupling_process[0] = 'pp --> Bbq --> bHbq'
                self.which_coupling[0] = "k_B"
                self.coupling_energy[0] = 13
                self.coupling_luminosity[0] = 139

                self.coupling_key[1] = '01486f43l'
                self.coupling_label[1] = 'arXiv:1802.01486'
                self.coupling_expt[1] = 'CMS'
                self.coupling_file_name[1] = '2405.17605_Fig43_lower_pp_B_bH_doublet_1802.01486_cf.dat'
                self.coupling_process[1] = 'pp --> Bbq --> bHbq'
                self.which_coupling[1] = "k_B"
                self.coupling_energy[1] = 13
                self.coupling_luminosity[1] = 35.9

                expected = [self.coupling_exp_upper, self.coupling_exp_lower]
                observed = [self.coupling_obs_lower, self.coupling_obs_upper]
                mass = [self.coupling_MB_obs, self.coupling_MB_exp]
                coupling_data_loading(self.coupling_file_name, len(self.coupling_key), mass, expected,
                                      observed, self.coupling_expt, self.m.model(), vlq='B')
        else:
            if self.m.model() == 'Singlet':
                self.coupling_key[0] = '05606f7b'
                self.coupling_label[0] = 'arXiv:1602.05606'
                self.coupling_expt[0] = 'ATLAS'
                self.coupling_file_name[0] = '1602.05606_ATLAS_f7b_pp_Tbj_Wbbj_s_L_Singlet.dat'
                self.coupling_process[0] = 'pp --> Tbq --> Wbbq'
                self.which_coupling[0] = "|sin_left|"
                self.coupling_energy[0] = 8
                self.coupling_luminosity[0] = 20.3

                self.coupling_key[1] = '07343f8as_L'
                self.coupling_label[1] = 'arXiv:1812.07343'
                self.coupling_expt[1] = 'ATLAS'
                self.coupling_file_name[1] = '1812.07343_ATLAS_f8a_pp_Tbq_wbbq_Singlet_s_L.dat'
                self.which_coupling[1] = "|sin_left|"
                self.coupling_process[1] = 'pp --> Tbq --> Wbbq'
                self.coupling_energy[1] = 13
                self.coupling_luminosity[1] = 36.1

                self.coupling_key[2] = '09743f6b_s_L'
                self.coupling_label[2] = 'arXiv:1812.09743'
                self.coupling_expt[2] = 'ATLAS'
                self.coupling_file_name[2] = '1812.09743_ATLAS_f6b_pp_Tbq_tZbq_s_L_Singlet.dat'
                self.which_coupling[2] = "|sin_left|"
                self.coupling_process[2] = 'pp --> Tbq --> tZbq'
                self.coupling_energy[2] = 13
                self.coupling_luminosity[2] = 36.1

                self.coupling_key[3] = '10555f16b_s_L'
                self.coupling_label[3] = 'arXiv:1806.10555'
                self.coupling_expt[3] = 'ATLAS'
                self.coupling_file_name[3] = '1806.10555_ATLAS_f16b_pp_Tbq_Zt_s_L_Singlet.dat'
                self.coupling_process[3] = 'pp --> Tbq --> tZbq'
                self.which_coupling[3] = "|sin_left|"
                self.coupling_energy[3] = 13
                self.coupling_luminosity[3] = 36.1

                self.coupling_key[4] = '072f10b'
                self.coupling_label[4] = 'arXiv:ATLAS-CONF-2016-072'
                self.coupling_expt[4] = 'ATLAS'
                self.coupling_file_name[4] = 'ATLAS-CONF-2016-072_ATLAS_f10a_pp_Tqb_Wb_singlet_s_L.dat'
                self.which_coupling[4] = "|sin_left|"
                self.coupling_process[4] = 'pp --> Tbq --> Wbbq'
                self.coupling_energy[4] = 13
                self.coupling_luminosity[4] = 36.1

                self.coupling_key[5] = '12802f5'
                self.coupling_label[5] = 'arXiv:2302.12802'
                self.coupling_expt[5] = 'CMS'
                self.coupling_file_name[5] = '2302.12802_CMS_Fig5_pp_Tbq_tH_k.dat'
                self.which_coupling[5] = "|sin_left|"
                self.coupling_process[5] = 'pp --> Tbq --> tHbq'
                self.coupling_energy[5] = 13
                self.coupling_luminosity[5] = 36.1

                self.coupling_key[6] = '16561f12a_k_T'
                self.coupling_label[6] = 'arXiv:2402.16561'
                self.coupling_expt[6] = 'ATLAS'
                self.coupling_file_name[6] = '2402.16561_ATLAS_Fig12a_pp_T_Ht_Zt_k_T_singlet.dat'
                self.which_coupling[6] = 'kappa'
                self.coupling_process[6] = 'pp --> Tbq --> tZbq'
                self.coupling_energy[6] = 13
                self.coupling_luminosity[6] = 139

                self.coupling_key[7] = '07045f9_k_T'
                self.coupling_label[7] = 'arXiv:2201.07045'
                self.coupling_expt[7] = 'ATLAS'
                self.coupling_file_name[7] = '2201.07045_ATLAS_f9_pp_Tbq_Htbq_k_T_singlet.dat'
                self.which_coupling[7] = 'kappa'
                self.coupling_process[7] = 'pp --> Tbq --> tHbq'
                self.coupling_energy[7] = 13
                self.coupling_luminosity[7] = 139

                self.coupling_key[8] = '03401f13a'
                self.coupling_label[8] = 'arXiv:2305.03401'
                self.coupling_expt[8] = 'ATLAS'
                self.coupling_file_name[8] = '2305.03401_ATLAS_f13a_pp_Tbq_Ztbq_singlet_k_T.dat'
                self.which_coupling[8] = 'kappa'
                self.coupling_process[8] = 'pp --> Tbq --> tZ(H)bq'
                self.coupling_energy[8] = 13
                self.coupling_luminosity[8] = 139

                self.coupling_key[9] = '07584f9a'
                self.coupling_label[9] = 'arXiv:2307.07584'
                self.coupling_expt[9] = 'ATLAS'
                self.which_coupling[9] = 'kappa'
                self.coupling_process[9] = 'pp --> Tbq --> tZbq'
                self.coupling_file_name[9] = '2307.07584_ATLAS_f9a_pp_Tbq_Ztbq_k_T_singlet.dat'
                self.coupling_energy[9] = 13
                self.coupling_luminosity[9] = 139

                self.coupling_key[10] = '17605f36'
                self.coupling_label[10] = 'arXiv:2405.17605'
                self.coupling_expt[10] = 'CMS'
                self.which_coupling[10] = 'width_mass_ratio'
                self.coupling_process[10] = 'pp --> Tbq'
                self.coupling_file_name[10] = '2405.17605_fig36_gamma_mT_singlet.dat'
                self.coupling_energy[10] = 13
                self.coupling_luminosity[10] = 138

                self.coupling_key[11] = '01062f6'
                self.coupling_label[11] = 'arXiv:1708.01062'
                self.coupling_expt[11] = 'CMS'
                self.which_coupling[11] = 'width_mass_ratio'
                self.coupling_process[11] = 'pp --> Tbq'
                self.coupling_file_name[11] = '1708.01062_CMS_Fig6_pp_T_tZ_gamma_mT_singlet.dat'
                self.coupling_energy[11] = 13
                self.coupling_luminosity[11] = 35.9

                self.coupling_key[12] = '02227f9'
                self.coupling_label[12] = 'arXiv:2201.02227'
                self.coupling_expt[12] = 'CMS'
                self.which_coupling[12] = 'width_mass_ratio'
                self.coupling_process[12] = 'pp --> Tbq --> tZbq'
                self.coupling_file_name[12] = '2201.02227_CMS_fig9_pp_T_tZ_singlet_gamma_mT.dat'
                self.coupling_energy[12] = 13
                self.coupling_luminosity[12] = 137

                expected = [self.coupling_exp_upper, self.coupling_exp_lower]
                observed = [self.coupling_obs_lower, self.coupling_obs_upper]
                mass = [self.coupling_MT_obs, self.coupling_MT_exp]

                coupling_data_loading(self.coupling_file_name, len(self.coupling_key), mass, expected,
                                      observed, self.coupling_expt, self.m.model())

            elif self.m.model() == 'Doublet':
                self.coupling_key[0] = '03401f13b'
                self.coupling_label[0] = 'arXiv:2305.03401'
                self.coupling_expt[0] = 'ATLAS'
                self.coupling_file_name[0] = '2305.03401_ATLAS_f13b_pp_Tbq_Ztbq_k_T_doublet.dat'
                self.which_coupling[0] = 'kappa'
                self.coupling_process[0] = 'pp --> Tbq --> tZbq'
                self.coupling_energy[0] = 13
                self.coupling_luminosity[0] = 139

                self.coupling_key[1] = '07584f9b'
                self.coupling_label[1] = 'arXiv:2307.07584'
                self.coupling_expt[1] = 'ATLAS'
                self.coupling_file_name[1] = '2307.07584_ATLAS_f9b_pp_Tbq_Ztbq_k_T_doublet.dat'
                self.which_coupling[1] = 'kappa'
                self.coupling_process[1] = 'pp --> Tbq --> tZbq'
                self.coupling_energy[1] = 13
                self.coupling_luminosity[1] = 139

                self.coupling_key[2] = '01062f6'
                self.coupling_label[2] = 'arXiv:1708.01062'
                self.coupling_expt[2] = 'CMS'
                self.which_coupling[2] = 'width_mass_ratio'
                self.coupling_process[2] = 'pp --> Tbq'
                self.coupling_file_name[2] = '1708.01062_CMS_Fig6_pp_T_tZ_gamma_mT_doublet.dat'
                self.coupling_energy[2] = 13
                self.coupling_luminosity[2] = 35.9

                expected = [self.coupling_exp_upper, self.coupling_exp_lower]
                observed = [self.coupling_obs_lower, self.coupling_obs_upper]
                mass = [self.coupling_MT_obs, self.coupling_MT_exp]

                coupling_data_loading(self.coupling_file_name, len(self.coupling_key), mass, expected,
                                      observed, self.coupling_expt, self.m.model())

    def model_coupling_calc(self, i):
        if self.VLB:
            if i != -1:
                if self.m.model() == 'Singlet':
                    if self.key[i] in self.k_keys:
                        return self.m.get_coupling_strength()
                    elif self.key[i] in self.sin_l_keys:
                        return self.m.get_sin_left()
                    else:
                        raise Exception("Something went wrong in filling coupling tables")
                elif self.m.model() == 'Doublet':
                    if self.key[i] in self.k_keys:
                        return self.m.get_coupling_strength()
                    else:
                        raise Exception("Something went wrong in filling coupling tables")
                else:
                    raise Exception(f"There are no coupling limits for the model {self.m.model}")
            else:
                return -1
        else:
            if self.m.model() == 'Singlet':
                if self.key[i] in self.sin_l_keys:
                    return self.m.get_sin_left()
                elif self.key[i] in self.k_keys:
                    return self.m.get_coupling_strength()
                elif self.key[i] in self.k_keys:
                    if self.which_coupling[i] == "|Tth_coupling|":
                        return self.m.get_sin_left()
                elif self.key[i] in self.width_keys:
                    if self.which_coupling[i] == "width_mass_ratio":
                        return self.m.get_width_mass_ratio()
                else:
                    raise Exception("Something went wrong in filling coupling tables")
            elif self.m.model() == 'Doublet':
                if self.key[i] in self.k_keys:
                    return self.m.get_coupling_strength()
                elif self.key[i] in self.width_keys:
                    if self.which_coupling[i] == "width_mass_ratio":
                        return self.m.get_width_mass_ratio()
                else:
                    raise Exception("Something went wrong in filling coupling tables")
            else:
                raise Exception(f"There are no coupling limits for the model {self.m.model}")

    def get_limit_from_data(self, num, index, t, mass):
        if self.coupling_process[index][:9] == 'pp --> Bb' or self.coupling_process[index][:9] == 'pp --> Bt':
            if 0 <= num:
                if self.VLB:
                    if self.m.model() == 'Singlet':
                        if min(mass[index]) <= self.m.get_mB() <= max(mass[index]):
                            expected_or_observed = interp1d(mass[index], t[index], 'linear')
                            exp_or_obs = expected_or_observed(self.m.get_mB())
                            return exp_or_obs
                        else:
                            d = -1
                            return d
                    elif self.m.model() == 'Doublet':
                        if min(mass[index]) <= self.m.get_mB() <= max(mass[index]):
                            expected_or_observed = interp1d(mass[index], t[index], 'linear')
                            exp_or_obs = expected_or_observed(self.m.get_mB())
                            return exp_or_obs
                        else:
                            d = -1
                            return d
                else:
                    if self.m.model() == 'Singlet':
                        if index in range(0, 10):
                            if min(mass[index]) <= self.m.get_mT() <= max(mass[index]):
                                expected_or_observed = interp1d(mass[index], t[index], 'linear')
                                exp_or_obs = expected_or_observed(self.m.get_mT())
                                return exp_or_obs
                            else:
                                d = -1
                                return d
                        else:
                            max_mass, min_mass = max_min_mass_from_width_files(mass, [10, 11, 12])
                            if min_mass > self.m.get_mT() or max_mass < self.m.get_mT():
                                if min(t[index] / 100) <= self.m.get_width_mass_ratio() <= max(t[index] / 100):
                                    expected_or_observed = interp1d(t[index] / 100, mass[index], 'linear')
                                    mass_interp = expected_or_observed(self.m.get_width_mass_ratio())
                                    self.mass_ratio = mass_interp / self.m.get_mT()
                                    d = self.m.get_width_mass_ratio()
                                    return d, mass_interp
                                else:
                                    d, mass_interp = -1, -1
                                    return d, mass_interp
                            elif min_mass <= self.m.get_mT() <= max_mass:
                                if min(t[index] / 100) <= self.m.get_width_mass_ratio() <= max(t[index] / 100):
                                    expected_or_observed = interp1d(t[index] / 100, mass[index], 'linear')
                                    mass_interp = expected_or_observed(self.m.get_width_mass_ratio())
                                    self.mass_ratio = mass_interp / self.m.get_mT()
                                    d = self.m.get_width_mass_ratio()
                                    return d, mass_interp
                                else:
                                    d, mass_interp = -1, -1
                                    return d, mass_interp
                            else:
                                d, mass_interp = -1, -1
                                return d, mass_interp
                    else:
                        if index in range(0, 2):
                            if min(mass[index]) <= self.m.get_mT() <= max(mass[index]):
                                expected_or_observed = interp1d(mass[index], t[index], 'linear')
                                exp_or_obs = expected_or_observed(self.m.get_mT())
                                return exp_or_obs
                            else:
                                d = -1
                                return d
                        else:
                            max_mass, min_mass = max_min_mass_from_width_files(mass, [2])
                            if min_mass > self.m.get_mT() or max_mass < self.m.get_mT():
                                if min(t[index] / 100) <= self.m.get_width_mass_ratio() <= max(t[index] / 100):
                                    expected_or_observed = interp1d(t[index] / 100, mass[index], 'linear')
                                    mass_interp = expected_or_observed(self.m.get_width_mass_ratio())
                                    self.mass_ratio = mass_interp / self.m.get_mT()
                                    d = self.m.get_width_mass_ratio()
                                    return d, mass_interp
                                else:
                                    d, mass_interp = -1, -1
                                    return d, mass_interp
                            elif min_mass <= self.m.get_mT() <= max_mass:
                                if min(t[index] / 100) <= self.m.get_width_mass_ratio() <= max(t[index] / 100):
                                    expected_or_observed = interp1d(t[index] / 100, mass[index], 'linear')
                                    mass_interp = expected_or_observed(self.m.get_width_mass_ratio())
                                    self.mass_ratio = mass_interp / self.m.get_mT()
                                    d = self.m.get_width_mass_ratio()
                                    return d, mass_interp
                                else:
                                    d = (-1, -1)
                                    return d
                            else:
                                d, mass_interp = -1, -1
                                return d, mass_interp
            else:
                d = -1
                return d
        else:
            d = -1
            return d

    def identify_strong_limit(self, exp_or_obs, mass):
        maxi = float('-inf')
        pos = -1
        if self.VLB:
            for index, k in enumerate(self.coupling_key):
                n = self.model_coupling_calc(index)
                d = self.get_limit_from_data(n, index, exp_or_obs, mass)
                if d == -1 or n == -1:
                    continue
                else:
                    rat = n / d
                    if rat > maxi:
                        maxi = rat
                        pos = index
            return pos
        else:
            for index, k in enumerate(self.coupling_key):
                if index in range(0, len(self.coupling_key) - len(self.width_keys)):
                    n = self.model_coupling_calc(index)
                    d = self.get_limit_from_data(n, index, exp_or_obs, mass)
                    if d == -1 or n == -1:
                        continue
                    else:
                        rat = n / d
                        if rat > maxi:
                            maxi = rat
                            pos = index
                else:
                    n = self.model_coupling_calc(index)
                    d, _ = self.get_limit_from_data(n, index, exp_or_obs, mass)
                    if d == -1 or n == -1:
                        continue
                    else:
                        if self.mass_ratio > maxi:
                            maxi = self.mass_ratio
                            pos = index
            return pos

    def set_result(self, pos):
        if pos == -1:
            self.obs_ratio = -1
            self.result = -1
            self.channel = pos
        else:
            if self.obs_ratio >= 1:
                self.result = 0
                self.channel = pos
            elif self.obs_ratio < 0:
                self.result = -1
                self.channel = pos
            else:
                self.result = 1
                self.channel = pos

    def result_based_on_branches(self, pos, coupling, obs_lower):
        obs_upper_branch = self.get_limit_from_data(coupling, pos, self.coupling_obs_upper, self.coupling_MB_obs)
        ch2_obs_upper_branch, ch2_exp_upper_branch = -1, -1
        if pos == 3:
            ch2_obs_upper_branch = self.get_limit_from_data(coupling, pos - 1,
                                                            self.coupling_obs_upper, self.coupling_MT_obs)
            ch2_exp_upper_branch = self.get_limit_from_data(coupling, pos - 1,
                                                            self.coupling_exp_upper, self.coupling_MT_exp)
        if pos == 3 or pos == 2:
            if obs_lower <= coupling <= obs_upper_branch:
                self.result = 0
                self.channel = pos
            elif obs_upper_branch <= coupling <= ch2_obs_upper_branch:
                self.result = 0
                self.channel = pos
            elif coupling >= ch2_obs_upper_branch:
                observed_ratio = ch2_obs_upper_branch / coupling
                self.obs_ratio = observed_ratio
                self.result = 0
                self.channel = pos
            else:
                self.result = 1
                self.channel = pos

            if coupling >= ch2_exp_upper_branch:
                expected_ratio = ch2_exp_upper_branch / coupling
                self.exp_ratio = expected_ratio

        else:
            self.set_result(pos)

    def dealing_with_width_limits(self, position):
        width_ratio_in = self.model_coupling_calc(position)
        if position == -1:
            self.obs_ratio, self.exp_ratio = -1, -1
            self.result = -1
            self.channel = position
        else:
            mT = self.m.get_mT()
            k_calc = self.m.kappa_coupling_from_width(mT, width_ratio_in)
            width_ratio, mT_interp = self.get_limit_from_data(width_ratio_in, position,
                                                              self.coupling_obs_lower, self.coupling_MT_obs)
            k_obs = self.m.kappa_coupling_from_width(mT_interp, width_ratio)

            width_ratio, mT_interp = self.get_limit_from_data(width_ratio_in, position, self.coupling_exp_lower,
                                                              self.coupling_MT_exp)
            k_exp = self.m.kappa_coupling_from_width(mT_interp, width_ratio)

            self.obs_ratio, self.exp_ratio = obs_exp_ratio_calc(k_calc, k_obs, k_exp)
            self.set_result(position)

    def coupling_limit(self):
        if self.VLB:
            if self.m.model() == 'Singlet':
                position = self.identify_strong_limit(self.coupling_obs_lower, self.coupling_MB_obs)
                coupling_in = self.model_coupling_calc(position)
                obs = self.get_limit_from_data(coupling_in, position, self.coupling_obs_lower, self.coupling_MB_obs)
                exp = self.get_limit_from_data(coupling_in, position, self.coupling_exp_lower, self.coupling_MB_exp)
                self.obs_ratio, self.exp_ratio = obs_exp_ratio_calc(coupling_in, obs, exp)
                self.set_result(position)
                print("coupling result:", self.result, self.obs_ratio, self.exp_ratio, self.channel)
                return self.result, self.obs_ratio, self.exp_ratio, self.channel
            elif self.m.model() == 'Doublet':
                position = self.identify_strong_limit(self.coupling_exp_lower, self.coupling_MB_obs)
                coupling_in = self.model_coupling_calc(position)
                obs = self.get_limit_from_data(coupling_in, position, self.coupling_obs_lower, self.coupling_MB_obs)
                exp = self.get_limit_from_data(coupling_in, position, self.coupling_exp_lower, self.coupling_MB_exp)
                self.obs_ratio, self.exp_ratio = obs_exp_ratio_calc(coupling_in, obs, exp)
                self.set_result(position)
                print("coupling result:", self.result, self.obs_ratio, self.exp_ratio, self.channel)
                return self.result, self.obs_ratio, self.exp_ratio, self.channel
            else:
                raise Exception("Error. There are no coupling limits for this model")
        else:
            if self.m.model() == 'Singlet':
                position = self.identify_strong_limit(self.coupling_obs_lower, self.coupling_MT_obs)
                if position in range(0, 10):
                    coupling_in = self.model_coupling_calc(position)
                    obs_lower_branch = self.get_limit_from_data(coupling_in, position,
                                                                self.coupling_obs_lower, self.coupling_MT_obs)
                    exp_lower_branch = self.get_limit_from_data(coupling_in, position,
                                                                self.coupling_exp_lower, self.coupling_MT_exp)

                    self.obs_ratio, self.exp_ratio = obs_exp_ratio_calc(coupling_in, obs_lower_branch, exp_lower_branch)

                    self.result_based_on_branches(position, coupling_in, obs_lower_branch)
                else:
                    self.dealing_with_width_limits(position)
                print("coupling result:", self.result, self.obs_ratio, self.exp_ratio, self.channel)
                return self.result, self.obs_ratio, self.exp_ratio, self.channel

            elif self.m.model() == 'Doublet':
                position = self.identify_strong_limit(self.coupling_exp_lower, self.coupling_MT_obs)
                if position in range(0, 2):
                    coupling_in = self.model_coupling_calc(position)
                    obs = self.get_limit_from_data(coupling_in, position, self.coupling_obs_lower, self.coupling_MT_obs)
                    exp = self.get_limit_from_data(coupling_in, position, self.coupling_exp_lower, self.coupling_MT_exp)
                    self.obs_ratio, self.exp_ratio = obs_exp_ratio_calc(coupling_in, obs, exp)
                    self.set_result(position)
                else:
                    self.dealing_with_width_limits(position)
            else:
                raise Exception("Error. There are no coupling limits for this model")

    def check_xs_and_coupling_limits(self):
        coupling_res, coupling_obs_ratio, coupling_exp_ratio, coupling_channel = self.coupling_limit()
        xs_res, xs_obs_ratio, xs_exp_ratio, xs_channel = self.check_channel()
        xs_is_stronger = biggest_ratio(coupling_obs_ratio, xs_obs_ratio)
        if xs_is_stronger:
            self.result = xs_res
            self.obs_ratio = xs_obs_ratio
            self.exp_ratio = xs_exp_ratio
            self.channel = xs_channel
        else:
            self.result = coupling_res
            self.obs_ratio = coupling_obs_ratio
            self.exp_ratio = coupling_exp_ratio
            if coupling_channel != -1:
                self.channel = coupling_channel + len(self.key)
            else:
                self.channel = coupling_channel
        print("end results:", self.result, self.obs_ratio, self.exp_ratio, self.channel)

    def all_couplings(self):
        with open("coupling_info.dat", "w") as f:
            f.write("************* File for each coupling limit information*****************\n")
            f.write("This File has been generated with PyTop version 0.1\n")
            f.write(f"With the T quark in the {self.m.model()} scenario\n")
            for i, proc in enumerate(self.process):
                f.write("***********************************************************************\n")
                f.write(f"channel {i}:\n")
                f.write(f"{proc} \t\t {self.label[i]} ({self.expt[i]}) "
                        f"\t sqrt(s) = {self.energy[i]} TeV\t luminosity = {self.luminosity[i]} fb-1\n")

    def coupling_and_xs_info(self):
        with open("coupling_and_xs_info.dat", "w") as f:
            f.write("************* cross section limit information *****************\n")
            f.write("This File has been generated with PyTop version 0.1\n")
            f.write(f"With the T quark in the {self.m.model()} scenario\n")
            count = 0
            for i, proc in enumerate(self.process):
                f.write("***********************************************************************\n")
                f.write(f"channel {i}:\n")
                f.write(f"{proc} \t\t {self.label[i]} ({self.expt[i]}) "
                        f"\t sqrt(s) = {self.energy[i]} TeV\t luminosity = {self.luminosity[i]} fb-1\n")
                count = count + i
            f.write("************* Coupling limits information part*****************\n")
            f.write(f"T quark in the {self.m.model()} scenario\n")
            for i, proc in enumerate(self.coupling_process):
                f.write("***********************************************************************\n")
                f.write(f"channel {i + count + 1}:\n")
                f.write(f"{proc} \t\t {self.coupling_label[i]} ({self.coupling_expt[i]}) "
                        f"\t sqrt(s) = {self.coupling_energy[i]} TeV\t luminosity = {self.coupling_luminosity[i]} fb-1\n")

    def fill_sin_and_kappa(self):
        #singlet and doublet and sin_right
        if self.VLB:
            if self.m.model() == 'Singlet':
                self.k_keys = [
                    self.key[j]
                    for j in range(len(self.which_coupling))
                    if self.which_coupling[j] == 'k_B'
                ]
                self.width_keys = 0
                self.sin_l_keys = [
                    self.key[j]
                    for j in range(len(self.which_coupling))
                    if self.which_coupling[j] == "s_l"
                ]
            else:
                    self.k_keys = [
                        self.key[j]
                        for j in range(len(self.which_coupling))
                        if self.which_coupling[j] == 'k_B'
                        ]
                    self.width_keys = 0

        else:
            self.sin_l_keys = [
                self.key[j]
                for j in range(len(self.which_coupling))
                if self.which_coupling[j] == "|sin_left|"
            ]
            self.k_keys = [
                self.key[j]
                for j in range(len(self.which_coupling))
                if self.which_coupling[j] == 'kappa'
            ]
            self.width_keys = [
                self.key[j]
                for j in range(len(self.which_coupling))
                if self.which_coupling[j] == 'width_mass_ratio'
            ]
