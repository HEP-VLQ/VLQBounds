from model import *
from manip import TheoryCalc
import sys
from utils import load_data_from_files
from scipy.interpolate import interp1d


class Coupling(TheoryCalc):
    def __init__(self, m):
        TheoryCalc.__init__(self, m)
        if isinstance(m, Singlet) or isinstance(m, Doublet) or isinstance(m, PureDecay):
            self.m = m
        else:
            raise Exception('Invalid model. Must be a singlet or Doublet')

        self.sin_l = []
        self.k = []

        if self.m.model() == 'Singlet':
            number_of_atlas_cms_tables = 8
            self.file_name = [None] * number_of_atlas_cms_tables
            self.key = [None] * number_of_atlas_cms_tables
            self.label = [None] * number_of_atlas_cms_tables
            self.expt = [None] * number_of_atlas_cms_tables
            self.MT = [None] * number_of_atlas_cms_tables
            self.obs = [None] * number_of_atlas_cms_tables
            self.exp = [None] * number_of_atlas_cms_tables
            self.process = [None] * number_of_atlas_cms_tables
            self.energy = [None] * number_of_atlas_cms_tables
            self.luminosity = [None] * number_of_atlas_cms_tables
        elif self.m.model() == 'Doublet':
            number_of_atlas_cms_tables = 2
            self.file_name = [None] * number_of_atlas_cms_tables
            self.key = [None] * number_of_atlas_cms_tables
            self.label = [None] * number_of_atlas_cms_tables
            self.expt = [None] * number_of_atlas_cms_tables
            self.MT = [None] * number_of_atlas_cms_tables
            self.obs = [None] * number_of_atlas_cms_tables
            self.exp = [None] * number_of_atlas_cms_tables
            self.process = [None] * number_of_atlas_cms_tables
            self.energy = [None] * number_of_atlas_cms_tables
            self.luminosity = [None] * number_of_atlas_cms_tables
        else:
            print(f"Warning. There is no coupling limits for this model {self.m.model()}")

    def fill_coupling_tables(self):
        if self.m.model() == 'Singlet':
            self.key[0] = '05606f7b'
            self.label[0] = 'arXiv:1602.05606'
            self.expt[0] = 'ATLAS'
            self.file_name[0] = '1602.05606_ATLAS_Fig7-b_pp_Tbj_Wb_s_L.txt'
            self.process[0] = "|sin_left|"
            self.energy[0] = 8
            self.luminosity[0] = 20.3

            self.key[1] = '07343f8as_L'
            self.label[1] = 'arXiv:1812.07343'
            self.expt[1] = 'ATLAS'
            self.file_name[1] = '1812.07343_ATLAS_fig8a_pp_Tbq_wb_Singlet_s_L.txt'
            self.process[1] = "|sin_left|"
            self.energy[1] = 13
            self.luminosity[1] = 36.1

            self.key[2] = '09743f6b_s_L'
            self.label[2] = 'arXiv:1812.09743'
            self.expt[2] = 'ATLAS'
            self.file_name[2] = '1812.09743_ATLAS_Fig6b_pp_Tbq_tZ.txt'
            self.process[2] = "|sin_left|"
            self.energy[2] = 13
            self.luminosity[2] = 36.1

            self.key[3] = '10555f16b_s_L'
            self.label[3] = 'arXiv:1806.10555'
            self.expt[3] = 'ATLAS'
            self.file_name[3] = '1806.10555_ATLAS_Fig16-b_pp_Tbq_Zt_Singlet.txt'
            self.process[3] = "|sin_left|"
            self.energy[3] = 13
            self.luminosity[3] = 36.1

            self.key[4] = '16561f12a_k_T'
            self.label[4] = 'arXiv:2402.16561'
            self.expt[4] = 'ATLAS'
            self.file_name[4] = '2402.16561_ATLAS_Fig12a_pp_T_Ht_Zt_singlet.txt'
            self.process[4] = 'kappa'
            self.energy[4] = 13
            self.luminosity[4] = 139

            self.key[5] = '07045f9_k_T'
            self.label[5] = 'arXiv:2201.07045'
            self.expt[5] = 'ATLAS'
            self.file_name[5] = '2201.07045_ATLAS_Fig9_pp_Tbq_Wb_Ht_Zt_singlet.txt'
            self.process[5] = 'kappa'
            self.energy[5] = 13
            self.luminosity[5] = 139

            self.key[6] = '03401f13a'
            self.label[6] = 'arXiv:2305.03401'
            self.expt[6] = 'ATLAS'
            self.file_name[6] = '2305.03401_ATLAS_Fig13a_pp_Tqt_Wb_Zt_Ht_singlet.txt'
            self.process[6] = 'kappa'
            self.energy[6] = 13
            self.luminosity[6] = 139

            self.key[7] = '07584f9a'
            self.label[7] = 'arXiv:2307.07584'
            self.expt[7] = 'ATLAS'
            self.process[7] = 'kappa'
            self.file_name[7] = '2307.07584_ATLAS_Fig9a_pp_T_Wb_Ht_Zt_singlet.txt'
            self.energy[7] = 13
            self.luminosity[7] = 139

        elif self.m.model() == 'Doublet':
            self.key[0] = '03401f13b'
            self.label[0] = 'arXiv:2305.03401'
            self.expt[0] = 'ATLAS'
            self.file_name[0] = '2305.03401_ATLAS_Fig13b_pp_Tqt_Ht_Zt_doublet.txt'
            self.process[0] = 'kappa'
            self.energy[0] = 13
            self.luminosity[0] = 139

            self.key[1] = '07584f9b'
            self.label[1] = 'arXiv:2307.07584'
            self.expt[1] = 'ATLAS'
            self.file_name[1] = '2307.07584_ATLAS_Fig9b_pp_T_Ht_Zt_doublet.txt'
            self.process[1] = 'kappa'
            self.energy[1] = 13
            self.luminosity[1] = 139

        load_data_from_files(self.file_name, len(self.key), self.MT, self.exp, self.obs, self.expt)

    def model_coupling_calc(self, i):
        if self.m.model() == 'Singlet':
            if self.key[i] in self.sin_l:
                return self.m.sin_left()
            elif self.key[i] in self.k:
                return self.m.universal_coupling()
            else:
                raise Exception("Something went wrong in filling coupling tables")
        elif self.m.model() == 'Doublet':
            if self.key[i] in self.k:
                return self.m.universal_coupling()
            else:
                raise Exception("Something went wrong in filling coupling tables")
        else:
            raise Exception(f"There are no coupling limits for the model {self.m.model}")

    def get_limit_from_data(self, num, index, t):
        if 0 <= num:
            if min(self.MT[index]) <= self.m.mv() <= max(self.MT[index]):
                expected_or_observed = interp1d(self.MT[index], t[index], 'linear')
                # donne l'observed limit qui correspont à la masse théorique entrée par l'utilisateur
                denom = expected_or_observed(self.m.mv())
                return denom
            else:
                d = -1
                return d
        else:
            d = -1
            return d

    def identify_strong_limit(self):
        try:
            maximum = -1000000
            pos = -1
            for index, k in enumerate(self.key):
                n = self.model_coupling_calc(index)
                d = self.get_limit_from_data(n, index, self.obs)
                if d == -1 or n == -1:
                    continue
                rat = n/d
                if rat > maximum:
                    maximum = rat
                    pos = index
            return pos
        except UnboundLocalError:
            sys.exit(f"The mass {self.m.mv()} is not in the range of included experiment files")

    def coupling_limit(self):
        position = self.identify_strong_limit()
        numerator = self.model_coupling_calc(position)
        deno = self.get_limit_from_data(numerator, position, self.obs)
        deno1 = self.get_limit_from_data(numerator, position, self.exp)
        deno2 = 0
        if position == 3:
            deno2 = self.get_limit_from_data(numerator, position - 1, self.exp)
        observed_ratio = numerator / deno
        self.model_observed_ratio = observed_ratio
        if position == 3 or position == 2:
            if deno <= numerator <= deno1:
                self.allowed_or_excluded = 0
                self.channel = position
            elif deno1 <= numerator <= deno2:
                self.allowed_or_excluded = 0
                self.channel = position
            else:
                self.allowed_or_excluded = 1
                self.channel = position
        else:
            if self.model_observed_ratio >= 1:
                self.allowed_or_excluded = 0
                self.channel = position
            elif self.model_observed_ratio < 0:
                self.allowed_or_excluded = -1
                self.channel = position
            else:
                self.allowed_or_excluded = 1
                self.channel = position

    def all_couplings(self):
        with open("coupling.dat", "w") as f:
            f.write("coupling energy experiment  process_number identifier(channel)\n")
            for i in range(len(self.key)):
                f.write(f"{self.process[i]} {self.energy[i]} {self.expt[i]} {self.label[i]} {i}\n")

    def fill_sin_and_kappa(self):
        self.sin_l = [
            self.key[j]
            for j in range(len(self.process))
            if self.process[j] == "|sin_left|"
        ]
        self.k = [
            self.key[j]
            for j in range(len(self.process))
            if self.process[j] == 'kappa'
        ]
