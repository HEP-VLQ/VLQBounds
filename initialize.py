from utils import load_data_from_files
from vector_like_T import *
from vector_like_B import *


class Tables:
    def __init__(self, m):
        self.cs_keys = {}
        self.TB_XT_keys = {}
        self.VLB = False
        self.m = m
        self.initialize_bounds_arrays()

    def bounds_properties_arrays(self, number_of_atlas_cms_tables):
        self.file_name = [None] * number_of_atlas_cms_tables
        self.key = [None] * number_of_atlas_cms_tables
        self.label = [None] * number_of_atlas_cms_tables
        self.expt = [None] * number_of_atlas_cms_tables
        self.process = [None] * number_of_atlas_cms_tables
        self.energy = [None] * number_of_atlas_cms_tables
        self.luminosity = [None] * number_of_atlas_cms_tables
        self.obs = [None] * number_of_atlas_cms_tables
        self.exp = [None] * number_of_atlas_cms_tables
        if isinstance(self.m, (SingletT, PureTDecay)):
            self.MT = [None] * number_of_atlas_cms_tables
        elif isinstance(self.m, DoubletT):
            self.which_doublet = [None] * number_of_atlas_cms_tables
            self.MT = [None] * number_of_atlas_cms_tables
        elif isinstance(self.m, (SingletB, PureBDecay)):
            self.MB = [None] * number_of_atlas_cms_tables
        elif isinstance(self.m, DoubletB):
            self.which_doublet = [None] * number_of_atlas_cms_tables
            self.MB = [None] * number_of_atlas_cms_tables

    def get_number_of_cms_atlas_tables(self, vlq='T'):
        if vlq == 'B':
            if self.m.model() == 'Singlet':
                return 24
            elif self.m.model() == 'Doublet':
                return 22
            else:
                return 17
        else:
            if self.m.model() == 'Singlet':
                return 59
            elif self.m.model() == 'Doublet':
                return 33
            else:
                return 25

    def initialize_bounds_arrays(self):
        if isinstance(self.m, (SingletB, DoubletB)):
            number_of_atlas_cms_tables = self.get_number_of_cms_atlas_tables(vlq='B')
            if number_of_atlas_cms_tables > 0:
                self.bounds_properties_arrays(number_of_atlas_cms_tables)
        else:
            number_of_atlas_cms_tables = self.get_number_of_cms_atlas_tables()
            if number_of_atlas_cms_tables > 0:
                self.bounds_properties_arrays(number_of_atlas_cms_tables)


    def initialize_tables_cms_and_atlas(self):
        """" fills experimental data from files """
        if self.VLB:
            if self.m.model() == 'Singlet':
                self.key[0] = '01762fb'
                self.label[0] = 'arXiv:1806.01762'
                self.expt[0] = 'ATLAS'
                self.file_name[0] = '1806.01762_ATLAS_fig4b_pp_BB_Wt_singlet.dat'
                self.process[0] = 'pp --> BB'
                self.energy[0] = 13
                self.luminosity[0] = 36.1

                self.key[1] = '10555f13b'
                self.label[1] = 'arXiv:1806.10555'
                self.expt[1] = 'ATLAS'
                self.file_name[1] = '1806.10555_ATLAS_fig13b_pp_BB_Zb_singlet.dat'
                self.process[1] = 'pp --> BB'
                self.energy[1] = 13
                self.luminosity[1] = 36.1

                self.key[2] = '15413f7b'
                self.label[2] = 'arXiv:2210.15413'
                self.expt[2] = 'ATLAS'
                self.file_name[2] = '2210.15413_ATLAS_fig7b_pp_BB_Zb_singlet.dat'
                self.process[2] = 'pp --> BB'
                self.energy[2] = 13
                self.luminosity[2] = 139

                self.key[3] = '05263f7d'
                self.label[3] = 'arXiv:2212.05263'
                self.expt[3] = 'ATLAS'
                self.file_name[3] = '2212.05263_ATLAS_fig7d_pp_BB_Wt_singlet.dat'
                self.process[3] = 'pp --> BB'
                self.energy[3] = 13
                self.luminosity[3] = 139

                self.key[4] = '01486Fig6a'
                self.label[4] = 'arXiv:1802.01486'
                self.expt[4] = 'CMS'
                self.file_name[4] = '1802.01486_Fig6a_CMS_upper_left_pp_B_bH_Gamma_M1_singlet_or_doublet.dat'
                self.process[4] = 'pp --> Bbq --> bHbq'
                self.energy[4] = 13
                self.luminosity[4] = 35.9

                self.key[5] = '01486Fig6b'
                self.label[5] = 'arXiv:1802.01486'
                self.expt[5] = 'CMS'
                self.file_name[5] = '1802.01486_Fig6b_CMS_upper_right_pp_B_bH_Gamma_M10_singlet_or_doublet.dat'
                self.process[5] = 'pp --> Bbq --> bHbq'
                self.energy[5] = 13
                self.luminosity[5] = 35.9

                self.key[6] = '01486Fig6c'
                self.label[6] = 'arXiv:1802.01486'
                self.expt[6] = 'CMS'
                self.file_name[6] = '1802.01486_Fig6c_CMS_lower_left_pp_B_bH_Gamma_M20_singlet_or_doublet.dat'
                self.process[6] = 'pp --> Bbq --> bHbq'
                self.energy[6] = 13
                self.luminosity[6] = 35.9

                self.key[7] = '01486Fig6d'
                self.label[7] = 'arXiv:1802.01486'
                self.expt[7] = 'CMS'
                self.file_name[7] = '1802.01486_Fig6d_CMS_lower_right_pp_B_bH_Gamma_M30_singlet_or_doublet.dat'
                self.process[7] = 'pp --> Bbq --> bHbq'
                self.energy[7] = 13
                self.luminosity[7] = 35.9

                self.key[8] = '04758f8ll'
                self.label[8] = 'arXiv:1805.04758'
                self.expt[8] = 'CMS'
                self.file_name[8] = '1805.04758_CMS_Fig8_lower_left_singlet.dat'
                self.process[8] = 'pp --> BB'
                self.energy[8] = 13
                self.luminosity[8] = 35.9

                self.key[8] = '04758f8ll'
                self.label[8] = 'arXiv:1805.04758'
                self.expt[8] = 'CMS'
                self.file_name[8] = '1805.04758_CMS_Fig8_lower_left_singlet.dat'
                self.process[8] = 'pp --> BB'
                self.energy[8] = 13
                self.luminosity[8] = 35.9

                self.key[9] = '07327f9c'
                self.label[9] = 'arXiv:2209.07327'
                self.expt[9] = 'CMS'
                self.file_name[9] = '2209.07327_CMS_f9c_pp_BB_singlet.dat'
                self.process[9] = 'pp --> BB'
                self.energy[9] = 13
                self.luminosity[9] = 138

                self.key[10] = '5500f12a'
                self.label[10] = 'arXiv:1409.5500'
                self.expt[10] = 'ATLAS'
                self.file_name[10] = '1409.5500_ATLAS_Fig12a_pp_BB_singlet.dat'
                self.process[10] = 'pp --> BB'
                self.energy[10] = 8
                self.luminosity[10] = 20.3

                self.key[11] = '05425f8'
                self.label[11] = 'arXiv:1503.05425'
                self.expt[11] = 'ATLAS'
                self.file_name[11] = '1503.05425_ATLAS_Fig8_pp_BB_Wt_Zb_HB_singlet.dat'
                self.process[11] = 'pp --> BB'
                self.energy[11] = 8
                self.luminosity[11] = 20.3

                self.key[12] = '04605f7a'
                self.label[12] = 'arXiv:1504.04605'
                self.expt[12] = 'ATLAS'
                self.file_name[12] = '1504.04605_ATLAS_Fig7a_pp_BB_singlet.dat'
                self.process[12] = 'pp --> BB'
                self.energy[12] = 8
                self.luminosity[12] = 20.3

                self.key[13] = '04306f22b'
                self.label[13] = 'arXiv:1505.04306'
                self.expt[13] = 'ATLAS'
                self.file_name[13] = '1505.04306_ATLAS_Fig22b_pp_BB_Hb_singlet.dat'
                self.process[13] = 'pp --> BB'
                self.energy[13] = 8
                self.luminosity[13] = 20.3

                self.key[14] = '02343f3a'
                self.label[14] = 'arXiv:1808.02343'
                self.expt[14] = 'ATLAS'
                self.file_name[14] = '1808.02343_ATLAS_Fig3a_pp_BB_singlet.dat'
                self.process[14] = 'pp --> BB'
                self.energy[14] = 13
                self.luminosity[14] = 36.1

                self.key[15] = '02595f8a'
                self.label[15] = 'arXiv:2308.02595'
                self.expt[15] = 'ATLAS'
                self.file_name[15] = '2308.02595_ATLAS_Fig8a_pp_B_bH_k03_singlet.dat'
                self.process[15] = 'pp --> Bb(t)q --> bHb(t)q'
                self.energy[15] = 13
                self.luminosity[15] = 139

                self.key[16] = '02595f8c'
                self.label[16] = 'arXiv:2308.02595'
                self.expt[16] = 'ATLAS'
                self.file_name[16] = '2308.02595_ATLAS_Fig8c_pp_B_bH_k04_singlet.dat'
                self.process[16] = 'pp --> Bb(t)q --> bHb(t)q'
                self.energy[16] = 13
                self.luminosity[16] = 139

                self.key[17] = '02595f8e'
                self.label[17] = 'arXiv:2308.02595'
                self.expt[17] = 'ATLAS'
                self.file_name[17] = '2308.02595_ATLAS_Fig8e_pp_B_bH_k05_singlet.dat'
                self.process[17] = 'pp --> Bb(t)q --> bHb(t)q'
                self.energy[17] = 13
                self.luminosity[17] = 139

                self.key[18] = '07409f5l'
                self.label[18] = 'arXiv:1701.07409'
                self.expt[18] = 'CMS'
                self.file_name[18] = '1701.07409_CMS_Fig5_left_pp_Bt_bZ_cWt05_singlet.dat'
                self.process[18] = 'pp --> Btq --> bZtq'
                self.energy[18] = 13
                self.luminosity[18] = 2.3

                self.key[19] = '07409f5r'
                self.label[19] = 'arXiv:1701.07409'
                self.expt[19] = 'CMS'
                self.file_name[19] = '1701.07409_CMS_Fig5_right_pp_Bb_bZ_cbZ05_singlet.dat'
                self.process[19] = 'pp --> Bbq --> bZbq'
                self.energy[19] = 13
                self.luminosity[19] = 2.3

                self.key[20] = '03408f13l'
                self.label[20] = 'arXiv:1706.03408'
                self.expt[20] = 'CMS'
                self.file_name[20] = '1706.03408_CMS_Fig13_left_pp_BB_singlet.dat'
                self.process[20] = 'pp --> BB'
                self.energy[20] = 13
                self.luminosity[20] = 2.6

                self.key[21] = '10216f4l'
                self.label[21] = 'arXiv:2111.10216'
                self.expt[21] = 'CMS'
                self.file_name[21] = '2111.10216_CMS_Fig4_left_pp_B_Wt_singlet_doublet.dat'
                self.process[21] = 'pp --> Bbq --> tWbq'
                self.energy[21] = 13
                self.luminosity[21] = 138

                self.key[22] = '10216f4r'
                self.label[22] = 'arXiv:2111.10216'
                self.expt[22] = 'CMS'
                self.file_name[22] = '2111.10216_CMS_Fig4_right_pp_B_Wt_singlet_doublet.dat'
                self.process[22] = 'pp --> Btq --> tWtq'
                self.energy[22] = 13
                self.luminosity[22] = 138

                self.key[23] = '17605f39ll'
                self.label[23] = 'arXiv:2405.17605'
                self.expt[23] = 'CMS'
                self.file_name[23] = '2405.17605_CMS_Fig39_lower_left_pp_BB_singlet.dat'
                self.process[23] = 'pp --> BB'
                self.energy[23] = 13
                self.luminosity[23] = 138

                load_data_from_files(self.file_name, len(self.key), self.MB, self.exp, self.obs, self.expt, vlq='B')

            elif self.m.model() == 'Doublet':
                self.key[0] = '10555f13d'
                self.label[0] = 'arXiv:1806.10555'
                self.expt[0] = 'ATLAS'
                self.file_name[0] = '1806.10555_ATLAS_fig13d_pp_BB_BY_doublet.dat'
                self.process[0] = 'pp --> BB'
                self.energy[0] = 13
                self.luminosity[0] = 36.1
                self.which_doublet[0] = 'BY'

                self.key[1] = '01771f13c'
                self.label[1] = 'arXiv:1808.01771'
                self.expt[1] = 'ATLAS'
                self.file_name[1] = '1808.01771_ATLAS_fig13c_pp_BB_BY_doublet.dat'
                self.process[1] = 'pp --> BB'
                self.energy[1] = 13
                self.luminosity[1] = 36.1
                self.which_doublet[1] = 'BY'

                self.key[2] = '15413f7d'
                self.label[2] = 'arXiv:2210.15413'
                self.expt[2] = 'ATLAS'
                self.file_name[2] = '2210.15413_ATLAS_fig7d_pp_BB_BY_doublet.dat'
                self.process[2] = 'pp --> BB'
                self.energy[2] = 13
                self.luminosity[2] = 139
                self.which_doublet[2] = 'BY'

                self.key[3] = '05263f7f'
                self.label[3] = 'arXiv:2212.05263'
                self.expt[3] = 'ATLAS'
                self.file_name[3] = '2212.05263_ATLAS_fig7b_pp_BB_BYorTB_doublet.dat'
                self.process[3] = 'pp --> BB'
                self.energy[3] = 13
                self.luminosity[3] = 139
                self.which_doublet[3] = 'BYorTB'

                self.key[4] = '05263f7f'
                self.label[4] = 'arXiv:2212.05263'
                self.expt[4] = 'ATLAS'
                self.file_name[4] = '2212.05263_ATLAS_fig7f_pp_QQ_mass_degenerate_BYorTB_doublet.dat'
                self.process[4] = 'pp --> BB'
                self.energy[4] = 13
                self.luminosity[4] = 139
                self.which_doublet[4] = 'BYorTB'

                self.key[5] = '01486Fig6a'
                self.label[5] = 'arXiv:1802.01486'
                self.expt[5] = 'CMS'
                self.file_name[5] = '1802.01486_Fig6a_CMS_upper_left_pp_B_bH_Gamma_M1_singlet_or_doublet.dat'
                self.process[5] = 'pp --> Bbq --> bHbq'
                self.energy[5] = 13
                self.luminosity[5] = 35.9
                self.which_doublet[5] = 'BYorTB'

                self.key[6] = '01486Fig6b'
                self.label[6] = 'arXiv:1802.01486'
                self.expt[6] = 'CMS'
                self.file_name[6] = '1802.01486_Fig6b_CMS_upper_right_pp_B_bH_Gamma_M10_singlet_or_doublet.dat'
                self.process[6] = 'pp --> Bbq --> bHbq'
                self.energy[6] = 13
                self.luminosity[6] = 35.9
                self.which_doublet[6] = 'BYorTB'

                self.key[7] = '01486Fig6c'
                self.label[7] = 'arXiv:1802.01486'
                self.expt[7] = 'CMS'
                self.file_name[7] = '1802.01486_Fig6c_CMS_lower_left_pp_B_bH_Gamma_M20_singlet_or_doublet.dat'
                self.process[7] = 'pp --> Bbq --> bHbq'
                self.energy[7] = 13
                self.luminosity[7] = 35.9
                self.which_doublet[7] = 'BYorTB'

                self.key[8] = '01486Fig6d'
                self.label[8] = 'arXiv:1802.01486'
                self.expt[8] = 'CMS'
                self.file_name[8] = '1802.01486_Fig6d_CMS_lower_right_pp_B_bH_Gamma_M30_singlet_or_doublet.dat'
                self.process[8] = 'pp --> Bbq --> bHbq'
                self.energy[8] = 13
                self.luminosity[8] = 35.9
                self.which_doublet[8] = 'BYorTB'

                self.key[9] = '04758Fig8lr'
                self.label[9] = 'arXiv:1805.04758'
                self.expt[9] = 'CMS'
                self.file_name[9] = '1805.04758_CMS_Fig8_lower_right_pp_BB_doublet.dat'
                self.process[9] = 'pp --> BB'
                self.energy[9] = 13
                self.luminosity[9] = 35.9
                self.which_doublet[9] = 'BYorTB'

                self.key[10] = '09768Fig7ur'
                self.label[10] = 'arXiv:1812.09768'
                self.expt[10] = 'CMS'
                self.file_name[10] = '1812.09768_CMS_Fig7_upper_right_pp_BB_doublet.dat'
                self.process[10] = 'pp --> BB'
                self.energy[10] = 13
                self.luminosity[10] = 35.9
                self.which_doublet[10] = 'BYorTB'

                self.key[11] = '09835Fig11l'
                self.label[11] = 'arXiv:2008.09835'
                self.expt[11] = 'CMS'
                self.file_name[11] = '2008.09835_CMS_Fig11_lower_pp_BB_doublet.dat'
                self.process[11] = 'pp --> BB'
                self.energy[11] = 13
                self.luminosity[11] = 137
                self.which_doublet[11] = 'BYorTB'

                self.key[12] = '07327f9d'
                self.label[12] = 'arXiv:2209.07327'
                self.expt[12] = 'CMS'
                self.file_name[12] = '2209.07327_CMS_f9d_pp_BB_doublet.dat'
                self.process[12] = 'pp --> BB'
                self.energy[12] = 13
                self.luminosity[12] = 137
                self.which_doublet[12] = 'BYorTB'

                self.key[13] = '02343f3b'
                self.label[13] = 'arXiv:1808.02343'
                self.expt[13] = 'ATLAS'
                self.file_name[13] = '1808.02343_ATLAS_Fig3b_pp_BB_TB_doublet.dat'
                self.process[13] = 'pp --> BB'
                self.energy[13] = 13
                self.luminosity[13] = 36.1
                self.which_doublet[13] = 'TB'

                self.key[14] = '02343f3c'
                self.label[14] = 'arXiv:1808.02343'
                self.expt[14] = 'ATLAS'
                self.file_name[14] = '1808.02343_ATLAS_Fig3c_pp_BB_BY_doublet.dat'
                self.process[14] = 'pp --> BB'
                self.energy[14] = 13
                self.luminosity[14] = 36.1
                self.which_doublet[14] = 'BY'

                self.key[15] = '02595f8b'
                self.label[15] = 'arXiv:2308.02595'
                self.expt[15] = 'ATLAS'
                self.file_name[15] = '2308.02595_ATLAS_Fig8b_pp_B_bH_k03_BY_doublet.dat'
                self.process[15] = 'pp --> Bb(t)q --> bHb(t)q'
                self.energy[15] = 13
                self.luminosity[15] = 139
                self.which_doublet[15] = 'BY'

                self.key[16] = '02595f8d'
                self.label[16] = 'arXiv:2308.02595'
                self.expt[16] = 'ATLAS'
                self.file_name[16] = '2308.02595_ATLAS_Fig8d_pp_B_bH_k04_BY_doublet.dat'
                self.process[16] = 'pp --> Bb(t)q --> bHb(t)q'
                self.energy[16] = 13
                self.luminosity[16] = 139
                self.which_doublet[16] = 'BY'

                self.key[17] = '02595f8f'
                self.label[17] = 'arXiv:2308.02595'
                self.expt[17] = 'ATLAS'
                self.file_name[17] = '2308.02595_ATLAS_Fig8f_pp_B_bH_k05_BY_doublet.dat'
                self.process[17] = 'pp --> Bb(t)q --> bHb(t)q'
                self.energy[17] = 13
                self.luminosity[17] = 139
                self.which_doublet[17] = 'BY'

                self.key[18] = '03408f13r'
                self.label[18] = 'arXiv:1706.03408'
                self.expt[18] = 'CMS'
                self.file_name[18] = '1706.03408_CMS_Fig13_right_pp_BB_doublet.dat'
                self.process[18] = 'pp --> BB'
                self.energy[18] = 13
                self.luminosity[18] = 2.6
                self.which_doublet[18] = 'BYorTB'

                self.key[19] = '13808f18ll'
                self.label[19] = 'arXiv:2402.13808'
                self.expt[19] = 'CMS'
                self.file_name[19] = '2402.13808_CMS_Fig18_lower_left_pp_BB_TB_doublet.dat'
                self.process[19] = 'pp --> BB'
                self.energy[19] = 13
                self.luminosity[19] = 138
                self.which_doublet[19] = 'TB'

                self.key[20] = '10216f4ld'
                self.label[20] = 'arXiv:2111.10216'
                self.expt[20] = 'CMS'
                self.file_name[20] = '2111.10216_CMS_Fig4_left_pp_B_Wt_singlet_doublet.dat'
                self.process[20] = 'pp --> Bbq --> tWbq'
                self.energy[20] = 13
                self.luminosity[20] = 138
                self.which_doublet[20] = 'BYorTB'

                self.key[21] = '17605f39lr'
                self.label[21] = 'arXiv:2405.17605'
                self.expt[21] = 'CMS'
                self.file_name[21] = '2405.17605_CMS_Fig39_lower_right_pp_BB_doublet.dat'
                self.process[21] = 'pp --> BB'
                self.energy[21] = 13
                self.luminosity[21] = 138
                self.which_doublet[21] = 'BYorTB'

                load_data_from_files(self.file_name, len(self.key), self.MB, self.exp, self.obs, self.expt, vlq='B')
            elif self.m.model() == 'Pure':
                self.key[0] = '01762f4a'
                self.label[0] = 'arXiv:1806.01762'
                self.expt[0] = 'ATLAS'
                self.file_name[0] = '1806.01762_ATLAS_fig4a_pp_BB_Wt.dat'
                self.process[0] = 'pp --> BB'
                self.energy[0] = 13
                self.luminosity[0] = 36.1

                self.key[1] = '10555f13f'
                self.label[1] = 'arXiv:1806.10555'
                self.expt[1] = 'ATLAS'
                self.file_name[1] = '1806.10555_ATLAS_fig13f_pp_BB_bZ.dat'
                self.process[1] = 'pp --> BB'
                self.energy[1] = 13
                self.luminosity[1] = 36.1

                self.key[2] = '01771fig13b'
                self.label[2] = 'arXiv:1808.01771'
                self.expt[2] = 'ATLAS'
                self.file_name[2] = '1808.01771_ATLAS_fig13b_pp_BB_Hb.dat'
                self.process[2] = 'pp --> BB'
                self.energy[2] = 13
                self.luminosity[2] = 36.1

                self.key[3] = '15413fig7f'
                self.label[3] = 'arXiv:2210.15413'
                self.expt[3] = 'ATLAS'
                self.file_name[3] = '2210.15413_ATLAS_fig7f_pp_BB_Zb.dat'
                self.process[3] = 'pp --> BB'
                self.energy[3] = 13
                self.luminosity[3] = 139

                self.key[4] = '09768fig7ul'
                self.label[4] = 'arXiv:1812.09768'
                self.expt[4] = 'CMS'
                self.file_name[4] = '1812.09768_Fig7_upper_left_pp_BB_bZ.dat'
                self.process[4] = 'pp --> BB'
                self.energy[4] = 13
                self.luminosity[4] = 35.9

                self.key[5] = '09768fig7ur'
                self.label[5] = 'arXiv:1812.09768'
                self.expt[5] = 'CMS'
                self.file_name[5] = '1812.09768_Fig7_upper_right_pp_BB_doublet.dat'
                self.process[5] = 'pp --> BB'
                self.energy[5] = 13
                self.luminosity[5] = 35.9

                self.key[6] = '09835fig11ul'
                self.label[6] = 'arXiv:2008.09835'
                self.expt[6] = 'CMS'
                self.file_name[6] = '2008.09835_CMS_fig11_upper_left_pp_BB_bH.dat'
                self.process[6] = 'pp --> BB'
                self.energy[6] = 13
                self.luminosity[6] = 137

                self.key[7] = '09835fig11ur'
                self.label[7] = 'arXiv:2008.09835'
                self.expt[7] = 'CMS'
                self.file_name[7] = '2008.09835_CMS_fig11_upper_right_pp_BB_bZ.dat'
                self.process[7] = 'pp --> BB'
                self.energy[7] = 13
                self.luminosity[7] = 137

                self.key[8] = '1265f5'
                self.label[8] = 'arXiv:1204.1265'
                self.expt[8] = 'ATLAS'
                self.file_name[8] = '1204.1265_ATLAS_Fig5_pp_BB_Zb.dat'
                self.process[8] = 'pp --> BB'
                self.energy[8] = 13
                self.luminosity[8] = 137

                self.key[9] = '04605f6a'
                self.label[9] = 'arXiv:1504.04605'
                self.expt[9] = 'ATLAS'
                self.file_name[9] = '1504.04605_ATLAS_Fig6a_pp_BB_Wt.dat'
                self.process[9] = 'pp --> BB'
                self.energy[9] = 8
                self.luminosity[9] = 20.3

                self.key[10] = '04306f22a'
                self.label[10] = 'arXiv:1505.04306'
                self.expt[10] = 'ATLAS'
                self.file_name[10] = '1505.04306_ATLAS_Fig22a_pp_BB_Hb.dat'
                self.process[10] = 'pp --> BB'
                self.energy[10] = 8
                self.luminosity[10] = 20.3

                self.key[11] = '13808f18ul'
                self.label[11] = 'arXiv:2402.13808'
                self.expt[11] = 'ATLAS'
                self.file_name[11] = '2402.13808_CMS_Fig18_upper_left_pp_BB_bH.dat'
                self.process[11] = 'pp --> BB'
                self.energy[11] = 13
                self.luminosity[11] = 138

                self.key[12] = '13808f18ur'
                self.label[12] = 'arXiv:2402.13808'
                self.expt[12] = 'ATLAS'
                self.file_name[12] = '2402.13808_CMS_Fig18_upper_right_pp_BB_bZ.dat'
                self.process[12] = 'pp --> BB'
                self.energy[12] = 13
                self.luminosity[12] = 138

                self.key[13] = '07129f13l'
                self.label[13] = 'arXiv:1507.07129'
                self.expt[13] = 'CMS'
                self.file_name[13] = '1507.07129_Fig13_left_pp_BB_Wt.dat'
                self.process[13] = 'pp --> BB'
                self.energy[13] = 8
                self.luminosity[13] = 19.7

                self.key[14] = '07129f13m'
                self.label[14] = 'arXiv:1507.07129'
                self.expt[14] = 'CMS'
                self.file_name[14] = '1507.07129_Fig13_middle_pp_BB_bZ.dat'
                self.process[14] = 'pp --> BB'
                self.energy[14] = 8
                self.luminosity[14] = 19.7

                self.key[15] = '07129f13r'
                self.label[15] = 'arXiv:1507.07129'
                self.expt[15] = 'CMS'
                self.file_name[15] = '1507.07129_Fig13_right_pp_BB_bH.dat'
                self.process[15] = 'pp --> BB'
                self.energy[15] = 8
                self.luminosity[15] = 19.7

                self.key[16] = '17605f38l'
                self.label[16] = 'arXiv:2405.17605'
                self.expt[16] = 'CMS'
                self.file_name[16] = '2405.17605_CMS_Fig38_lower_pp_BB_tW.dat'
                self.process[16] = 'pp --> BB'
                self.energy[16] = 8
                self.luminosity[16] = 19.7

        else:
            if self.m.model() == 'Singlet':
                self.key[0] = '10751fig6b'
                self.label[0] = 'arXiv:1705.10751'
                self.expt[0] = 'ATLAS'
                self.file_name[0] = '1705.10751_ATLAS_fig6b_pp_TT_Zt_Singlet.txt'
                self.process[0] = 'pp --> TT'
                self.energy[0] = 13
                self.luminosity[0] = 36.1

                self.key[1] = '73270'
                self.label[1] = 'arXiv:2209.07327'
                self.expt[1] = 'CMS'
                self.file_name[1] = '2209.07327_CMS_f9a_pp_TTbar_Singlet.txt'
                self.process[1] = 'pp --> TT'
                self.energy[1] = 13
                self.luminosity[1] = 138

                self.key[2] = '33470fig4b'
                self.label[2] = 'arXiv:1707.03347'
                self.expt[2] = 'ATLAS'
                self.file_name[2] = '1707.03347_ATLAS_fig4b_pp_TT_Singlet.txt'
                self.process[2] = 'pp --> TT'
                self.energy[2] = 13
                self.luminosity[2] = 36.1

                self.key[3] = '05263'
                self.label[3] = 'arXiv:2212.05263'
                self.expt[3] = 'ATLAS'
                self.file_name[3] = '2212.05263_ATLAS_fig7c_pp_TT_Zt_Singlet.txt'
                self.process[3] = 'pp --> TT'
                self.energy[3] = 13
                self.luminosity[3] = 139

                self.key[4] = '10555'
                self.label[4] = 'arXiv:1806.10555'
                self.expt[4] = 'ATLAS'
                self.file_name[4] = '1806.10555_ATLAS_Fig-13_a_pp_TT_Zt_singlet.txt'
                self.process[4] = 'pp --> TT'
                self.energy[4] = 13
                self.luminosity[4] = 36.1

                self.key[5] = '04758'
                self.label[5] = 'arXiv:1805.04758'
                self.expt[5] = 'CMS'
                self.file_name[5] = '1805.04758_CMS_Fig8-upper-row-left_pp_TT_bW_Zt_tH_Singlet.txt'
                self.process[5] = 'pp --> TT'
                self.energy[5] = 13
                self.luminosity[5] = 35.9

                self.key[6] = '11883'
                self.label[6] = 'arXiv:1807.11883'
                self.expt[6] = 'ATLAS'
                self.file_name[6] = '1807.11883_ATLAS_pp_TT_Wb_Zt_Ht_Fig_8_b_Singlet.txt'
                self.process[6] = 'pp --> TT'
                self.energy[6] = 13
                self.luminosity[6] = 36.1

                self.key[7] = '03408'
                self.label[7] = 'arXiv:1706.03408'
                self.expt[7] = 'CMS'
                self.file_name[7] = '1706.03408_CMS_Fig-12-left_pp_TT_bW_Zt_tH_Singlet.txt'
                self.process[7] = 'pp --> TT'
                self.energy[7] = 13
                self.luminosity[7] = 2.6

                self.key[8] = '5500fc'
                self.label[8] = 'arXiv:1409.5500'
                self.expt[8] = 'ATLAS'
                self.file_name[8] = '1409.5500_ATLAS_Fig-12-c_pp_TT_Zt_Singlet.txt'
                self.process[8] = 'pp --> TT'
                self.energy[8] = 8
                self.luminosity[8] = 20.3

                self.key[9] = '04306fb'
                self.label[9] = 'arXiv:1505.04306'
                self.expt[9] = 'ATLAS'
                self.file_name[9] = '1505.04306_ATLAS_Fig18-b_pp_TT_Ht+X-Wb+X_Singlet.txt'
                self.process[9] = 'pp --> TT'
                self.energy[9] = 8
                self.luminosity[9] = 20.3

                self.key[10] = '02227fa'
                self.label[10] = 'arXiv:2201.02227'
                self.expt[10] = 'CMS'
                self.file_name[10] = '2201.02227_CMS_f8a_pp_Tbq_tZ_gamma_mT_0.05_Singlet.txt'
                self.process[10] = 'pp --> Tbq --> tZbq'
                self.energy[10] = 13
                self.luminosity[10] = 137

                self.key[11] = '02227fb'
                self.label[11] = 'arXiv:2201.02227'
                self.expt[11] = 'CMS'
                self.file_name[11] = '2201.02227_CMS_f8b_pp_Tbq_tZ_gamma_mT_0.1_Singlet.txt'
                self.process[11] = 'pp --> Tbq --> tZbq'
                self.energy[11] = 13
                self.luminosity[11] = 137

                self.key[12] = '02227fc'
                self.label[12] = 'arXiv:2201.02227'
                self.expt[12] = 'CMS'
                self.file_name[12] = '2201.02227_CMS_fig8c_pp_Tbq_tZ_gamma_mT_0.2_Singlet.txt'
                self.process[12] = 'pp --> Tbq --> tZbq'
                self.energy[12] = 13
                self.luminosity[12] = 137

                self.key[13] = '02227fd'
                self.label[13] = 'arXiv:2201.02227'
                self.expt[13] = 'CMS'
                self.file_name[13] = '2201.02227_CMS_fig8d_pp_Tbq_tZ_gamma_mT_0.3_Singlet.txt'
                self.process[13] = 'pp --> Tbq --> tZbq'
                self.energy[13] = 13
                self.luminosity[13] = 137

                self.key[14] = '01062f5a'
                self.label[14] = 'arXiv:1708.01062'
                self.expt[14] = 'CMS'
                self.file_name[14] = '1708.01062_CMS_Fig5-left_pp_Tbq_tZbq_Singlet-LH.txt'
                self.process[14] = 'pp --> Tbq --> tZbq'
                self.energy[14] = 13
                self.luminosity[14] = 35.9

                self.key[15] = '17605f35'
                self.label[15] = 'arXiv:2405.17605'
                self.expt[15] = 'CMS'
                self.file_name[15] = '2405.17605_CMS_fig35_pp_Tbq_singlet.dat'
                self.process[15] = 'pp --> Tbq'
                self.energy[15] = 13
                self.luminosity[15] = 138

                self.key[16] = '12802'
                self.label[16] = 'arXiv:2302.12802'
                self.expt[16] = 'CMS'
                self.file_name[16] = '2302.12802_CMS_f4_pp_Tbq_tH_Singlet.txt'
                self.process[16] = 'pp --> Tbq --> tHbq'
                self.energy[16] = 13
                self.luminosity[16] = 138

                self.key[17] = '00999f10a'
                self.label[17] = 'arXiv:1612.00999'
                self.expt[17] = 'CMS'
                self.file_name[17] = '1612.00999_CMS_Fig10-left_pp_TT_tH.txt'
                self.process[17] = 'pp --> Tbq --> tHbq'
                self.energy[17] = 13
                self.luminosity[17] = 2.3

                self.key[18] = '04721f8a'
                self.label[18] = 'arXiv:1909.04721'
                self.expt[18] = 'CMS'
                self.file_name[18] = '1909.04721_CMS_Fig8_upper-row-left_pp_Tbq_tHbq.txt'
                self.process[18] = 'pp --> Tbq --> tHbq'
                self.energy[18] = 13
                self.luminosity[18] = 35.9

                self.key[19] = '04721f8b'
                self.label[19] = 'arXiv:1909.04721'
                self.expt[19] = 'CMS'
                self.file_name[19] = '1909.04721_CMS_Fig8_upper-row-right_pp_Tbq_tHbq.txt'
                self.process[19] = 'pp --> Tbq --> tHbq'
                self.energy[19] = 13
                self.luminosity[19] = 35.9

                self.key[20] = '04721f8c'
                self.label[20] = 'arXiv:1909.04721'
                self.expt[20] = 'CMS'
                self.file_name[20] = '1909.04721_CMS_Fig8_middle-row-left_pp_Tbq_tZbq.txt'
                self.process[20] = 'pp --> Tbq --> tZbq'
                self.energy[20] = 13
                self.luminosity[20] = 35.9

                self.key[21] = '04721f8d'
                self.label[21] = 'arXiv:1909.04721'
                self.expt[21] = 'CMS'
                self.file_name[21] = '1909.04721_CMS_Fig8_middle-row-right_pp_Tbq_tZbq.txt'
                self.process[21] = 'pp --> Tbq --> tZbq'
                self.energy[21] = 13
                self.luminosity[21] = 35.9

                self.key[22] = '04721f8e'
                self.label[22] = 'arXiv:1909.04721'
                self.expt[22] = 'CMS'
                self.file_name[22] = '1909.04721_CMS_Fig8_lower-row-left_pp_Tbq_tH+tZ_bq.txt'
                self.process[22] = 'pp --> Tbq --> (tZ + tH)bq'
                self.energy[22] = 13
                self.luminosity[22] = 35.9

                self.key[23] = '04721f8f'
                self.label[23] = 'arXiv:1909.04721'
                self.expt[23] = 'CMS'
                self.file_name[23] = '1909.04721_CMS_Fig8_lower-row-right_pp_Tbq_tH+tZ_bq.txt'
                self.process[23] = 'pp --> Tbq --> (tZ + tH)bq'
                self.energy[23] = 13
                self.luminosity[23] = 35.9

                self.key[24] = '04721f9a'
                self.label[24] = 'arXiv:1909.04721'
                self.expt[24] = 'CMS'
                self.file_name[24] = '1909.04721_CMS_Fig9_upper-row-left_pp_Tbq_tHbq.txt'
                self.process[24] = 'pp --> Tbq --> tHbq'
                self.energy[24] = 13
                self.luminosity[24] = 35.9

                self.key[25] = '04721f9b'
                self.label[25] = 'arXiv:1909.04721'
                self.expt[25] = 'CMS'
                self.file_name[25] = '1909.04721_CMS_Fig9_upper-row-right_pp_Tbq_tHbq.txt'
                self.process[25] = 'pp --> Tbq --> tHbq'
                self.energy[25] = 13
                self.luminosity[25] = 35.9

                self.key[26] = '04721f9c'
                self.label[26] = 'arXiv:1909.04721'
                self.expt[26] = 'CMS'
                self.file_name[26] = '1909.04721_CMS_Fig9_middle-row-left_pp_Tbq_tZbq.txt'
                self.process[26] = 'pp --> Tbq --> tZbq'
                self.energy[26] = 13
                self.luminosity[26] = 35.9

                self.key[27] = '04721f9d'
                self.label[27] = 'arXiv:1909.04721'
                self.expt[27] = 'CMS'
                self.file_name[27] = '1909.04721_CMS_Fig9_middle-row-right_pp_Tbq_tZbq.txt'
                self.process[27] = 'pp --> Tbq --> tZbq'
                self.energy[27] = 13
                self.luminosity[27] = 35.9

                self.key[28] = '04721f9e'
                self.label[28] = 'arXiv:1909.04721'
                self.expt[28] = 'CMS'
                self.file_name[28] = '1909.04721_CMS_Fig9_lower-row-left_pp_Tbq_tHbq_tZbq.txt'
                self.process[28] = 'pp --> Tbq --> (tZ + tH)bq'
                self.energy[28] = 13
                self.luminosity[28] = 35.9

                self.key[29] = '04721f9f'
                self.label[29] = 'arXiv:1909.04721'
                self.expt[29] = 'CMS'
                self.file_name[29] = '1909.04721_CMS_Fig9_lower-row-right_pp_Tbq_tHbq_tZbq.txt'
                self.process[29] = 'pp --> Tbq --> (tZ + tH)bq'
                self.energy[29] = 13
                self.luminosity[29] = 35.9

                self.key[30] = '05606f6'
                self.label[30] = 'arXiv:1602.05606'
                self.expt[30] = 'ATLAS'
                self.file_name[30] = '1602.05606_ATLAS_Fig6_pp_Tbj_Wb_singlet.txt'
                self.process[30] = 'pp --> Tbq --> bWbq'
                self.energy[30] = 8
                self.luminosity[30] = 20.3

                self.key[31] = '07409f4a'
                self.label[31] = 'arXiv:1701.07409'
                self.expt[31] = 'CMS'
                self.file_name[31] = '1701.07409_CMS_Fig4left_pp_Tb_tZ_singlet.txt'
                self.process[31] = 'pp --> Tbq --> tZbq'
                self.energy[31] = 13
                self.luminosity[31] = 2.3

                self.key[32] = '03401f11a'
                self.label[32] = 'arXiv:2305.03401'
                self.expt[32] = 'ATLAS'
                self.file_name[32] = '2305.03401_ATLAS_Fig11a_pp_Tqt_Wb_Ht_Zt_singlet-k02.txt'
                self.process[32] = 'pp --> Tb(t)q --> tZ(H)b(t)q'
                self.energy[32] = 13
                self.luminosity[32] = 139

                self.key[33] = '03401f11b'
                self.label[33] = 'arXiv:2305.03401'
                self.expt[33] = 'ATLAS'
                self.file_name[33] = '2305.03401_ATLAS_Fig11b_pp_Tqt_Wb_Ht_Zt_singlet-k04.txt'
                self.process[33] = 'pp --> Tb(t)q --> tZ(H)b(t)q'
                self.energy[33] = 13
                self.luminosity[33] = 139

                self.key[34] = '03401f11c'
                self.label[34] = 'arXiv:2305.03401'
                self.expt[34] = 'ATLAS'
                self.file_name[34] = '2305.03401_ATLAS_Fig11c_pp_Tqt_Wb_Ht_Zt_singlet-k06.txt'
                self.process[34] = 'pp --> Tb(t)q --> tZ(H)b(t)q'
                self.energy[34] = 13
                self.luminosity[34] = 139

                self.key[35] = '16561f9c'
                self.label[35] = 'arXiv:2402.16561'
                self.expt[35] = 'ATLAS'
                self.file_name[35] = '2402.16561_ATLAS_Fig9c_pp_T_Ht_Zt_singlet.txt'
                self.process[35] = "pp --> Tb(t)q --> tZb(t)q"
                self.energy[35] = 13
                self.luminosity[35] = 139

                self.key[36] = '09743f4c'
                self.label[36] = 'arXiv:1812.09743'
                self.expt[36] = 'ATLAS'
                self.file_name[36] = '1812.09743_ATLAS_Fig4c_pp_Tbq_Wb_Ht_Zt_singlet.txt'
                self.process[36] = "pp --> Tbq --> tZbq"
                self.energy[36] = 13
                self.luminosity[36] = 36.1

                self.key[37] = '07045f8a'
                self.label[37] = 'arXiv:2201.07045'
                self.expt[37] = 'ATLAS'
                self.file_name[37] = '2201.07045_ATLAS_Fig8-a_pp_TT_tH_k_T-0.1_singlet.txt'
                self.process[37] = "pp --> Tbq --> tHbq"
                self.energy[37] = 13
                self.luminosity[37] = 139

                self.key[38] = '07045f8b'
                self.label[38] = 'arXiv:2201.07045'
                self.expt[38] = 'ATLAS'
                self.file_name[38] = '2201.07045_ATLAS_Fig8-b_pp_TT_tH_k_T-0.3_singlet.txt'
                self.process[38] = "pp --> Tbq --> tHbq"
                self.energy[38] = 13
                self.luminosity[38] = 139

                self.key[39] = '07045f8c'
                self.label[39] = 'arXiv:2201.07045'
                self.expt[39] = 'ATLAS'
                self.file_name[39] = '2201.07045_ATLAS_Fig8-c_pp_TT_tH_k_T-0.5_singlet.txt'
                self.process[39] = "pp --> Tbq --> tHbq"
                self.energy[39] = 13
                self.luminosity[39] = 139

                self.key[40] = '07045f8d'
                self.label[40] = 'arXiv:2201.07045'
                self.expt[40] = 'ATLAS'
                self.file_name[40] = '2201.07045_ATLAS_Fig8-d_pp_TT_tH_k_T-0.7_singlet.txt'
                self.process[40] = "pp --> Tbq --> tHbq"
                self.energy[40] = 13
                self.luminosity[40] = 139

                self.key[41] = '07045f8e'
                self.label[41] = 'arXiv:2201.07045'
                self.expt[41] = 'ATLAS'
                self.file_name[41] = '2201.07045_ATLAS_Fig8-e_pp_TT_tH_k_T-0.9_singlet.txt'
                self.process[41] = "pp --> Tbq --> tHbq"
                self.energy[41] = 13
                self.luminosity[41] = 139

                self.key[42] = '07045f8f'
                self.label[42] = 'arXiv:2201.07045'
                self.expt[42] = 'ATLAS'
                self.file_name[42] = '2201.07045_ATLAS_Fig8-f_pp_TT_tH_k_T-1.1_singlet.txt'
                self.process[42] = "pp --> Tbq --> tHbq"
                self.energy[42] = 13
                self.luminosity[42] = 139

                self.key[43] = '07584f8a'
                self.label[43] = 'arXiv:2307.07584'
                self.expt[43] = 'ATLAS'
                self.file_name[43] = '2307.07584_ATLAS_Fig8a_pp_T_Wb_Ht_Zt_singlet_k03.txt'
                self.process[43] = "pp --> Tb(t)q --> tZb(t)q"
                self.energy[43] = 13
                self.luminosity[43] = 139

                self.key[44] = '07584f8c'
                self.label[44] = 'arXiv:2307.07584'
                self.expt[44] = 'ATLAS'
                self.file_name[44] = '2307.07584_ATLAS_Fig8c_pp_T_Wb_Ht_Zt_singlet_k05.txt'
                self.process[44] = "pp --> Tb(t)q --> tZb(t)q"
                self.energy[44] = 13
                self.luminosity[44] = 139

                self.key[45] = '07584f8e'
                self.label[45] = 'arXiv:2307.07584'
                self.expt[45] = 'ATLAS'
                self.file_name[45] = '2307.07584_ATLAS_Fig8e_pp_T_Wb_Ht_Zt_singlet_k07.txt'
                self.process[45] = "pp --> Tb(t)q --> tZb(t)q"
                self.energy[45] = 13
                self.luminosity[45] = 139

                self.key[46] = '05336f4ul'
                self.label[46] = 'arXiv:1612.05336'
                self.expt[46] = 'CMS'
                self.file_name[46] = '1612.05336_CMS_fig4_upper_left_pp_Tbq_tHbq_LH_coupling.txt'
                self.process[46] = "pp --> Tbq --> tHbq"
                self.energy[46] = 13
                self.luminosity[46] = 2.3

                self.key[47] = '032f6b'
                self.label[47] = 'ATLAS-CONF-2016-032'
                self.expt[47] = 'ATLAS'
                self.file_name[47] = 'ATLAS-CONF-2016-032_ATLAS_Fig6b_pp_TT_Wb_Zt_Ht_Singlet.txt'
                self.process[47] = 'pp --> TT'
                self.energy[47] = 13
                self.luminosity[47] = 3.2

                self.key[48] = '104f16a'
                self.label[48] = 'ATLAS-CONF-2016-104'
                self.expt[48] = 'ATLAS'
                self.file_name[48] = 'ATLAS-CONF-2016-104_ATLAS_Fig16b_pp_TT_HtX_singlet.txt'
                self.process[48] = 'pp --> TT'
                self.energy[48] = 13
                self.luminosity[48] = 13.2

                self.key[49] = '7667f6'
                self.label[49] = 'arXiv:1311.7667'
                self.expt[49] = 'CMS'
                self.file_name[49] = '1311.7667_CMS_Fig6_pp_TT_bW_tH_Zt.txt'
                self.process[49] = 'pp --> TT'
                self.energy[49] = 8
                self.luminosity[49] = 19.5

                self.key[50] = '05071f4ur'
                self.label[50] = 'arXiv:2405.05071'
                self.expt[50] = 'CMS'
                self.file_name[50] = '2405.05071_CMS_Fig7_upper_right_pp_Tbq_tZbq.txt'
                self.process[50] = "pp --> Tbq --> tZbq --> tbbbq"
                self.energy[50] = 13
                self.luminosity[50] = 138

                self.key[51] = '05071f4ul'
                self.label[51] = 'arXiv:2405.05071'
                self.expt[51] = 'CMS'
                self.file_name[51] = '2405.05071_CMS_Fig7_upper_left_pp_Tbq_tHbq.txt'
                self.process[51] = "pp --> Tbq --> tHbq --> tbbbq"
                self.energy[51] = 13
                self.luminosity[51] = 138

                self.key[52] = '05071f4ll'
                self.label[52] = 'arXiv:2405.05071'
                self.expt[52] = 'CMS'
                self.file_name[52] = '2405.05071_CMS_Fig7_lower_left_pp_Tbq_tZbq_tHbq.txt'
                self.process[52] = "pp --> Tbq --> (tH + tZ)bq --> tbbbq"
                self.energy[52] = 13
                self.luminosity[52] = 138

                self.key[53] = '05071f4lr'
                self.label[53] = 'arXiv:2405.05071'
                self.expt[53] = 'CMS'
                self.file_name[53] = '2405.05071_CMS_Fig7_lower_right_pp_Tbq_tZbq_tHbq.txt'
                self.process[53] = "pp --> Tbq --> (tH + tZ)bq --> tbbbq"
                self.energy[53] = 13
                self.luminosity[53] = 138

                self.key[54] = '04605f7b'
                self.label[54] = 'arXiv:1504.04605'
                self.expt[54] = 'ATLAS'
                self.file_name[54] = '1504.04605_ATLAS_Fig7b_pp_TT_bW_tH_Zt_singlet.txt'
                self.process[54] = 'pp --> TT'
                self.energy[54] = 8
                self.luminosity[54] = 20.3

                self.key[55] = '09678f17b'
                self.label[55] = 'arXiv:1803.09678'
                self.expt[55] = 'ATLAS'
                self.file_name[55] = '1803.09678_ATLAS_Fig17-b_pp_TT_Wb_Ht_Zt_Singlet.txt'
                self.process[55] = 'pp --> TT'
                self.energy[55] = 13
                self.luminosity[55] = 36.1

                self.key[56] = '15413f7a'
                self.label[56] = 'arXiv:2210.15413'
                self.expt[56] = 'ATLAS'
                self.file_name[56] = '2210.15413_ATLAS_Fig7-a_pp_TT_Wb-Zt_Ht_Singlet.txt'
                self.process[56] = 'pp --> TT'
                self.energy[56] = 13
                self.luminosity[56] = 139

                self.key[57] = '10555f15'
                self.label[57] = 'arXiv:1806.10555'
                self.expt[57] = 'ATLAS'
                self.file_name[57] = '1806.10555_ATLAS_Fig15_pp_T_Zt_Singlet.txt'
                self.process[57] = "pp --> Tbq --> tZbq"
                self.energy[57] = 13
                self.luminosity[57] = 36.1

                self.key[58] = '08328'
                self.label[58] = 'arXiv:1701.08328'
                self.expt[58] = 'CMS'
                self.file_name[58] = '1701.08328_CMS_fig5_pp_Tbq_or_Ybq_bW.txt'
                self.process[58] = 'pp --> Tbq --> bWbq'
                self.energy[58] = 13
                self.luminosity[58] = 2.3

                load_data_from_files(self.file_name, len(self.key), self.MT, self.exp, self.obs, self.expt)

            elif self.m.model() == 'Doublet':
                self.key[0] = '10751'
                self.label[0] = 'arXiv:1705.10751'
                self.expt[0] = 'ATLAS'
                self.file_name[0] = '1705.10751_ATLAS_fig6c_pp_TT_Doublet.txt'
                self.process[0] = 'pp --> TT'
                self.energy[0] = 13
                self.luminosity[0] = 36.1
                self.which_doublet[0] = 'XTorTB'

                self.key[1] = '07327'
                self.label[1] = 'arXiv:2209.07327'
                self.expt[1] = 'CMS'
                self.file_name[1] = '2209.07327_CMS_f9b_pp_TTbar_Doublet.txt'
                self.process[1] = 'pp --> TT'
                self.energy[1] = 13
                self.luminosity[1] = 138
                self.which_doublet[1] = 'XTorTB'

                self.key[2] = '05263'
                self.label[2] = 'arXiv:2212.05263'
                self.expt[2] = 'ATLAS'
                self.file_name[2] = '2212.05263_ATLAS_fig7e_pp_TT_Zt_T,B_or_X,T_Doublet.txt'
                self.process[2] = 'pp --> TT'
                self.energy[2] = 13
                self.luminosity[2] = 36.1
                self.which_doublet[2] = 'XTorTB'

                self.key[3] = '10555'
                self.label[3] = 'arXiv:1806.10555'
                self.expt[3] = 'ATLAS'
                self.file_name[3] = '1806.10555_ATLAS_Fig-13_c_pp_TT_Zt_doublet.txt'
                self.process[3] = 'pp --> TT'
                self.energy[3] = 13
                self.luminosity[3] = 139
                self.which_doublet[3] = 'XT'

                self.key[4] = '04758'
                self.label[4] = 'arXiv:1805.04758'
                self.expt[4] = 'CMS'
                self.file_name[4] = '1805.04758_CMS_Fig8-upper-row-right_pp_TT_Zt_tH_Doublet.txt'
                self.process[4] = 'pp --> TT'
                self.energy[4] = 13
                self.luminosity[4] = 35.9
                self.which_doublet[4] = 'XTorTB'

                self.key[5] = '00999f10b'
                self.label[5] = 'arXiv:1612.00999'
                self.expt[5] = 'CMS'
                self.file_name[5] = '1612.00999_CMS_Fig10-right_pp_Ttq_tH.txt'
                self.process[5] = 'pp --> Ttq --> tHtq'
                self.energy[5] = 13
                self.luminosity[5] = 2.3
                self.which_doublet[5] = 'XTorTB'

                self.key[6] = '03408'
                self.label[6] = 'arXiv:1706.03408'
                self.expt[6] = 'CMS'
                self.file_name[6] = '1706.03408_CMS_Fig-12-right_pp_TT_Zt_tH_Doublet.txt'
                self.process[6] = 'pp --> TT'
                self.energy[6] = 13
                self.luminosity[6] = 2.6
                self.which_doublet[6] = 'XTorTB'

                self.key[7] = '01062f5b'
                self.label[7] = 'arXiv:1708.01062'
                self.expt[7] = 'CMS'
                self.file_name[7] = '1708.01062_CMS_Fig5-right_pp_Ttq_tZtq_Doublet-RH.txt'
                self.process[7] = 'pp --> Ttq --> tZtq'
                self.energy[7] = 13
                self.luminosity[7] = 35.9
                self.which_doublet[7] = 'XTorTB'

                self.key[8] = '5500fd'
                self.label[8] = 'arXiv:1409.5500'
                self.expt[8] = 'ATLAS'
                self.file_name[8] = '1409.5500_ATLAS_Fig-12-d_pp_TT_Zt_doublet.txt'
                self.process[8] = 'pp --> TT'
                self.energy[8] = 8
                self.luminosity[8] = 20.3
                self.which_doublet[8] = 'TB'


                self.key[9] = '04721f10a'
                self.label[9] = 'arXiv:1909.04721'
                self.expt[9] = 'CMS'
                self.file_name[9] = '1909.04721_CMS_Fig10_upper-row-left_pp_Ttq_tHtq.txt'
                self.process[9] = 'pp --> Ttq --> tHtq'
                self.energy[9] = 13
                self.luminosity[9] = 35.9
                self.which_doublet[9] = 'TB'

                self.key[10] = '04721f10b'
                self.label[10] = 'arXiv:1909.04721'
                self.expt[10] = 'CMS'
                self.file_name[10] = '1909.04721_CMS_Fig10_upper-row-right_pp_Ttq_tHtq.txt'
                self.process[10] = 'pp --> Ttq --> tHtq'
                self.energy[10] = 13
                self.luminosity[10] = 35.9
                self.which_doublet[10] = 'TB'

                self.key[11] = '04721f10c'
                self.label[11] = 'arXiv:1909.04721'
                self.expt[11] = 'CMS'
                self.file_name[11] = '1909.04721_CMS_Fig10_middle-row-left_pp_Ttq_tZtq.txt'
                self.process[11] = 'pp --> Ttq --> tZtq'
                self.energy[11] = 13
                self.luminosity[11] = 35.9
                self.which_doublet[11] = 'TB'

                self.key[12] = '04721f10d'
                self.label[12] = 'arXiv:1909.04721'
                self.expt[12] = 'CMS'
                self.file_name[12] = '1909.04721_CMS_Fig10_middle-row-right_pp_Ttq_tZtq.txt'
                self.process[12] = 'pp --> Ttq --> tZtq'
                self.energy[12] = 13
                self.luminosity[12] = 35.9
                self.which_doublet[12] = 'TB'

                self.key[13] = '04721f10e'
                self.label[13] = 'arXiv:1909.04721'
                self.expt[13] = 'CMS'
                self.file_name[13] = '1909.04721_CMS_Fig10_lower-row-left_pp_Ttq_tH-tZ_tq.txt'
                self.process[13] = 'pp --> Ttq --> (tZ + tH)tq'
                self.energy[13] = 13
                self.luminosity[13] = 35.9
                self.which_doublet[13] = 'TB'

                self.key[14] = '04721f10f'
                self.label[14] = 'arXiv:1909.04721'
                self.expt[14] = 'CMS'
                self.file_name[14] = '1909.04721_CMS_Fig10_lower-row-right_pp_Ttq_tH-tZ_tq.txt'
                self.process[14] = 'pp --> Ttq --> (tZ + tH)tq'
                self.energy[14] = 13
                self.luminosity[14] = 35.9
                self.which_doublet[14] = 'TB'

                self.key[15] = '04721f11a'
                self.label[15] = 'arXiv:1909.04721'
                self.expt[15] = 'CMS'
                self.file_name[15] = '1909.04721_CMS_Fig11_upper-row-left_pp_Ttq_tHtq.txt'
                self.process[15] = 'pp --> Ttq --> tHtq'
                self.energy[15] = 13
                self.luminosity[15] = 35.9
                self.which_doublet[15] = 'TB'

                self.key[16] = '04721f11b'
                self.label[16] = 'arXiv:1909.04721'
                self.expt[16] = 'CMS'
                self.file_name[16] = '1909.04721_CMS_Fig11_upper-row-right_pp_Ttq_tHtq.txt'
                self.process[16] = 'pp --> Ttq --> tHtq'
                self.energy[16] = 13
                self.luminosity[16] = 35.9
                self.which_doublet[16] = 'TB'

                self.key[17] = '04721f11c'
                self.label[17] = 'arXiv:1909.04721'
                self.expt[17] = 'CMS'
                self.file_name[17] = '1909.04721_CMS_Fig11_middle-row-left_pp_Ttq_tZtq.txt'
                self.process[17] = 'pp --> Ttq --> tZtq'
                self.energy[17] = 13
                self.luminosity[17] = 35.9
                self.which_doublet[17] = 'TB'

                self.key[18] = '04721f11d'
                self.label[18] = 'arXiv:1909.04721'
                self.expt[18] = 'CMS'
                self.file_name[18] = '1909.04721_CMS_Fig11_middle-row-right_pp_Ttq_tZtq.txt'
                self.process[18] = 'pp --> Ttq --> tZtq'
                self.energy[18] = 13
                self.luminosity[18] = 35.9
                self.which_doublet[18] = 'TB'

                self.key[19] = '04721f11e'
                self.label[19] = 'arXiv:1909.04721'
                self.expt[19] = 'CMS'
                self.file_name[19] = '1909.04721_CMS_Fig11_lower-row-left_pp_Ttq_tZ-tH_tq.txt'
                self.process[19] = 'pp --> Ttq --> (tZ + tH)tq'
                self.energy[19] = 13
                self.luminosity[19] = 35.9
                self.which_doublet[19] = 'TB'

                self.key[20] = '04721f11f'
                self.label[20] = 'arXiv:1909.04721'
                self.expt[20] = 'CMS'
                self.file_name[20] = '1909.04721_CMS_Fig11_lower-row-right_pp_Ttq_tZ-tH_tq.txt'
                self.process[20] = 'pp --> Ttq --> (tZ + tH)tq'
                self.energy[20] = 13
                self.luminosity[20] = 35.9
                self.which_doublet[20] = 'TB'

                self.key[21] = '07409f4b'
                self.label[21] = 'arXiv:1701.07409'
                self.expt[21] = 'CMS'
                self.file_name[21] = '1701.07409_CMS_Fig4right_pp_Tt_tZ_doublet.txt'
                self.process[21] = 'pp --> Ttq --> tZtq'
                self.energy[21] = 13
                self.luminosity[21] = 2.3
                self.which_doublet[21] = 'XTorTB'

                self.key[22] = '04306fc'
                self.label[22] = 'arXiv:1505.04306'
                self.expt[22] = 'ATLAS'
                self.file_name[22] = '1505.04306_ATLAS_Fig18-c_pp_TT_Ht+X_Doublet.txt'
                self.process[22] = 'pp --> TT'
                self.energy[22] = 8
                self.luminosity[22] = 20.3
                self.which_doublet[22] = 'XTorTB'

                self.key[23] = '03401f12a'
                self.label[23] = 'arXiv:2305.03401'
                self.expt[23] = 'ATLAS'
                self.file_name[23] = '2305.03401_ATLAS_Fig12a_pp_Tqt_Ht_Zt_doublet-k02.txt'
                self.process[23] = 'pp --> Tb(t)q --> tZ(H)b(t)q'
                self.energy[23] = 13
                self.luminosity[23] = 139
                self.which_doublet[23] = 'TB'

                self.key[24] = '03401f12b'
                self.label[24] = 'arXiv:2305.03401'
                self.expt[24] = 'ATLAS'
                self.file_name[24] = '2305.03401_ATLAS_Fig12b_pp_Tqt_Ht_Zt_doublet-k04.txt'
                self.process[24] = 'pp --> Tb(t)q --> tZ(H)b(t)q'
                self.energy[24] = 13
                self.luminosity[24] = 139
                self.which_doublet[24] = 'TB'

                self.key[25] = '03401f12c'
                self.label[25] = 'arXiv:2305.03401'
                self.expt[25] = 'ATLAS'
                self.file_name[25] = '2305.03401_ATLAS_Fig12c_pp_Tqt_Ht_Zt_doublet-k06.txt'
                self.process[25] = 'pp --> Tb(t)q --> tZ(H)b(t)q'
                self.energy[25] = 13
                self.luminosity[25] = 139
                self.which_doublet[25] = 'TB'

                self.key[26] = '07584f8b'
                self.label[26] = 'arXiv:2307.07584'
                self.expt[26] = 'ATLAS'
                self.file_name[26] = '2307.07584_ATLAS_Fig8b_pp_T_Ht_Zt_doublet_k03.txt'
                self.process[26] = "pp --> Ttq --> tZtq"
                self.energy[26] = 13
                self.luminosity[26] = 139
                self.which_doublet[26] = 'XTorTB'

                self.key[27] = '07584f8d'
                self.label[27] = 'arXiv:2307.07584'
                self.expt[27] = 'ATLAS'
                self.file_name[27] = '2307.07584_ATLAS_Fig8d_pp_T_Ht_Zt_doublet_k05.txt'
                self.process[27] = "pp --> Ttq --> tZtq"
                self.energy[27] = 13
                self.luminosity[27] = 139
                self.which_doublet[27] = 'XTorTB'

                self.key[28] = '07584f8f'
                self.label[28] = 'arXiv:2307.07584'
                self.expt[28] = 'ATLAS'
                self.file_name[28] = '2307.07584_ATLAS_Fig8f_pp_T_Ht_Zt_doublet_k07.txt'
                self.process[28] = "pp --> Ttq --> tZtq"
                self.energy[28] = 13
                self.luminosity[28] = 139
                self.which_doublet[28] = 'XTorTB'

                self.key[29] = '05336f4lr'
                self.label[29] = 'arXiv:1612.05336'
                self.expt[29] = 'CMS'
                self.file_name[29] = '1612.05336_CMS_fig4_lower_right_pp_Tbq_tHbq_RH_coupling.txt'
                self.process[29] = "pp --> Ttq --> tHtq"
                self.energy[29] = 13
                self.luminosity[29] = 2.3
                self.which_doublet[29] = 'XTorTB'

                self.key[30] = '104f16a'
                self.label[30] = 'ATLAS-CONF-2016-104'
                self.expt[30] = 'ATLAS'
                self.file_name[30] = 'ATLAS-CONF-2016-104_ATLAS_Fig16a_pp_TT_HtX_doublet.txt'
                self.process[30] = 'pp --> TT'
                self.energy[30] = 13
                self.luminosity[30] = 13.2
                self.which_doublet[30] = 'XTorTB'

                self.key[31] = '09678f17a'
                self.label[31] = 'arXiv:1803.09678'
                self.expt[31] = 'ATLAS'
                self.file_name[31] = '1803.09678_ATLAS_Fig17-a_pp_TT_Ht_Zt_Doublet.txt'
                self.process[31] = 'pp --> TT'
                self.energy[31] = 13
                self.luminosity[31] = 36.1
                self.which_doublet[31] = 'XTorTB'

                self.key[32] = '15413f7c'
                self.label[32] = 'arXiv:2210.15413'
                self.expt[32] = 'ATLAS'
                self.file_name[32] = '2210.15413_ATLAS_Fig7-c_pp_TT_Zt_Ht_Doublet-X-T.txt'
                self.process[32] = 'pp --> TT'
                self.energy[32] = 13
                self.luminosity[32] = 139
                self.which_doublet[32] = 'XT'

                load_data_from_files(self.file_name, len(self.key), self.MT, self.exp, self.obs, self.expt)

            elif self.m.model() == 'Pure':
                self.key[0] = '05263'
                self.label[0] = 'arXiv:2212.05263'
                self.expt[0] = 'ATLAS'
                self.file_name[0] = '2212.05263_ATLAS_fig7a_pp_TT_tZ.txt'
                self.process[0] = 'pp --> TT'
                self.energy[0] = 13
                self.luminosity[0] = 139

                self.key[1] = '97680'
                self.label[1] = 'arXiv:1812.09768'
                self.expt[1] = 'CMS'
                self.file_name[1] = '1812.09768_CMS_fig4a_pp_TT_tZ.txt'
                self.process[1] = 'pp --> TT'
                self.energy[1] = 13
                self.luminosity[1] = 36.1

                self.key[2] = '10751fig6a'
                self.label[2] = 'arXiv:1705.10751'
                self.expt[2] = 'ATLAS'
                self.file_name[2] = '1705.10751_ATLAS_fig6a_pp_TT_Zt.txt'
                self.process[2] = 'pp --> TT'
                self.energy[2] = 13
                self.luminosity[2] = 36.1

                self.key[3] = '17710'
                self.label[3] = 'arXiv:1808.01771'
                self.expt[3] = 'ATLAS'
                self.file_name[3] = '1808.01771_ATLAS_fig13a_pp_TT_Ht.txt'
                self.process[3] = 'pp --> TT'
                self.energy[3] = 13
                self.luminosity[3] = 36.1

                self.key[4] = '19520'
                self.label[4] = 'arXiv:1503.01952'
                self.expt[4] = 'CMS'
                self.file_name[4] = '1503.01952_CMS_fig13_pp_TT_tH.txt'
                self.process[4] = 'pp --> TT'
                self.energy[4] = 8
                self.luminosity[4] = 19.7

                self.key[5] = '33470fig4a'
                self.label[5] = 'arXiv:1707.03347'
                self.expt[5] = 'ATLAS'
                self.file_name[5] = '1707.03347_ATLAS_fig4a_pp_TT_Wb.txt'
                self.process[5] = 'pp --> TT'
                self.energy[5] = 13
                self.luminosity[5] = 36.1

                self.key[6] = '10555'
                self.label[6] = 'arXiv:1806.10555'
                self.expt[6] = 'ATLAS'
                self.file_name[6] = '1806.10555_ATLAS_Fig-13e_pp_TT_Zt.txt'
                self.process[6] = 'pp --> TT'
                self.energy[6] = 13
                self.luminosity[6] = 36.1

                self.key[7] = '04177'
                self.label[7] = 'arXiv:1509.04177'
                self.expt[7] = 'CMS'
                self.file_name[7] = '1509.04177_CMS_fig8_pp_TT_bW.txt'
                self.process[7] = 'pp --> TT'
                self.energy[7] = 8
                self.luminosity[7] = 19.7

                self.key[8] = '04177'
                self.label[8] = 'arXiv:1509.04177'
                self.expt[8] = 'CMS'
                self.file_name[8] = '1509.04177_CMS_fig8_pp_TT_tH.txt'
                self.process[8] = 'pp --> TT'
                self.energy[8] = 8
                self.luminosity[8] = 19.7

                self.key[9] = '04177'
                self.label[9] = 'arXiv:1509.04177'
                self.expt[9] = 'CMS'
                self.file_name[9] = '1509.04177_CMS_fig8_pp_TT_tZ.txt'
                self.process[9] = 'pp --> TT'
                self.energy[9] = 8
                self.luminosity[9] = 19.7

                self.key[10] = '03408'
                self.label[10] = 'arXiv:1706.03408'
                self.expt[10] = 'CMS'
                self.file_name[10] = '1706.03408_CMS_Fig-11-left_pp_TT_bW.txt'
                self.process[10] = 'pp --> TT'
                self.energy[10] = 13
                self.luminosity[10] = 2.6

                self.key[11] = '03408'
                self.label[11] = 'arXiv:1706.03408'
                self.expt[11] = 'CMS'
                self.file_name[11] = '1706.03408_CMS_Fig-11-right_pp_TT_tH.txt'
                self.process[11] = 'pp --> TT'
                self.energy[11] = 13
                self.luminosity[11] = 2.6

                self.key[12] = '0471fa'
                self.label[12] = 'arXiv:1209.0471'
                self.expt[12] = 'CMS'
                self.file_name[12] = '1209.0471_CMS_Fig6_upper_pp_TT_bW.txt'
                self.process[12] = 'pp --> TT'
                self.energy[12] = 13
                self.luminosity[12] = 2.6

                self.key[13] = '0471fb'
                self.label[13] = 'arXiv:1209.0471'
                self.expt[13] = 'CMS'
                self.file_name[13] = '1209.0471_CMS_Fig6_middle_pp_TT_bW.txt'
                self.process[13] = 'pp --> TT'
                self.energy[13] = 7
                self.luminosity[13] = 5

                self.key[14] = '0471fc'
                self.label[14] = 'arXiv:1209.0471'
                self.expt[14] = 'CMS'
                self.file_name[14] = '1209.0471_CMS_Fig6_lower_pp_TT_bW.txt'
                self.process[14] = 'pp --> TT'
                self.energy[14] = 7
                self.luminosity[14] = 5

                self.key[15] = '04306fa'
                self.label[15] = 'arXiv:1505.04306'
                self.expt[15] = 'ATLAS'
                self.file_name[15] = '1505.04306_ATLAS_Fig18-a_pp_TT_Wb+X.txt'
                self.process[15] = 'pp --> TT'
                self.energy[15] = 8
                self.luminosity[15] = 20.3

                self.key[16] = '5468'
                self.label[16] = 'arXiv:1210.5468'
                self.expt[16] = 'ATLAS'
                self.file_name[16] = '1210.5468_ATLAS_Fig-3_pp_tt_Wb.txt'
                self.process[16] = 'pp --> TT'
                self.energy[16] = 7
                self.luminosity[16] = 4.7

                self.key[17] = '01539'
                self.label[17] = 'arXiv:1710.01539'
                self.expt[17] = 'CMS'
                self.file_name[17] = '1710.01539_CMS_Fig4_upper_pp_TT_bW.txt'
                self.process[17] = 'pp --> TT'
                self.energy[17] = 13
                self.luminosity[17] = 35.8

                self.key[18] = '104f15a'
                self.label[18] = 'ATLAS-CONF-2016-104'
                self.expt[18] = 'ATLAS'
                self.file_name[18] = 'ATLAS-CONF-2016-104_ATLAS_Fig15a_pp_TT_tH.txt'
                self.process[18] = 'pp --> TT'
                self.energy[18] = 13
                self.luminosity[18] = 13.2

                self.key[19] = '104f15b'
                self.label[19] = 'ATLAS-CONF-2016-104'
                self.expt[19] = 'ATLAS'
                self.file_name[19] = 'ATLAS-CONF-2016-104_ATLAS_Fig15b_pp_TT_tZ.txt'
                self.process[19] = 'pp --> TT'
                self.energy[19] = 13
                self.luminosity[19] = 13.2

                self.key[20] = '11903fa'
                self.label[20] = 'arXiv:1906.11903'
                self.expt[20] = 'CMS'
                self.file_name[20] = '1906.11903_CMS_Fig6_lower_left_pp_TT_bW.txt'
                self.process[20] = 'pp --> TT'
                self.energy[20] = 13
                self.luminosity[20] = 35.9

                self.key[21] = '11903fc'
                self.label[21] = 'arXiv:1906.11903'
                self.expt[21] = 'CMS'
                self.file_name[21] = '1906.11903_CMS_Fig6_upper_left_pp_TT_tZ.txt'
                self.process[21] = 'pp --> TT'
                self.energy[21] = 13
                self.luminosity[21] = 35.9

                self.key[22] = '11903ff'
                self.label[22] = 'arXiv:1906.11903'
                self.expt[22] = 'CMS'
                self.file_name[22] = '1906.11903_CMS_Fig6_middle_left_pp_TT_tH.txt'
                self.process[22] = 'pp --> TT'
                self.energy[22] = 13
                self.luminosity[22] = 35.9

                self.key[23] = '5410f2'
                self.label[23] = 'arXiv:1203.5410'
                self.expt[23] = 'CMS'
                self.file_name[23] = '1203.5410_CMS_Fig2_pp_tt_bWbW.txt'
                self.process[23] = 'pp --> TT'
                self.energy[23] = 7
                self.luminosity[23] = 5

                self.key[24] = '3076f2'
                self.label[24] = 'arXiv:1202.3076'
                self.expt[24] = 'ATLAS'
                self.file_name[24] = '1202.3076_ATLAS_Fig2_pp_tt_WbWb.txt'
                self.process[24] = 'pp --> TT'
                self.energy[24] = 7
                self.luminosity[24] = 1.04

                self.key[25] = '03903f9'
                self.label[25] = 'arXiv:1606.03903'
                self.expt[25] = 'ATLAS'
                self.file_name[25] = '1606.03903_ATLAS_Fig9_pp_TT_Zt.txt'
                self.process[25] = 'pp --> TT'
                self.energy[25] = 13
                self.luminosity[25] = 3.2

                self.key[26] = '15413f7e'
                self.label[26] = 'arXiv:2210.15413'
                self.expt[26] = 'ATLAS'
                self.file_name[26] = '2210.15413_ATLAS_Fig7-e_pp_TT_Zt.txt'
                self.process[26] = 'pp --> TT'
                self.energy[26] = 13
                self.luminosity[26] = 139

                load_data_from_files(self.file_name, len(self.key), self.MT, self.exp, self.obs, self.expt)
            else:
                raise Exception("Error in model choice")

    def get_T_caracteristics(self):
        if self.m.model() == 'Singlet' or self.m.model() == 'pure':
            return self.key, self.label, self.expt, self.process, self.energy, self.luminosity

    def all_processes(self):
        with open("processes_info.dat", "w") as f:
            f.write("************* File for each cross section limit information*****************\n")
            f.write("This File has been generated with PyTop version 0.1\n")
            f.write(f"With the T quark in the {self.m.model()} scenario\n")
            for i, proc in enumerate(self.process):
                f.write("***********************************************************************\n")
                f.write(f"channel {i}:\n")
                f.write(f"{proc} \t\t {self.label[i]} ({self.expt[i]}) "
                        f"\t sqrt(s) = {self.energy[i]} TeV\t luminosity = {self.luminosity[i]} fb-1\n")

    def cs_dict(self):
        if self.VLB:
            pair_prod = [self.key[j] for j in range(len(self.process)) if self.process[j][:9] == 'pp --> BB']
            single_prod = [
                self.key[j]
                for j in range(len(self.process))
                if self.process[j][:9] == 'pp --> Bb' or self.process[j][:9] == 'pp --> Bt'
            ]

        else:
            pair_prod = [self.key[j] for j in range(len(self.process)) if self.process[j][:9] == 'pp --> TT']
            single_prod = [
                self.key[j]
                for j in range(len(self.process))
                if self.process[j][:9] == 'pp --> Tb' or self.process[j][:9] == 'pp --> Tt'
            ]

        self.cs_keys = {

            'pair_prod': pair_prod,
            'single_prod': single_prod
        }

    def tb_xt_dict(self):
        if self.VLB:
            if self.m.model() == 'Singlet' or self.m.model() == 'Pure':
                self.TB_YB_keys = {}

            elif self.m.model() == 'Doublet':
                BY_doublet_keys = [self.key[j] for j in range(len(self.key)) if self.which_doublet[j][:2] == 'BY']
                TB_doublet_keys = [self.key[j] for j in range(len(self.key)) if self.which_doublet[j][-2:] == 'TB']
                self.TB_XT_keys = {
                    '(T,B)': TB_doublet_keys,
                    '(B,Y)': BY_doublet_keys
                }
        else:
            if self.m.model() == 'Singlet' or self.m.model() == 'Pure':
                self.TB_XT_keys = {}
            elif self.m.model() == 'Doublet':
                XT_doublet_keys = [self.key[j] for j in range(len(self.key)) if self.which_doublet[j][:2] == 'XT']
                TB_doublet_keys = [self.key[j] for j in range(len(self.key)) if self.which_doublet[j][-2:] == 'TB']
                self.TB_XT_keys = {
                    '(T,B)': TB_doublet_keys,
                    '(X,T)': XT_doublet_keys
                }

            else:
                raise Exception(f"Error, this model {self.m.model()} is not included")
