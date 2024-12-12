import os
from typing import List, Optional
from numpy.typing import NDArray
import numpy as np
from .models import *
from .manip import TheoryCalc
from scipy.interpolate import interp1d
from .utils import coupling_data_loading, obs_exp_ratio_calc, biggest_ratio, from_cf_to_kappa


class Coupling(TheoryCalc):
    def __init__(self, m):
        super().__init__(m)
        self.coupling_luminosity: Optional[List[float]] = None
        self.coupling_energy: Optional[List[int]] = None
        self.which_coupling: Optional[List[str]] = None
        self.coupling_process: Optional[List[str]] = None
        self.coupling_exp_lower: Optional[List[NDArray[np.float64]]] = None
        self.coupling_obs_lower: Optional[List[NDArray[np.float64]]] = None
        self.coupling_exp_upper: Optional[List[NDArray[np.float64]]] = None
        self.coupling_obs_upper: Optional[List[NDArray[np.float64]]] = None
        self.coupling_MY_exp: Optional[List[NDArray[np.float64]]] = None
        self.coupling_MY_obs: Optional[List[NDArray[np.float64]]] = None
        self.coupling_MX_exp: Optional[List[NDArray[np.float64]]] = None
        self.coupling_MX_obs: Optional[List[NDArray[np.float64]]] = None
        self.coupling_MB_exp: Optional[List[NDArray[np.float64]]] = None
        self.coupling_MB_obs: Optional[List[NDArray[np.float64]]] = None
        self.coupling_MT_exp: Optional[List[NDArray[np.float64]]] = None
        self.coupling_MT_obs: Optional[List[NDArray[np.float64]]] = None
        self.coupling_expt: Optional[List[str]] = None
        self.coupling_label: Optional[List[str]] = None
        self.coupling_key: Optional[List[str]] = None
        self.coupling_file_name: Optional[List[str]] = None
        if isinstance(m, (SingletT, DoubletT, PureT, SingletB, DoubletB,
                          PureB, DoubletX, DoubletY, TripletY)):
            self.m = m
        else:
            raise Exception('Invalid model. Must be a Singlet or Doublet')
        self.sin_l_keys: List[str] = []
        self.sin_r_keys: List[str] = []
        self.k_keys: List[str] = []
        self.mass_ratio: Optional[float] = None
        self.initialize_coupling_data()

    def initialize_coupling_lists(self, number_of_atlas_cms_tables):
        self.coupling_file_name = [None] * number_of_atlas_cms_tables
        self.coupling_key = [None] * number_of_atlas_cms_tables
        self.coupling_label = [None] * number_of_atlas_cms_tables
        self.coupling_expt = [None] * number_of_atlas_cms_tables
        self.coupling_process = [None] * number_of_atlas_cms_tables
        self.which_coupling = [None] * number_of_atlas_cms_tables
        self.coupling_energy = [None] * number_of_atlas_cms_tables
        self.coupling_luminosity = [None] * number_of_atlas_cms_tables
        self.coupling_obs_upper = [None] * number_of_atlas_cms_tables
        self.coupling_exp_upper = [None] * number_of_atlas_cms_tables
        self.coupling_obs_lower = [None] * number_of_atlas_cms_tables
        self.coupling_exp_lower = [None] * number_of_atlas_cms_tables
        if isinstance(self.m, (SingletT, DoubletT)):
            self.coupling_MT_obs = [None] * number_of_atlas_cms_tables
            self.coupling_MT_exp = [None] * number_of_atlas_cms_tables
        elif isinstance(self.m, (SingletB, DoubletB)):
            self.coupling_MB_obs = [None] * number_of_atlas_cms_tables
            self.coupling_MB_exp = [None] * number_of_atlas_cms_tables
        elif isinstance(self.m, DoubletX):
            self.coupling_MX_obs = [None] * number_of_atlas_cms_tables
            self.coupling_MX_exp = [None] * number_of_atlas_cms_tables
        elif isinstance(self.m, (DoubletY, TripletY)):
            self.coupling_MY_obs = [None] * number_of_atlas_cms_tables
            self.coupling_MY_exp = [None] * number_of_atlas_cms_tables

    def get_number_of_tables(self, vlq='T'):
        if vlq == 'B':
            if self.m.model() == 'Singlet':
                return 6
            elif self.m.model() == 'Doublet':
                return 2
            else:
                print(f"Warning. There is no coupling limits for this model {self.m.model()}")
                return 0
        elif vlq == 'X':
            return 3
        elif vlq == 'Y':
            if self.m.model() == 'Doublet':
                return 5
            elif self.m.model() == 'Triplet':
                return 1
        else:
            if self.m.model() == 'Singlet':
                return 21
            elif self.m.model() == 'Doublet':
                return 6
            else:
                print(f"Warning. There is no coupling limits for this model {self.m.model()}")
                return 0

    def initialize_coupling_data(self):
        if isinstance(self.m, (SingletB, DoubletB)):
            number_of_atlas_cms_tables = self.get_number_of_tables(vlq='B')
            if number_of_atlas_cms_tables > 0:
                self.initialize_coupling_lists(number_of_atlas_cms_tables)
        elif isinstance(self.m, DoubletX):
            number_of_atlas_cms_tables = self.get_number_of_tables(vlq='X')
            if number_of_atlas_cms_tables > 0:
                self.initialize_coupling_lists(number_of_atlas_cms_tables)
        elif isinstance(self.m, (DoubletY, TripletY)):
            number_of_atlas_cms_tables = self.get_number_of_tables(vlq='Y')
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
                self.coupling_process[0] = 'pp --> Bbq --> bH --> b, bb'
                self.which_coupling[0] = "k_B"
                self.coupling_energy[0] = 13
                self.coupling_luminosity[0] = 139

                self.coupling_key[1] = '01486f43'
                self.coupling_label[1] = 'arXiv:1802.01486'
                self.coupling_expt[1] = 'CMS'
                self.coupling_file_name[1] = '2405.17605_Fig43_upper_pp_B_bH_singlet_1802.01486_cf.dat'
                self.coupling_process[1] = 'pp --> Bqq --> bH --> b,bb,bq'
                self.which_coupling[1] = "k_B"
                self.coupling_energy[1] = 13
                self.coupling_luminosity[1] = 35.9

                self.coupling_key[2] = '01486f43b'
                self.coupling_label[2] = 'arXiv:1809.08597'
                self.coupling_expt[2] = 'CMS'
                self.coupling_file_name[2] = '2405.17605_Fig43_upper_pp_Bbq_tW_singlet_1809.08597_cf.dat'
                self.coupling_process[2] = 'pp --> Bbq --> tW --> bqq,lnu/blnu,qq'
                self.which_coupling[2] = "k_B"
                self.coupling_energy[2] = 13
                self.coupling_luminosity[2] = 35.9

                self.coupling_key[3] = '10216f43'
                self.coupling_label[3] = 'arXiv:2111.10216'
                self.coupling_expt[3] = 'CMS'
                self.coupling_file_name[3] = '2405.17605_Fig43_upper_pp_Bbq_tW_singlet_2111.10216_cf.dat'
                self.coupling_process[3] = 'pp --> Bbq --> tW --> bqq,lnu/qq'
                self.which_coupling[3] = "k_B"
                self.coupling_energy[3] = 13
                self.coupling_luminosity[3] = 138

                self.coupling_key[4] = '01486f43t'
                self.coupling_label[4] = 'arXiv:1809.08597'
                self.coupling_expt[4] = 'CMS'
                self.coupling_file_name[4] = '2405.17605_Fig43_upper_pp_Btq_tW_singlet_1809.08597_cf.dat'
                self.coupling_process[4] = 'pp --> Btq --> tW --> bqq,lnu/blnu,qq'
                self.which_coupling[4] = "k_B"
                self.coupling_energy[4] = 13
                self.coupling_luminosity[4] = 35.9

                self.coupling_key[5] = '10216f43t'
                self.coupling_label[5] = 'arXiv:2111.10216'
                self.coupling_expt[5] = 'CMS'
                self.coupling_file_name[5] = '2405.17605_Fig43_upper_pp_Btq_tW_singlet_2111.10216_cf.dat'
                self.coupling_process[5] = 'pp --> Btq --> tW --> bqq,lnu/qq'
                self.which_coupling[5] = "k_B"
                self.coupling_energy[5] = 13
                self.coupling_luminosity[5] = 138

                expected = [self.coupling_exp_upper, self.coupling_exp_lower]
                observed = [self.coupling_obs_lower, self.coupling_obs_upper]
                mass = [self.coupling_MB_obs, self.coupling_MB_exp]
                coupling_data_loading(self.coupling_file_name, len(self.coupling_key), mass, expected, observed,
                                      self.coupling_expt, vlq='B')

            elif self.m.model() == 'Doublet':
                self.coupling_key[0] = '02595f9b'
                self.coupling_label[0] = 'arXiv:2308.02595'
                self.coupling_expt[0] = 'ATLAS'
                self.coupling_file_name[0] = '2308.02595_ATLAS_Fig9b_pp_B_bH_k_doublet.dat'
                self.coupling_process[0] = 'pp --> Bbq --> bH --> bbb'
                self.which_coupling[0] = "k_B"
                self.coupling_energy[0] = 13
                self.coupling_luminosity[0] = 139

                self.coupling_key[1] = '01486f43l'
                self.coupling_label[1] = 'arXiv:1802.01486'
                self.coupling_expt[1] = 'CMS'
                self.coupling_file_name[1] = '2405.17605_Fig43_lower_pp_B_bH_doublet_1802.01486_cf.dat'
                self.coupling_process[1] = 'pp --> Bbq --> bH -- bbb'
                self.which_coupling[1] = "k_B"
                self.coupling_energy[1] = 13
                self.coupling_luminosity[1] = 35.9

                expected = [self.coupling_exp_upper, self.coupling_exp_lower]
                observed = [self.coupling_obs_lower, self.coupling_obs_upper]
                mass = [self.coupling_MB_obs, self.coupling_MB_exp]
                coupling_data_loading(self.coupling_file_name, len(self.coupling_key), mass, expected,
                                      observed, self.coupling_expt, vlq='B')

            self.coupling_factor_to_coupling_strength('B')

        elif self.VLX:
            self.coupling_key[0] = '08597Fig44l'
            self.coupling_label[0] = 'arXiv:1809.08597'
            self.coupling_expt[0] = 'CMS'
            self.coupling_file_name[0] = '2405.17605_CMS_Fig44_left_pp_tqX_tW_1809.08597.dat'
            self.coupling_process[0] = 'pp --> Xtq --> tW --> bqq,lnu/blnu,qq'
            self.which_coupling[0] = "k_x"
            self.coupling_energy[0] = 13
            self.coupling_luminosity[0] = 35.9

            self.coupling_key[1] = '10216Fig44l'
            self.coupling_label[1] = 'arXiv:2111.10216'
            self.coupling_expt[1] = 'CMS'
            self.coupling_file_name[1] = '2405.17605_CMS_Fig44_left_pp_tqX_tW_2111.10216.dat'
            self.coupling_process[1] = 'pp --> Xtq --> tW --> bqq,lnu/blnu,qq'
            self.which_coupling[1] = "k_x"
            self.coupling_energy[1] = 13
            self.coupling_luminosity[1] = 138

            self.coupling_key[2] = '11883f10b'
            self.coupling_label[2] = 'arXiv:1807.11883'
            self.coupling_expt[2] = 'ATLAS'
            self.coupling_file_name[2] = '1807.11883_ATLAS_Fig10b_pp_XX_Wt_coupling.dat'
            self.coupling_process[2] = 'pp --> XX(Xtq) --> tW --> '
            self.which_coupling[2] = "k_x"
            self.coupling_energy[2] = 13
            self.coupling_luminosity[2] = 36.1

            expected = [self.coupling_exp_upper, self.coupling_exp_lower]
            observed = [self.coupling_obs_lower, self.coupling_obs_upper]
            mass = [self.coupling_MX_obs, self.coupling_MX_exp]
            coupling_data_loading(self.coupling_file_name, len(self.coupling_key), mass, expected, observed,
                                  self.coupling_expt, vlq='X')
        elif self.VLY:
            if self.m.model() == 'Doublet':
                self.coupling_key[0] = '08328Fig44r'
                self.coupling_label[0] = 'arXiv:1701.08328'
                self.coupling_expt[0] = 'CMS'
                self.coupling_file_name[0] = '2405.17605_CMS_Fig44_right_pp_tqY_bW_1701.08328.dat'
                self.coupling_process[0] = 'pp --> Ytq --> bW --> bqq,lnu/blnu,qq'
                self.which_coupling[0] = "k_y"
                self.coupling_energy[0] = 13
                self.coupling_luminosity[0] = 2.3

                self.coupling_key[1] = '05606f8b'
                self.coupling_label[1] = 'arXiv:1602.05606'
                self.coupling_expt[1] = 'ATLAS'
                self.coupling_file_name[1] = '1602.05606_ATLAS_Fig8b_pp_Ybj_Wb_Doublet_sinR.dat'
                self.coupling_process[1] = 'pp --> Ybq --> bW --> b,lnu'
                self.which_coupling[1] = "k_y"
                self.coupling_energy[1] = 8
                self.coupling_luminosity[1] = 20.3

                self.coupling_key[2] = '072f10b'
                self.coupling_label[2] = 'ATLAS_CONF_2016_072'
                self.coupling_expt[2] = 'ATLAS'
                self.coupling_file_name[2] = 'ATLAS_CONF_2016_072_fig10b_doublet.dat'
                self.coupling_process[2] = 'pp --> Ybq --> bW --> b,lnu'
                self.which_coupling[2] = "k_y"
                self.coupling_energy[2] = 13
                self.coupling_luminosity[2] = 3.2

                self.coupling_key[3] = '07343f8c'
                self.coupling_label[3] = 'arXiv:1812.07343'
                self.coupling_expt[3] = 'ATLAS'
                self.coupling_file_name[3] = '1812.07343_ATLAS_pp_Ybq_Wbbq_Fig8c_doublet_Y_RH_sinR.dat'
                self.coupling_process[3] = 'pp --> Ybq --> bW --> b,lnu'
                self.which_coupling[3] = "k_y"
                self.coupling_energy[3] = 13
                self.coupling_luminosity[3] = 36.1

                self.coupling_key[4] = '20273'
                self.coupling_label[4] = 'arXiv:2409.20273'
                self.coupling_expt[4] = 'ATLAS'
                self.coupling_file_name[4] = '2409.20273_ATLAS_Fig6_pp_Ybq_Wb_doublet_BY.dat'
                self.coupling_process[4] = 'pp --> Ybq --> bW --> b, qq'
                self.which_coupling[4] = "k_y"
                self.coupling_energy[4] = 13
                self.coupling_luminosity[4] = 36.1

                expected = [self.coupling_exp_upper, self.coupling_exp_lower]
                observed = [self.coupling_obs_lower, self.coupling_obs_upper]
                mass = [self.coupling_MY_obs, self.coupling_MY_exp]
                coupling_data_loading(self.coupling_file_name, len(self.coupling_key), mass, expected, observed,
                                      self.coupling_expt, vlq='Y')
            elif self.m.model() == 'Triplet':
                self.coupling_key[0] = '07343f8b'
                self.coupling_label[0] = 'ArXiv:1812.07343'
                self.coupling_expt[0] = 'ATLAS'
                self.coupling_file_name[0] = '1812.07343_ATLAS_Fig8b_pp_Ybq_Wb_triplet_Y_LH_sinL.dat'
                self.coupling_process[0] = 'pp --> Ybq --> bW --> b,lnu'
                self.which_coupling[0] = "s_d_l"
                self.coupling_energy[0] = 13
                self.coupling_luminosity[0] = 36.1

                expected = [self.coupling_exp_upper, self.coupling_exp_lower]
                observed = [self.coupling_obs_lower, self.coupling_obs_upper]
                mass = [self.coupling_MY_obs, self.coupling_MY_exp]
                coupling_data_loading(self.coupling_file_name, len(self.coupling_key), mass, expected, observed,
                                      self.coupling_expt, vlq='Y')
        else:
            if self.m.model() == 'Singlet':
                self.coupling_key[0] = '05606f7b'
                self.coupling_label[0] = 'arXiv:1602.05606'
                self.coupling_expt[0] = 'ATLAS'
                self.coupling_file_name[0] = '1602.05606_ATLAS_f7b_pp_Tbj_Wbbj_s_L_Singlet.dat'
                self.coupling_process[0] = 'pp --> Tbq --> Wb --> lnu,b'
                self.which_coupling[0] = "s_l"
                self.coupling_energy[0] = 8
                self.coupling_luminosity[0] = 20.3

                self.coupling_key[1] = '07343f8as_L'
                self.coupling_label[1] = 'arXiv:1812.07343'
                self.coupling_expt[1] = 'ATLAS'
                self.coupling_file_name[1] = '1812.07343_ATLAS_f8a_pp_Tbq_wbbq_Singlet_s_L.dat'
                self.which_coupling[1] = "s_l"
                self.coupling_process[1] = 'pp --> Tbq --> Wb --> '
                self.coupling_energy[1] = 13
                self.coupling_luminosity[1] = 36.1

                self.coupling_key[2] = '09743f6b_s_L'
                self.coupling_label[2] = 'arXiv:1812.09743'
                self.coupling_expt[2] = 'ATLAS'
                self.coupling_file_name[2] = '1812.09743_ATLAS_f6b_pp_Tbq_tZbq_s_L_Singlet.dat'
                self.which_coupling[2] = "s_l"
                self.coupling_process[2] = 'pp --> Tbq --> tZ --> '
                self.coupling_energy[2] = 13
                self.coupling_luminosity[2] = 36.1

                self.coupling_key[3] = '10555f16b_s_L'
                self.coupling_label[3] = 'arXiv:1806.10555'
                self.coupling_expt[3] = 'ATLAS'
                self.coupling_file_name[3] = '1806.10555_ATLAS_f16b_pp_Tbq_Zt_s_L_Singlet.dat'
                self.coupling_process[3] = 'pp --> Tbq --> tZ --> '
                self.which_coupling[3] = "s_l"
                self.coupling_energy[3] = 13
                self.coupling_luminosity[3] = 36.1

                self.coupling_key[4] = '072f10b'
                self.coupling_label[4] = 'ATLAS-CONF-2016-072'
                self.coupling_expt[4] = 'ATLAS'
                self.coupling_file_name[4] = 'ATLAS-CONF-2016-072_ATLAS_f10a_pp_Tqb_Wb_singlet_s_L.dat'
                self.which_coupling[4] = "s_l"
                self.coupling_process[4] = 'pp --> Tbq --> bW -->'
                self.coupling_energy[4] = 13
                self.coupling_luminosity[4] = 36.1
                
                self.coupling_key[5] = '12802f5'
                self.coupling_label[5] = 'arXiv:2302.12802'
                self.coupling_expt[5] = 'CMS'
                self.coupling_file_name[5] = '2302.12802_CMS_Fig5_pp_Tbq_tH_cf.dat'
                self.which_coupling[5] = "k_T"
                self.coupling_process[5] = 'pp --> Tbq --> tH --> '
                self.coupling_energy[5] = 13
                self.coupling_luminosity[5] = 36.1

                self.coupling_key[6] = '16561f12a_k_T'
                self.coupling_label[6] = 'arXiv:2402.16561'
                self.coupling_expt[6] = 'ATLAS'
                self.coupling_file_name[6] = '2402.16561_ATLAS_Fig12a_pp_T_Ht_Zt_k_T_singlet.dat'
                self.which_coupling[6] = 'k_T'
                self.coupling_process[6] = 'pp --> Tbq --> tZ --> '
                self.coupling_energy[6] = 13
                self.coupling_luminosity[6] = 139

                self.coupling_key[7] = '07045f9_k_T'
                self.coupling_label[7] = 'arXiv:2201.07045'
                self.coupling_expt[7] = 'ATLAS'
                self.coupling_file_name[7] = '2201.07045_ATLAS_f9_pp_Tbq_Htbq_k_T_singlet.dat'
                self.which_coupling[7] = 'k_T'
                self.coupling_process[7] = 'pp --> Tbq --> tH -->'
                self.coupling_energy[7] = 13
                self.coupling_luminosity[7] = 139

                self.coupling_key[8] = '03401f13a'
                self.coupling_label[8] = 'arXiv:2305.03401'
                self.coupling_expt[8] = 'ATLAS'
                self.coupling_file_name[8] = '2305.03401_ATLAS_f13a_pp_Tbq_Ztbq_singlet_k_T.dat'
                self.which_coupling[8] = 'k_T'
                self.coupling_process[8] = 'pp --> Tbq --> tZ(H) -->'
                self.coupling_energy[8] = 13
                self.coupling_luminosity[8] = 139

                self.coupling_key[9] = '07584f9a'
                self.coupling_label[9] = 'arXiv:2307.07584'
                self.coupling_expt[9] = 'ATLAS'
                self.which_coupling[9] = 'k_T'
                self.coupling_process[9] = 'pp --> Tbq --> tZ --> '
                self.coupling_file_name[9] = '2307.07584_ATLAS_f9a_pp_Tbq_Ztbq_k_T_singlet.dat'
                self.coupling_energy[9] = 13
                self.coupling_luminosity[9] = 139

                self.coupling_key[10] = '01062f42u'
                self.coupling_label[10] = 'arXiv:1708.01062'
                self.coupling_expt[10] = 'CMS'
                self.which_coupling[10] = "k_T"
                self.coupling_process[10] = 'pp --> Tbq --> tZbq'
                self.coupling_file_name[10] = '2405.17605_CMS_Fig42_upper_pp_Tbq_tZ_ll_singlet_1708.01062_cf.dat'
                self.coupling_energy[10] = 13
                self.coupling_luminosity[10] = 35.9

                self.coupling_key[11] = '08328f42u'
                self.coupling_label[11] = 'arXiv:1701.08328'
                self.coupling_expt[11] = 'CMS'
                self.which_coupling[11] = "k_T"
                self.coupling_process[11] = 'pp --> Tbq --> tZbq'
                self.coupling_file_name[11] = '2405.17605_CMS_Fig42_upper_pp_T_bW_singlet_1701.08328_cf.dat'
                self.coupling_energy[11] = 13
                self.coupling_luminosity[11] = 2.3

                self.coupling_key[12] = '17605f42u'
                self.coupling_label[12] = 'arXiv:2405.17605'
                self.coupling_expt[12] = 'CMS'
                self.which_coupling[12] = "k_T"
                self.coupling_process[12] = 'pp --> Tbq --> tZbq'
                self.coupling_file_name[12] = '2405.17605_CMS_Fig42_upper_pp_T_combination_singlet_cf.dat'
                self.coupling_energy[12] = 13
                self.coupling_luminosity[12] = 138

                self.coupling_key[13] = '04721f42up1'
                self.coupling_label[13] = 'arXiv:1909.04721'
                self.coupling_expt[13] = 'CMS'
                self.which_coupling[13] = "k_T"
                self.coupling_process[13] = 'pp --> Tbq --> tZbq'
                self.coupling_file_name[13] = '2405.17605_CMS_Fig42_upper_pp_Ttq_tZ_tH_singlet_part1_1909.04721_cf.dat'
                self.coupling_energy[13] = 13
                self.coupling_luminosity[13] = 35.9

                self.coupling_key[14] = '04721f42up2'
                self.coupling_label[14] = 'arXiv:1909.04721'
                self.coupling_expt[14] = 'CMS'
                self.which_coupling[14] = "k_T"
                self.coupling_process[14] = 'pp --> Tbq --> tZbq'
                self.coupling_file_name[14] = '2405.17605_CMS_Fig42_upper_pp_Ttq_tZ_tH_part2_singlet_1909.04721_cf.dat'
                self.coupling_energy[14] = 13
                self.coupling_luminosity[14] = 35.9

                self.coupling_key[15] = '01062f42utq'
                self.coupling_label[15] = 'arXiv:1708.01062'
                self.coupling_expt[15] = 'CMS'
                self.which_coupling[15] = "k_T"
                self.coupling_process[15] = 'pp --> Tbq --> tZbq'
                self.coupling_file_name[15] = '2405.17605_CMS_Fig42_upper_pp_Ttq_tZ_singlet_1708.01062_cf.dat'
                self.coupling_energy[15] = 13
                self.coupling_luminosity[15] = 35.9

                self.coupling_key[16] = '02227f42u'
                self.coupling_label[16] = 'arXiv:2201.02227'
                self.coupling_expt[16] = 'CMS'
                self.which_coupling[16] = "k_T"
                self.coupling_process[16] = 'pp --> Tbq --> tZbq'
                self.coupling_file_name[16] = '2405.17605_CMS_Fig42_upper_pp_T_tZ_singlet_2201.02227_cf.dat'
                self.coupling_energy[16] = 13
                self.coupling_luminosity[16] = 137

                self.coupling_key[17] = '05071f42u'
                self.coupling_label[17] = 'arXiv:2405.05071'
                self.coupling_expt[17] = 'CMS'
                self.which_coupling[17] = "k_T"
                self.coupling_process[17] = 'pp --> Tbq --> tZbq'
                self.coupling_file_name[17] = '2405.17605_CMS_Fig42_upper_pp_T_tZ_tH_singlet_2405.05071_cf.dat'
                self.coupling_energy[17] = 13
                self.coupling_luminosity[17] = 138

                self.coupling_key[18] = '04721f42ubq1'
                self.coupling_label[18] = 'arXiv:1909.04721'
                self.coupling_expt[18] = 'CMS'
                self.which_coupling[18] = "k_T"
                self.coupling_process[18] = 'pp --> Tbq --> (tZ + tH) --> bqq, bb'
                self.coupling_file_name[18] = '2405.17605_CMS_Fig42_upper_pp_Tbq_tZ_tH_singlet_part1_1909.04721_cf.dat'
                self.coupling_energy[18] = 13
                self.coupling_luminosity[18] = 35.9

                self.coupling_key[19] = '04721f42ubq2'
                self.coupling_label[19] = 'arXiv:1909.04721'
                self.coupling_expt[19] = 'CMS'
                self.which_coupling[19] = "k_T"
                self.coupling_process[19] = 'pp --> Tbq --> (tZ + tH) --> bqq, bb'
                self.coupling_file_name[19] = '2405.17605_CMS_Fig42_upper_pp_Tbq_tZ_tH_singlet_part2_1909.04721_cf.dat'
                self.coupling_energy[19] = 13
                self.coupling_luminosity[19] = 35.9

                self.coupling_key[20] = '08789f6a'
                self.coupling_label[20] = 'arXiv:2408.08789'
                self.coupling_expt[20] = 'ATLAS'
                self.which_coupling[20] = 'k_T'
                self.coupling_process[20] = 'pp --> Tb(t)q --> tZ/H --> 1l + 2l + nl'
                self.coupling_file_name[20] = '2408.08789_ATLAS_Fig6a_pp_Tbq_Ht_Zt_singlet.dat'
                self.coupling_energy[20] = 13
                self.coupling_luminosity[20] = 139

                expected = [self.coupling_exp_upper, self.coupling_exp_lower]
                observed = [self.coupling_obs_lower, self.coupling_obs_upper]
                mass = [self.coupling_MT_obs, self.coupling_MT_exp]

                coupling_data_loading(self.coupling_file_name, len(self.coupling_key), mass, expected,
                                      observed, self.coupling_expt)

            elif self.m.model() == 'Doublet':
                self.coupling_key[0] = '03401f13b'
                self.coupling_label[0] = 'arXiv:2305.03401'
                self.coupling_expt[0] = 'ATLAS'
                self.coupling_file_name[0] = '2305.03401_ATLAS_f13b_pp_Tbq_Ztbq_k_T_doublet.dat'
                self.which_coupling[0] = 'k_T'
                self.coupling_process[0] = 'pp --> Tbq --> tZbq'
                self.coupling_energy[0] = 13
                self.coupling_luminosity[0] = 139

                self.coupling_key[1] = '07584f9b'
                self.coupling_label[1] = 'arXiv:2307.07584'
                self.coupling_expt[1] = 'ATLAS'
                self.coupling_file_name[1] = '2307.07584_ATLAS_f9b_pp_Tbq_Ztbq_k_T_doublet.dat'
                self.which_coupling[1] = 'k_T'
                self.coupling_process[1] = 'pp --> Tbq --> tZbq'
                self.coupling_energy[1] = 13
                self.coupling_luminosity[1] = 139

                self.coupling_key[2] = '01062f42l'
                self.coupling_label[2] = 'arXiv:1708.01062'
                self.coupling_expt[2] = 'CMS'
                self.coupling_file_name[2] = '2405.17605_CMS_Fig42_lower_pp_T_tZ_doublet_1708.01062_cf.dat'
                self.which_coupling[2] = 'k_T'
                self.coupling_process[2] = 'pp --> Tbq --> tZbq'
                self.coupling_energy[2] = 13
                self.coupling_luminosity[2] = 35.9

                self.coupling_key[3] = '04721f42lp1'
                self.coupling_label[3] = 'arXiv:1909.04721'
                self.coupling_expt[3] = 'CMS'
                self.coupling_file_name[3] = '2405.17605_CMS_Fig42_lower_pp_T_tZ_tH_doublet_part1_1909.04721_cf.dat'
                self.which_coupling[3] = 'k_T'
                self.coupling_process[3] = 'pp --> Tbq --> tZbq'
                self.coupling_energy[3] = 13
                self.coupling_luminosity[3] = 35.9

                self.coupling_key[4] = '04721f42lp2'
                self.coupling_label[4] = 'arXiv:1909.04721'
                self.coupling_expt[4] = 'CMS'
                self.coupling_file_name[4] = '2405.17605_Fig42_lower_pp_T_tZ_tH_doublet_part2_cf_1909.04721.dat'
                self.which_coupling[4] = 'k_T'
                self.coupling_process[4] = 'pp --> Tbq --> tZbq'
                self.coupling_energy[4] = 13
                self.coupling_luminosity[4] = 35.9

                self.coupling_key[5] = '08789f6b'
                self.coupling_label[5] = 'arXiv:2408.08789'
                self.coupling_expt[5] = 'ATLAS'
                self.which_coupling[5] = 'k_T'
                self.coupling_process[5] = 'pp --> Tb(t)q --> tZ/H --> 1l + 2l + >=3l'
                self.coupling_file_name[5] = '2408.08789_ATLAS_Fig6b_pp_Tbq_Ht_Zt_doublet.dat'
                self.coupling_energy[5] = 13
                self.coupling_luminosity[5] = 139

                expected = [self.coupling_exp_upper, self.coupling_exp_lower]
                observed = [self.coupling_obs_lower, self.coupling_obs_upper]
                mass = [self.coupling_MT_obs, self.coupling_MT_exp]

                coupling_data_loading(self.coupling_file_name, len(self.coupling_key), mass, expected,
                                      observed, self.coupling_expt)

            self.coupling_factor_to_coupling_strength()

    def model_coupling_calc(self, i):
        if self.VLB:
            if i != -1:
                if self.m.model() == 'Singlet':
                    if self.coupling_key[i] in self.k_keys:
                        return self.m.get_coupling_strength()
                    elif self.coupling_key[i] in self.sin_l_keys:
                        return self.m.get_sin_left()
                    else:
                        raise Exception("Something went wrong in filling coupling tables")
                elif self.m.model() == 'Doublet':
                    if self.coupling_key[i] in self.k_keys:
                        return self.m.get_coupling_strength()
                    else:
                        raise Exception("Something went wrong in filling coupling tables")
                else:
                    raise Exception(f"There are no coupling limits for the model {self.m.model}")
            else:
                return -1
        elif self.VLX:
            if i != -1:
                if self.coupling_key[i] in self.k_keys:
                    return self.m.get_coupling_strength()
                else:
                    raise Exception("Something went wrong in filling coupling tables")
            else:
                return -1
        elif self.VLY:
            if i != -1:
                if self.m.model() == 'Doublet':
                    if self.coupling_key[i] in self.k_keys:
                        return self.m.get_coupling_strength()
                elif self.m.model() == 'Triplet':
                    if self.coupling_key[i] in self.sin_l_keys:
                        return self.m.get_sin_down_left()
                else:
                    raise Exception("Something went wrong in filling coupling tables")
            else:
                return -1
        else:
            if self.m.model() == 'Singlet':
                if self.coupling_key[i] in self.sin_l_keys:
                    return self.m.get_sin_left()
                elif self.coupling_key[i] in self.k_keys:
                    return self.m.get_coupling_strength()
                elif self.coupling_key[i] in self.k_keys:
                    if self.which_coupling[i] == "|Tth_coupling|":
                        return self.m.get_sin_left()
                else:
                    raise Exception("Something went wrong in filling coupling tables")
            elif self.m.model() == 'Doublet':
                if self.coupling_key[i] in self.k_keys:
                    return self.m.get_coupling_strength()
                else:
                    raise Exception("Something went wrong in filling coupling tables")
            else:
                raise Exception(f"There are no coupling limits for the model {self.m.model}")

    def get_limit_from_data(self, num, index, t, mass):
        if 0 <= num:
            if self.VLB:
                if self.m.model() == 'Singlet':
                    if min(mass[index]) <= self.m.get_mB() <= max(mass[index]):
                        expected_or_observed = interp1d(mass[index], t[index], 'linear')
                        exp_or_obs = expected_or_observed(self.m.get_mB())
                        return exp_or_obs
                    else:
                        exp_or_obs = -1
                        return exp_or_obs
                elif self.m.model() == 'Doublet':
                    if min(mass[index]) <= self.m.get_mB() <= max(mass[index]):
                        expected_or_observed = interp1d(mass[index], t[index], 'linear')
                        exp_or_obs = expected_or_observed(self.m.get_mB())
                        return exp_or_obs
                    else:
                        exp_or_obs = -1
                        return exp_or_obs

            elif self.VLX:
                if min(mass[index]) <= self.m.get_mX() <= max(mass[index]):
                    expected_or_observed = interp1d(mass[index], t[index], 'linear')
                    exp_or_obs = expected_or_observed(self.m.get_mX())
                    return exp_or_obs
                else:
                    exp_or_obs = -1
                    return exp_or_obs
            elif self.VLY:
                if min(mass[index]) <= self.m.get_mY() <= max(mass[index]):
                    expected_or_observed = interp1d(mass[index], t[index], 'linear')
                    exp_or_obs = expected_or_observed(self.m.get_mY())
                    return exp_or_obs
                else:
                    exp_or_obs = -1
                    return exp_or_obs

            else:
                if self.m.model() == 'Singlet':
                    if self.coupling_key[index] in self.k_keys or self.coupling_key[index] in self.sin_l_keys:
                        if min(mass[index]) <= self.m.get_mT() <= max(mass[index]):
                            expected_or_observed = interp1d(mass[index], t[index], 'linear')
                            exp_or_obs = expected_or_observed(self.m.get_mT())
                            return exp_or_obs
                        else:
                            exp_or_obs = -1
                            return exp_or_obs

                else:
                    if self.coupling_key[index] in self.k_keys:
                        if min(mass[index]) <= self.m.get_mT() <= max(mass[index]):
                            expected_or_observed = interp1d(mass[index], t[index], 'linear')
                            exp_or_obs = expected_or_observed(self.m.get_mT())
                            return exp_or_obs
                        else:
                            exp_or_obs = -1
                            return exp_or_obs
        else:
            exp_or_obs = -1
            return exp_or_obs

    def identify_strong_limit(self, exp_or_obs, mass):
        maxi = float('-inf')
        pos = -1
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

    def set_result(self, pos):
        if pos == -1:
            self._obs_ratio = -1
            self._result = -1
            self._channel = pos
        else:
            if self._obs_ratio >= 1:
                self._result = 0
                self._channel = pos
            elif self._obs_ratio < 0:
                self._result = -1
                self._channel = pos
            else:
                self._result = 1
                self._channel = pos

    def result_based_on_branches(self, pos, pos2, coupling, obs_lower):
        obs_upper_branch = self.get_limit_from_data(coupling, pos, self.coupling_obs_upper, self.coupling_MT_obs)

        if pos == 3:
            ch2_obs_upper_branch = self.get_limit_from_data(coupling, pos - 1, self.coupling_obs_upper,
                                                            self.coupling_MT_obs)
            ch2_exp_upper_branch = self.get_limit_from_data(coupling, pos2 - 1, self.coupling_exp_upper,
                                                            self.coupling_MT_exp)
        elif pos == 2:
            ch2_obs_upper_branch = self.get_limit_from_data(coupling, pos, self.coupling_obs_upper,
                                                            self.coupling_MT_obs)
            ch2_exp_upper_branch = self.get_limit_from_data(coupling, pos2, self.coupling_exp_upper,
                                                            self.coupling_MT_exp)
        else:
            ch2_obs_upper_branch, ch2_exp_upper_branch = None, None

        if pos in [2, 3]:
            if obs_lower <= coupling <= obs_upper_branch:
                self._obs_ratio = coupling / obs_lower
                self._result = 0
                self._channel = pos
            elif obs_upper_branch <= coupling <= ch2_obs_upper_branch:
                self._obs_ratio = coupling / obs_upper_branch
                self._result = 0
                self._channel = pos

            elif coupling > ch2_obs_upper_branch and coupling > obs_upper_branch:
                ch0_obs_lower = self.get_limit_from_data(coupling, 0, self.coupling_obs_lower,
                                                         self.coupling_MT_obs)
                ch1_obs_lower = self.get_limit_from_data(coupling, 1, self.coupling_obs_lower,
                                                         self.coupling_MT_obs)
                ch4_obs_lower = self.get_limit_from_data(coupling, 4, self.coupling_obs_lower, self.coupling_MT_obs)

                if min(self.coupling_MT_obs[0]) <= self.m.get_mT() <= max(self.coupling_MT_obs[0]):
                    self._obs_ratio = coupling / ch0_obs_lower
                    self._result = 0
                    self._channel = 0
                elif min(self.coupling_MT_obs[1]) <= self.m.get_mT() <= max(self.coupling_MT_obs[1]):
                    self._obs_ratio = coupling / ch1_obs_lower
                    self._result = 0
                    self._channel = 1

                elif min(self.coupling_MT_obs[4]) <= self.m.get_mT() <= max(self.coupling_MT_obs[4]):
                    self._obs_ratio = coupling / ch4_obs_lower
                    self._result = 0
                    self._channel = 4

                else:
                    self._obs_ratio = max(ch2_obs_upper_branch, obs_upper_branch) / coupling
                    self._result = 1
                    self._channel = pos

            else:
                self._result = 1
                self._channel = pos

            if ch2_exp_upper_branch is not None and coupling >= ch2_exp_upper_branch:
                expected_ratio = ch2_exp_upper_branch / coupling
                self._exp_ratio = expected_ratio
        else:
            self.set_result(pos)

    def coupling_limit(self):
        if self.VLB:
            if self.m.model() == 'Singlet':
                position = self.identify_strong_limit(self.coupling_obs_lower, self.coupling_MB_obs)
                coupling_in = self.model_coupling_calc(position)
                obs = self.get_limit_from_data(coupling_in, position, self.coupling_obs_lower, self.coupling_MB_obs)
                exp = self.get_limit_from_data(coupling_in, position, self.coupling_exp_lower, self.coupling_MB_exp)
                self._obs_ratio, self._exp_ratio = obs_exp_ratio_calc(coupling_in, obs, exp)
                self.set_result(position)
                return self._result, self._obs_ratio, self._exp_ratio, self._channel
            elif self.m.model() == 'Doublet':
                position = self.identify_strong_limit(self.coupling_obs_lower, self.coupling_MB_obs)
                coupling_in = self.model_coupling_calc(position)
                obs = self.get_limit_from_data(coupling_in, position, self.coupling_obs_lower, self.coupling_MB_obs)
                exp = self.get_limit_from_data(coupling_in, position, self.coupling_exp_lower, self.coupling_MB_exp)
                self._obs_ratio, self._exp_ratio = obs_exp_ratio_calc(coupling_in, obs, exp)
                self.set_result(position)
                return self._result, self._obs_ratio, self._exp_ratio, self._channel
            else:
                raise Exception("Error. There are no coupling limits for this model")
        elif self.VLX:
            position = self.identify_strong_limit(self.coupling_obs_lower, self.coupling_MX_obs)
            coupling_in = self.model_coupling_calc(position)
            obs = self.get_limit_from_data(coupling_in, position, self.coupling_obs_lower, self.coupling_MX_obs)
            exp = self.get_limit_from_data(coupling_in, position, self.coupling_exp_lower, self.coupling_MX_exp)
            self._obs_ratio, self._exp_ratio = obs_exp_ratio_calc(coupling_in, obs, exp)
            self.set_result(position)
            return self._result, self._obs_ratio, self._exp_ratio, self._channel
        elif self.VLY:
            position = self.identify_strong_limit(self.coupling_obs_lower, self.coupling_MY_obs)
            coupling_in = self.model_coupling_calc(position)
            obs = self.get_limit_from_data(coupling_in, position, self.coupling_obs_lower, self.coupling_MY_obs)
            exp = self.get_limit_from_data(coupling_in, position, self.coupling_exp_lower, self.coupling_MY_exp)
            self._obs_ratio, self._exp_ratio = obs_exp_ratio_calc(coupling_in, obs, exp)
            self.set_result(position)
            return self._result, self._obs_ratio, self._exp_ratio, self._channel
        else:
            if self.m.model() == 'Singlet':
                position = self.identify_strong_limit(self.coupling_obs_lower, self.coupling_MT_obs)
                if self.coupling_key[position] in self.k_keys or self.coupling_key[position] in self.sin_l_keys:
                    coupling_in = self.model_coupling_calc(position)
                    obs_lower_branch = self.get_limit_from_data(coupling_in, position,
                                                                self.coupling_obs_lower, self.coupling_MT_obs)

                    exp_lower_branch = self.get_limit_from_data(coupling_in, position,
                                                                self.coupling_exp_lower, self.coupling_MT_exp)

                    self._obs_ratio, self._exp_ratio = (
                        obs_exp_ratio_calc(coupling_in, obs_lower_branch, exp_lower_branch))

                    self.result_based_on_branches(position, position, coupling_in, obs_lower_branch)

                else:
                    raise Exception(f"The coupling key {self.coupling_key[position]} is not found in kappa, "
                                    f"sin_left and width ratio keys")
                return self._result, self._obs_ratio, self._exp_ratio, self._channel

            elif self.m.model() == 'Doublet':
                position = self.identify_strong_limit(self.coupling_obs_lower, self.coupling_MT_obs)
                if self.coupling_key[position] in self.k_keys:
                    coupling_in = self.model_coupling_calc(position)
                    obs = self.get_limit_from_data(coupling_in, position,
                                                   self.coupling_obs_lower,
                                                   self.coupling_MT_obs)
                    exp = self.get_limit_from_data(coupling_in, position,
                                                   self.coupling_exp_lower,
                                                   self.coupling_MT_exp)
                    self._obs_ratio, self._exp_ratio = obs_exp_ratio_calc(coupling_in, obs, exp)
                    self.set_result(position)
                else:
                    raise Exception(f"The coupling key {self.coupling_key[position]} "
                                    f"is not found in kappa or width keys.")
                return self._result, self._obs_ratio, self._exp_ratio, self._channel
            else:
                raise Exception("Error. There are no coupling limits for this model")

    def check_xs_and_coupling_limits(self):
        coupling_res, coupling_obs_ratio, coupling_exp_ratio, coupling_channel = self.coupling_limit()
        xs_res, xs_obs_ratio, xs_exp_ratio, xs_channel = self.check_channel()
        xs_is_stronger = biggest_ratio(coupling_obs_ratio, xs_obs_ratio)
        if xs_is_stronger:
            self._result = xs_res
            self._obs_ratio = xs_obs_ratio
            self._exp_ratio = xs_exp_ratio
            self._channel = xs_channel
        else:
            self._result = coupling_res
            self._obs_ratio = coupling_obs_ratio
            self._exp_ratio = coupling_exp_ratio
            if coupling_channel != -1:
                self._channel = coupling_channel + len(self.key)
            else:
                self._channel = coupling_channel
            self.most_sensitive_channels.append(self._channel)

    def all_couplings(self):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'keys', 'coupling_info.dat'))
        with open(file_path, "w") as f:
            f.write("************* File for each coupling limit information*****************\n")
            f.write("This File has been generated with VLQBounds version 0.1\n")
            f.write(f"With the {type(self.m).__name__[-1]} quark in the {self.m.model()} scenario\n")
            for i, proc in enumerate(self.coupling_process):
                f.write("***********************************************************************\n")
                f.write(f"channel {i}:\n")
                f.write(f"{proc} \t\t {self.coupling_label[i]} ({self.coupling_expt[i]}) "
                        f"\t sqrt(s) = {self.coupling_energy[i]} TeV\t "
                        f"luminosity = {self.coupling_luminosity[i]} fb-1\n")

    def coupling_and_xs_info(self):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'keys', 'coupling_and_xs_info.dat'))
        with open(file_path, "w") as f:
            f.write("************* cross section limit information *****************\n")
            f.write("This File has been generated with VLQBounds version 0.1\n")

            f.write(f"With the {type(self.m).__name__[-1]} quark in the {self.m.model()} scenario\n")
            for i, proc in enumerate(self.process):
                f.write("***********************************************************************\n")
                f.write(f"channel {i}:\n")
                f.write(f"{proc} \t\t {self.label[i]} ({self.expt[i]}) "
                        f"\t sqrt(s) = {self.energy[i]} TeV\t luminosity = {self.luminosity[i]} fb-1\n")
            f.write("************* Coupling limits information part   *****************\n")
            f.write(f" quark {type(self.m).__name__[-1]} in the {self.m.model()} scenario\n")
            for i, proc in enumerate(self.coupling_process):
                f.write("***********************************************************************\n")
                f.write(f"channel {i + len(self.key)}:\n")
                f.write(f"{proc} \t\t {self.coupling_label[i]} ({self.coupling_expt[i]}) "
                        f"\t sqrt(s) = {self.coupling_energy[i]} TeV\t "
                        f"luminosity = {self.coupling_luminosity[i]} fb-1\n")

    def get_sensitive_limits_info(self):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'keys', 'channels_key.dat'))
        with open(file_path, "w") as f:
            f.write("************* selected limits *****************\n")
            f.write("This File has been generated with VLQBounds version 0.1\n")
            f.write(f"With the {type(self.m).__name__[-1]} quark in the {self.m.model()} scenario\n")
            high_sensitivity_channels = np.unique(self.most_sensitive_channels)
            for i in high_sensitivity_channels[high_sensitivity_channels != -1]:
                f.write("***********************************************************************\n")
                if i >= len(self.key):
                    f.write(f"channel {i}:\n")
                    f.write(
                        f"{self.coupling_process[i - len(self.key)]} \t\t "
                        f"{self.coupling_label[i - len(self.key)]} "
                        f"({self.coupling_expt[i - len(self.key)]}) "
                        f"\t sqrt(s) = {self.coupling_energy[i - len(self.key)]} TeV\t "
                        f"luminosity = {self.coupling_luminosity[i - len(self.key)]} fb-1\n")
                else:
                    f.write(f"channel {i}:\n")
                    f.write(
                        f"{self.process[i]} \t\t "
                        f"{self.label[i]} "
                        f"({self.expt[i]}) "
                        f"\t sqrt(s) = {self.energy[i]} TeV\t "
                        f"luminosity = {self.luminosity[i]} fb-1\n")

    def fill_sin_and_kappa(self):
        if self.VLB:
            if self.m.model() == 'Singlet':
                self.k_keys = [
                    self.coupling_key[j]
                    for j, coupling in enumerate(self.which_coupling)
                    if coupling == 'k_B'
                ]

                self.sin_l_keys = [
                    self.coupling_key[j]
                    for j, coupling in enumerate(self.which_coupling)
                    if coupling == "s_l"
                ]
            else:
                self.k_keys = [
                    self.coupling_key[j]
                    for j, coupling in enumerate(self.which_coupling)
                    if coupling == 'k_B'
                ]

        elif self.VLX:
            self.k_keys = [
                self.coupling_key[j]
                for j, coupling in enumerate(self.which_coupling)
                if coupling == 'k_x'
            ]
        elif self.VLY:
            self.k_keys = [
                self.coupling_key[j]
                for j, coupling in enumerate(self.which_coupling)
                if coupling == 'k_y'
            ]
            self.sin_l_keys = [
                self.coupling_key[j]
                for j, coupling in enumerate(self.which_coupling)
                if coupling == 's_d_l'
            ]

        else:
            self.sin_l_keys = [
                self.coupling_key[j]
                for j, coupling in enumerate(self.which_coupling)
                if coupling == 's_l'
            ]
            self.k_keys = [
                self.coupling_key[j]
                for j, coupling in enumerate(self.which_coupling)
                if coupling == 'k_T'
            ]

    def coupling_factor_to_coupling_strength(self, vlq='T'):
        for file in self.coupling_file_name:
            if 'cf' in file:
                j = self.coupling_file_name.index(file)
                if vlq == 'T':
                    self.coupling_obs_lower[j] = from_cf_to_kappa(self.coupling_obs_lower[j],
                                                                  self.coupling_MT_obs[j],
                                                                  self.m.model()
                                                                  )
                    self.coupling_exp_lower[j] = from_cf_to_kappa(self.coupling_exp_lower[j],
                                                                  self.coupling_MT_exp[j],
                                                                  self.m.model()
                                                                  )

                elif vlq == 'B':
                    self.coupling_obs_lower[j] = from_cf_to_kappa(self.coupling_obs_lower[j],
                                                                  self.coupling_MB_obs[j],
                                                                  self.m.model())

                    self.coupling_exp_lower[j] = from_cf_to_kappa(self.coupling_exp_lower[j],
                                                                  self.coupling_MB_exp[j],
                                                                  self.m.model())

