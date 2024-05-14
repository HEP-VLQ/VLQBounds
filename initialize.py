import numpy as np
import os


class Tables:
    def __init__(self, m):
        self.key = None
        self.label = None
        self.expt = None
        self.MT = None
        self.exp = None
        self.obs = None
        self.file_name = None
        self.model = None
        self.process = None
        self.energy = None
        self.luminosity = None
        self.cs_keys = {}
        self.m = m

    def initialize_tables_cms_and_atlas(self):
        """" fills experimental data from files """
        if self.m.model() == 'Singlet':

            number_of_atlas_cms_tables = 46

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

            self.key[0] = '10751fig6b'
            self.label[0] = 'arXiv:1705.10751'
            self.expt[0] = 'ATLAS'
            self.file_name[0] = '1705.10751_ATLAS_fig6b_pp_TT_Zt_Singlet.txt'
            self.process[0] = 'pp --> TT --> Zt + X -> l+ + E_T + j'
            self.energy[0] = 13
            self.luminosity[0] = 36.1

            self.key[1] = '73270'
            self.label[1] = 'arXiv:2209.07327'
            self.expt[1] = 'CMS'
            self.file_name[1] = '2209.07327_CMS_f9a_pp_TTbar_Singlet.txt'
            self.process[1] = 'pp --> TT --> l+ + l+l+ + l+l+l-'
            self.energy[1] = 13
            self.luminosity[1] = 138

            self.key[2] = '33470fig4b'
            self.label[2] = 'arXiv:1707.03347'
            self.expt[2] = 'ATLAS'
            self.file_name[2] = '1707.03347_ATLAS_fig4b_pp_TT_Singlet.txt'
            self.process[2] = 'pp --> TT --> Wb + X --> l+ + E_T + j'
            self.energy[2] = 13
            self.luminosity[2] = 36.1

            self.key[3] = '05263'
            self.label[3] = 'arXiv:2212.05263'
            self.expt[3] = 'ATLAS'
            self.file_name[3] = '2212.05263_ATLAS_fig7c_pp_TT_Zt_Singlet.txt'
            self.process[3] = 'pp --> TT --> Zt + X -> l+ + E_T + j'
            self.energy[3] = 13
            self.luminosity[3] = 139

            self.key[4] = '10555'
            self.label[4] = 'arXiv:1806.10555'
            self.expt[4] = 'ATLAS'
            self.file_name[4] = '1806.10555_ATLAS_Fig-13_a_pp_TT_Zt_singlet.txt'
            self.process[4] = 'pp --> TT --> Zt + X -> l+l- + l+l+l-'
            self.energy[4] = 13
            self.luminosity[4] = 36.1

            self.key[5] = '04758'
            self.label[5] = 'arXiv:1805.04758'
            self.expt[5] = 'CMS'
            self.file_name[5] = '1805.04758_CMS_Fig8-upper-row-left_pp_TT_bW_Zt_tH_Singlet.txt'
            self.process[5] = 'pp --> TT --> l+ + l+l+ + l+l+l-'
            self.energy[5] = 13
            self.luminosity[5] = 35.9

            self.key[6] = '11883'
            self.label[6] = 'arXiv:1807.11883'
            self.expt[6] = 'ATLAS'
            self.file_name[6] = '1807.11883_ATLAS_pp_TT_Wb_Zt_Ht_Fig_8_b_Singlet.txt'
            self.process[6] = 'pp --> TT --> l+l+ + j'
            self.energy[6] = 13
            self.luminosity[6] = 36.1

            self.key[7] = '03408'
            self.label[7] = 'arXiv:1706.03408'
            self.expt[7] = 'CMS'
            self.file_name[7] = '1706.03408_CMS_Fig-12-left_pp_TT_bW_Zt_tH_Singlet.txt'
            self.process[7] = 'pp --> TT --> l+ + E_T + j'
            self.energy[7] = 13
            self.luminosity[7] = 2.6

            self.key[8] = '5500fc'
            self.label[8] = 'arXiv:1409.5500'
            self.expt[8] = 'ATLAS'
            self.file_name[8] = '1409.5500_ATLAS_Fig-12-c_pp_TT_Zt_Singlet.txt'
            self.process[8] = 'pp --> TT --> Zt + X -> l+l- + l+l+l-'
            self.energy[8] = 8
            self.luminosity[8] = 20.3

            self.key[9] = '04306fb'
            self.label[9] = 'arXiv:1505.04306'
            self.expt[9] = 'ATLAS'
            self.file_name[9] = '1505.04306_ATLAS_Fig18-b_pp_TT_Ht+X-Wb+X_Singlet.txt'
            self.process[9] = 'pp --> TT --> Wb + X + Ht + X --> l+ + E_T + j'
            self.energy[9] = 8
            self.luminosity[9] = 20.3

            self.key[10] = '02227fa'
            self.label[10] = 'arXiv:2201.02227'
            self.expt[10] = 'CMS'
            self.file_name[10] = '2201.02227_CMS_f8a_pp_Tbq_tZ_gamma_mT_0.05_Singlet.txt'
            self.process[10] = 'pp --> Tbq --> tZbq --> E_T + j'
            self.energy[10] = 13
            self.luminosity[10] = 137

            self.key[11] = '02227fb'
            self.label[11] = 'arXiv:2201.02227'
            self.expt[11] = 'CMS'
            self.file_name[11] = '2201.02227_CMS_f8b_pp_Tbq_tZ_gamma_mT_0.1_Singlet.txt'
            self.process[11] = 'pp --> Tbq --> tZbq --> E_T + j'
            self.energy[11] = 13
            self.luminosity[11] = 137

            self.key[12] = '02227fc'
            self.label[12] = 'arXiv:2201.02227'
            self.expt[12] = 'CMS'
            self.file_name[12] = '2201.02227_CMS_fig8c_pp_Tbq_tZ_gamma_mT_0.2_Singlet.txt'
            self.process[12] = 'pp --> Tbq --> tZbq --> E_T + j'
            self.energy[12] = 13
            self.luminosity[12] = 137

            self.key[13] = '02227fd'
            self.label[13] = 'arXiv:2201.02227'
            self.expt[13] = 'CMS'
            self.file_name[13] = '2201.02227_CMS_fig8d_pp_Tbq_tZ_gamma_mT_0.3_Singlet.txt'
            self.process[13] = 'pp --> Tbq --> tZbq --> E_T + j'
            self.energy[13] = 13
            self.luminosity[13] = 137

            self.key[14] = '01062f5a'
            self.label[14] = 'arXiv:1708.01062'
            self.expt[14] = 'CMS'
            self.file_name[14] = '1708.01062_CMS_Fig5-left_pp_Tbq_tZbq_Singlet-LH.txt'
            self.process[14] = 'pp --> Tbq --> tZbq --> l+l- + j'
            self.energy[14] = 13
            self.luminosity[14] = 35.9

            self.key[15] = '5500'
            self.label[15] = 'arXiv:1409.5500'
            self.expt[15] = 'ATLAS'
            self.file_name[15] = '1409.5500_ATLAS_Fig-15-b_pp_Tbq_Zt.txt'
            self.process[15] = 'pp --> Tbq --> tZbq --> l+l- + j'
            self.energy[15] = 8
            self.luminosity[15] = 20.3

            self.key[16] = '12802'
            self.label[16] = 'arXiv:2302.12802'
            self.expt[16] = 'CMS'
            self.file_name[16] = '2302.12802_CMS_f4_pp_Tbq_tH_Singlet.txt'
            self.process[16] = 'pp --> Tbq --> tHbq --> l+ + gamma + E_T + j'
            self.energy[16] = 13
            self.luminosity[16] = 138

            self.key[17] = '00999f10a'
            self.label[17] = 'arXiv:1612.00999'
            self.expt[17] = 'CMS'
            self.file_name[17] = '1612.00999_CMS_Fig10-left_pp_TT_tH.txt'
            self.process[17] = 'pp --> Tbq --> tHbq --> l+ + E_T + j'
            self.energy[17] = 13
            self.luminosity[17] = 2.3

            self.key[18] = '04721f8b'
            self.label[18] = 'arXiv:1909.04721'
            self.expt[18] = 'CMS'
            self.file_name[18] = '1909.04721_CMS_Fig8_upper-row-right_pp_Tbq_tHbq.txt'
            self.process[18] = 'pp --> Tbq --> tHbq --> j'
            self.energy[18] = 13
            self.luminosity[18] = 35.9

            self.key[19] = '04721f8a'
            self.label[19] = 'arXiv:1909.04721'
            self.expt[19] = 'CMS'
            self.file_name[19] = '1909.04721_CMS_Fig8_upper-row-left_pp_Tbq_tHbq.txt'
            self.process[19] = 'pp --> Tbq --> tHbq --> j'
            self.energy[19] = 13
            self.luminosity[19] = 35.9

            self.key[20] = '04721f8d'
            self.label[20] = 'arXiv:1909.04721'
            self.expt[20] = 'CMS'
            self.file_name[20] = '1909.04721_CMS_Fig8_middle-row-right_pp_Tbq_tZbq.txt'
            self.process[20] = 'pp --> Tbq --> tZbq --> j'
            self.energy[20] = 13
            self.luminosity[20] = 35.9

            self.key[21] = '04721f8c'
            self.label[21] = 'arXiv:1909.04721'
            self.expt[21] = 'CMS'
            self.file_name[21] = '1909.04721_CMS_Fig8_middle-row-left_pp_Tbq_tZbq.txt'
            self.process[21] = 'pp --> Tbq --> tZbq --> j'
            self.energy[21] = 13
            self.luminosity[21] = 35.9

            self.key[22] = '04721f8f'
            self.label[22] = 'arXiv:1909.04721'
            self.expt[22] = 'CMS'
            self.file_name[22] = '1909.04721_CMS_Fig8_lower-row-right_pp_Tbq_tH+tZ_bq.txt'
            self.process[22] = 'pp --> Tbq --> (tZ + tH)bq --> j'
            self.energy[22] = 13
            self.luminosity[22] = 35.9

            self.key[23] = '04721f8e'
            self.label[23] = 'arXiv:1909.04721'
            self.expt[23] = 'CMS'
            self.file_name[23] = '1909.04721_CMS_Fig8_lower-row-left_pp_Tbq_tH+tZ_bq.txt'
            self.process[23] = 'pp --> Tbq --> (tZ + tH)bq --> j'
            self.energy[23] = 13
            self.luminosity[23] = 35.9

            self.key[24] = '04721f9b'
            self.label[24] = 'arXiv:1909.04721'
            self.expt[24] = 'CMS'
            self.file_name[24] = '1909.04721_CMS_Fig9_upper-row-right_pp_Tbq_tHbq.txt'
            self.process[24] = 'pp --> Tbq --> tHbq --> j'
            self.energy[24] = 13
            self.luminosity[24] = 35.9

            self.key[25] = '04721f9a'
            self.label[25] = 'arXiv:1909.04721'
            self.expt[25] = 'CMS'
            self.file_name[25] = '1909.04721_CMS_Fig9_upper-row-left_pp_Tbq_tHbq.txt'
            self.process[25] = 'pp --> Tbq --> tHbq --> j'
            self.energy[25] = 13
            self.luminosity[25] = 35.9

            self.key[26] = '04721f9d'
            self.label[26] = 'arXiv:1909.04721'
            self.expt[26] = 'CMS'
            self.file_name[26] = '1909.04721_CMS_Fig9_middle-row-right_pp_Tbq_tZbq.txt'
            self.process[26] = 'pp --> Tbq --> tZbq --> j'
            self.energy[26] = 13
            self.luminosity[26] = 35.9

            self.key[27] = '04721f9c'
            self.label[27] = 'arXiv:1909.04721'
            self.expt[27] = 'CMS'
            self.file_name[27] = '1909.04721_CMS_Fig9_middle-row-left_pp_Tbq_tZbq.txt'
            self.process[27] = 'pp --> Tbq --> tZbq --> j'
            self.energy[27] = 13
            self.luminosity[27] = 35.9

            self.key[28] = '04721f9f'
            self.label[28] = 'arXiv:1909.04721'
            self.expt[28] = 'CMS'
            self.file_name[28] = '1909.04721_CMS_Fig9_lower-row-right_pp_Tbq_tHbq_tZbq.txt'
            self.process[28] = 'pp --> Tbq --> tHbq --> j'
            self.energy[28] = 13
            self.luminosity[28] = 35.9

            self.key[29] = '04721f9e'
            self.label[29] = 'arXiv:1909.04721'
            self.expt[29] = 'CMS'
            self.file_name[29] = '1909.04721_CMS_Fig9_lower-row-left_pp_Tbq_tHbq_tZbq.txt'
            self.process[29] = 'pp --> Tbq --> tHbq --> j'
            self.energy[29] = 13
            self.luminosity[29] = 35.9

            self.key[30] = '05606f6'
            self.label[30] = 'arXiv:1602.05606'
            self.expt[30] = 'ATLAS'
            self.file_name[30] = '1602.05606_ATLAS_Fig6_pp_Tbj_Wb.txt'
            self.process[30] = 'pp --> Tbq --> bWbq --> l+ + E_T + j'
            self.energy[30] = 8
            self.luminosity[30] = 20.3

            self.key[31] = '07409f4a'
            self.label[31] = 'arXiv:1701.07409'
            self.expt[31] = 'CMS'
            self.file_name[31] = '1701.07409_CMS_Fig4left_pp_Tb_tZ_singlet.txt'
            self.process[31] = 'pp --> Tbq --> tZbq --> l+l- + j'
            self.energy[31] = 13
            self.luminosity[31] = 2.3

            self.key[32] = '03401f11a'
            self.label[32] = 'arXiv:2305.03401'
            self.expt[32] = 'ATLAS'
            self.file_name[32] = '2305.03401_ATLAS_Fig11a_pp_Tqt_Wb_Ht_Zt_singlet-k02.txt'
            self.process[32] = 'pp --> Tbq --> tZ(H)bq --> l+ + E_T + j'
            self.energy[32] = 13
            self.luminosity[32] = 139

            self.key[33] = '03401f11b'
            self.label[33] = 'arXiv:2305.03401'
            self.expt[33] = 'ATLAS'
            self.file_name[33] = '2305.03401_ATLAS_Fig11b_pp_Tqt_Wb_Ht_Zt_singlet-k04.txt'
            self.process[33] = 'pp --> Tbq --> tZ(H)bq --> l+ + E_T + j'
            self.energy[33] = 13
            self.luminosity[33] = 139

            self.key[34] = '03401f11c'
            self.label[34] = 'arXiv:2305.03401'
            self.expt[34] = 'ATLAS'
            self.file_name[34] = '2305.03401_ATLAS_Fig11c_pp_Tqt_Wb_Ht_Zt_singlet-k06.txt'
            self.process[34] = 'pp --> Tbq --> tZ(H)bq --> l+ + E_T + j'
            self.energy[34] = 13
            self.luminosity[34] = 139

            self.key[35] = '16561f9c'
            self.label[35] = 'arXiv:2402.16561'
            self.expt[35] = 'ATLAS'
            self.file_name[35] = '2402.16561_ATLAS_Fig9c_pp_T_Ht_Zt_singlet.txt'
            self.process[35] = "pp --> Tbq --> tZbq --> E_T + j"
            self.energy[35] = 13
            self.luminosity[35] = 139

            self.key[36] = '09743f4c'
            self.label[36] = 'arXiv:1812.09743'
            self.expt[36] = 'ATLAS'
            self.file_name[36] = '1812.09743_ATLAS_Fig4c_pp_Tbq_Wb_Ht_Zt_singlet.txt'
            self.process[36] = "pp --> Tbq --> tZbq --> E_T + j"
            self.energy[36] = 13
            self.luminosity[36] = 36.1

            self.key[37] = '07045f8a'
            self.label[37] = 'arXiv:2201.07045'
            self.expt[37] = 'ATLAS'
            self.file_name[37] = '2201.07045_ATLAS_Fig8-a_pp_TT_tH_k_T-0.1_singlet.txt'
            self.process[37] = "pp --> Tbq --> tHbq --> j"
            self.energy[37] = 13
            self.luminosity[37] = 139

            self.key[38] = '07045f8b'
            self.label[38] = 'arXiv:2201.07045'
            self.expt[38] = 'ATLAS'
            self.file_name[38] = '2201.07045_ATLAS_Fig8-b_pp_TT_tH_k_T-0.3_singlet.txt'
            self.process[38] = "pp --> Tbq --> tHbq --> j"
            self.energy[38] = 13
            self.luminosity[38] = 139
            
            self.key[39] = '07045f8c'
            self.label[39] = 'arXiv:2201.07045'
            self.expt[39] = 'ATLAS'
            self.file_name[39] = '2201.07045_ATLAS_Fig8-c_pp_TT_tH_k_T-0.5_singlet.txt'
            self.process[39] = "pp --> Tbq --> tHbq --> j"
            self.energy[39] = 13
            self.luminosity[39] = 139
            
            self.key[40] = '07045f8d'
            self.label[40] = 'arXiv:2201.07045'
            self.expt[40] = 'ATLAS'
            self.file_name[40] = '2201.07045_ATLAS_Fig8-d_pp_TT_tH_k_T-0.7_singlet.txt'
            self.process[40] = "pp --> Tbq --> tHbq --> j"
            self.energy[40] = 13
            self.luminosity[40] = 139
            
            self.key[41] = '07045f8e'
            self.label[41] = 'arXiv:2201.07045'
            self.expt[41] = 'ATLAS'
            self.file_name[41] = '2201.07045_ATLAS_Fig8-e_pp_TT_tH_k_T-0.9_singlet.txt'
            self.process[41] = "pp --> Tbq --> tHbq --> j"
            self.energy[41] = 13
            self.luminosity[41] = 139
            
            self.key[42] = '07045f8f'
            self.label[42] = 'arXiv:2201.07045'
            self.expt[42] = 'ATLAS'
            self.file_name[42] = '2201.07045_ATLAS_Fig8-f_pp_TT_tH_k_T-1.1_singlet.txt'
            self.process[42] = "pp --> Tbq --> tHbq --> j"
            self.energy[42] = 13
            self.luminosity[42] = 139

            self.key[43] = '07584f8a'
            self.label[43] = 'arXiv:2307.07584'
            self.expt[43] = 'ATLAS'
            self.file_name[43] = '2307.07584_ATLAS_Fig8a_pp_T_Wb_Ht_Zt_singlet_k03.txt'
            self.process[43] = "pp --> Tb(t)q --> tZbq --> l+l- + l+l+l-"
            self.energy[43] = 13
            self.luminosity[43] = 139

            self.key[44] = '07584f8c'
            self.label[44] = 'arXiv:2307.07584'
            self.expt[44] = 'ATLAS'
            self.file_name[44] = '2307.07584_ATLAS_Fig8c_pp_T_Wb_Ht_Zt_singlet_k05.txt'
            self.process[44] = "pp --> Tb(t)q --> tZbq --> l+l- + l+l+l-"
            self.energy[44] = 13
            self.luminosity[44] = 139

            self.key[45] = '07584f8e'
            self.label[45] = 'arXiv:2307.07584'
            self.expt[45] = 'ATLAS'
            self.file_name[45] = '2307.07584_ATLAS_Fig8e_pp_T_Wb_Ht_Zt_singlet_k07.txt'
            self.process[45] = "pp --> Tb(t)q --> tZbq --> l+l- + l+l+l-"
            self.energy[45] = 13
            self.luminosity[45] = 139

            for i in range(len(self.key)):
                if self.expt[i] == 'ATLAS':
                    current_path = os.getcwd()
                    file_path = current_path + '/ATLAS_Tables/' + self.file_name[i]
                    data = np.loadtxt(file_path)
                    self.MT[i] = data[:, 0]
                    self.obs[i] = data[:, 1]
                    self.exp[i] = data[:, 2]
                else:
                    current_path = os.getcwd()
                    file_path = current_path + '/CMS_Tables/' + self.file_name[i]
                    data = np.loadtxt(file_path)
                    self.MT[i] = data[:, 0]
                    self.obs[i] = data[:, 1]
                    self.exp[i] = data[:, 2]

        elif self.m.model() == 'Doublet':
   
            number_of_atlas_cms_tables = 30

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

            self.key[0] = '10751'
            self.label[0] = 'arXiv:1705.10751'
            self.expt[0] = 'ATLAS'
            self.file_name[0] = '1705.10751_ATLAS_fig6c_pp_TT_Doublet.txt'
            self.process[0] = 'pp --> TT --> Zt + X -> l+ + E_T + j'
            self.energy[0] = 13
            self.luminosity[0] = 36.1

            self.key[1] = '07327'
            self.label[1] = 'arXiv:2209.07327'
            self.expt[1] = 'CMS'
            self.file_name[1] = '2209.07327_CMS_f9b_pp_TTbar_Doublet.txt'
            self.process[1] = 'pp --> TT --> l+ + l+l+ + l+l+l-'
            self.energy[1] = 13
            self.luminosity[1] = 138

            self.key[2] = '05263'
            self.label[2] = 'arXiv:2212.05263'
            self.expt[2] = 'ATLAS'
            self.file_name[2] = '2212.05263_ATLAS_fig7e_pp_TT_Zt_T,B_or_X,T_Doublet.txt'
            self.process[2] = 'pp --> TT --> Zt + X -> l+ + E_T + j'
            self.energy[2] = 13
            self.luminosity[2] = 36.1

            self.key[3] = '10555'
            self.label[3] = 'arXiv:1806.10555'
            self.expt[3] = 'ATLAS'
            self.file_name[3] = '1806.10555_ATLAS_Fig-13_c_pp_TT_Zt_doublet.txt'
            self.process[3] = 'pp --> TT --> Zt + X -> l+l- + l+l+l-'
            self.energy[3] = 13
            self.luminosity[3] = 139

            self.key[4] = '04758'
            self.label[4] = 'arXiv:1805.04758'
            self.expt[4] = 'CMS'
            self.file_name[4] = '1805.04758_CMS_Fig8-upper-row-right_pp_TT_Zt_tH_Doublet.txt'
            self.process[4] = 'pp --> TT --> l+ + l+l+ + l+l+l-'
            self.energy[4] = 13
            self.luminosity[4] = 35.9

            self.key[5] = '00999f10b'
            self.label[5] = 'arXiv:1612.00999'
            self.expt[5] = 'CMS'
            self.file_name[5] = '1612.00999_CMS_Fig10-right_pp_Ttq_tH.txt'
            self.process[5] = 'pp --> Ttq --> tHtq --> l+ + E_T + j'
            self.energy[5] = 13
            self.luminosity[5] = 2.3

            self.key[6] = '03408'
            self.label[6] = 'arXiv:1706.03408'
            self.expt[6] = 'CMS'
            self.file_name[6] = '1706.03408_CMS_Fig-12-right_pp_TT_Zt_tH_Doublet.txt'
            self.process[6] = 'pp --> TT --> l+ + E_T + j'
            self.energy[6] = 13
            self.luminosity[6] = 2.6

            self.key[7] = '01062f5b'
            self.label[7] = 'arXiv:1708.01062'
            self.expt[7] = 'CMS'
            self.file_name[7] = '1708.01062_CMS_Fig5-right_pp_Ttq_tZtq_Doublet-RH.txt'
            self.process[7] = 'pp --> Ttq --> tZtq --> l+l- + j'
            self.energy[7] = 13
            self.luminosity[7] = 35.9

            self.key[8] = '04758'
            self.label[8] = 'arXiv:1805.04758'
            self.expt[8] = 'CMS'
            self.file_name[8] = '1805.04758_CMS_Fig8-upper-row-right_pp_TT_Zt_tH_Doublet.txt'
            self.process[8] = 'pp --> TT --> l+ + l+l+ + l+l+l-'
            self.energy[8] = 13
            self.luminosity[8] = 35.9

            #doublet (T, B)
            self.key[9] = '5500fd'
            self.label[9] = 'arXiv:1409.5500'
            self.expt[9] = 'ATLAS'
            self.file_name[9] = '1409.5500_ATLAS_Fig-12-d_pp_TT_Zt_doublet.txt'
            self.process[9] = 'pp --> TT --> Zt + X -> l+l- + l+l+l-'
            self.energy[9] = 8
            self.luminosity[9] = 20.3
            #T, B model
            self.key[10] = '04721f10b'
            self.label[10] = 'arXiv:1909.04721'
            self.expt[10] = 'CMS'
            self.file_name[10] = '1909.04721_CMS_Fig10_upper-row-right_pp_Ttq_tHtq.txt'
            self.process[10] = 'pp --> Ttq --> tHtq --> j'
            self.energy[10] = 13
            self.luminosity[10] = 35.9

            self.key[11] = '04721f10a'
            self.label[11] = 'arXiv:1909.04721'
            self.expt[11] = 'CMS'
            self.file_name[11] = '1909.04721_CMS_Fig10_upper-row-left_pp_Ttq_tHtq.txt'
            self.process[11] = 'pp --> Ttq --> tHtq --> j'
            self.energy[11] = 13
            self.luminosity[11] = 35.9

            self.key[12] = '04721f10d'
            self.label[12] = 'arXiv:1909.04721'
            self.expt[12] = 'CMS'
            self.file_name[12] = '1909.04721_CMS_Fig10_middle-row-right_pp_Ttq_tZtq.txt'
            self.process[12] = 'pp --> Ttq --> tZtq --> j'
            self.energy[12] = 13
            self.luminosity[12] = 35.9

            self.key[13] = '04721f10c'
            self.label[13] = 'arXiv:1909.04721'
            self.expt[13] = 'CMS'
            self.file_name[13] = '1909.04721_CMS_Fig10_middle-row-left_pp_Ttq_tZtq.txt'
            self.process[13] = 'pp --> Ttq --> tZtq --> j'
            self.energy[13] = 13
            self.luminosity[13] = 35.9

            self.key[14] = '04721f10f'
            self.label[14] = 'arXiv:1909.04721'
            self.expt[14] = 'CMS'
            self.file_name[14] = '1909.04721_CMS_Fig10_lower-row-right_pp_Ttq_tH-tZ_tq.txt'
            self.process[14] = 'pp --> Ttq --> (tZ + tH)tq --> j'
            self.energy[14] = 13
            self.luminosity[14] = 35.9

            self.key[15] = '04721f10e'
            self.label[15] = 'arXiv:1909.04721'
            self.expt[15] = 'CMS'
            self.file_name[15] = '1909.04721_CMS_Fig10_lower-row-left_pp_Ttq_tH-tZ_tq.txt'
            self.process[15] = 'pp --> Ttq --> (tZ + tH)tq --> j'
            self.energy[15] = 13
            self.luminosity[15] = 35.9

            self.key[16] = '04721f11b'
            self.label[16] = 'arXiv:1909.04721'
            self.expt[16] = 'CMS'
            self.file_name[16] = '1909.04721_CMS_Fig11_upper-row-right_pp_Ttq_tHtq.txt'
            self.process[16] = 'pp --> Ttq --> tHtq --> j'
            self.energy[16] = 13
            self.luminosity[16] = 35.9

            self.key[17] = '04721f11a'
            self.label[17] = 'arXiv:1909.04721'
            self.expt[17] = 'CMS'
            self.file_name[17] = '1909.04721_CMS_Fig11_upper-row-left_pp_Ttq_tHtq.txt'
            self.process[17] = 'pp --> Ttq --> tHtq --> j'
            self.energy[17] = 13
            self.luminosity[17] = 35.9

            self.key[18] = '04721f11d'
            self.label[18] = 'arXiv:1909.04721'
            self.expt[18] = 'CMS'
            self.file_name[18] = '1909.04721_CMS_Fig11_middle-row-right_pp_Ttq_tZtq.txt'
            self.process[18] = 'pp --> Ttq --> tZtq --> j'
            self.energy[18] = 13
            self.luminosity[18] = 35.9

            self.key[19] = '04721f11c'
            self.label[19] = 'arXiv:1909.04721'
            self.expt[19] = 'CMS'
            self.file_name[19] = '1909.04721_CMS_Fig11_middle-row-left_pp_Ttq_tZtq.txt'
            self.process[19] = 'pp --> Ttq --> tZtq --> j'
            self.energy[19] = 13
            self.luminosity[19] = 35.9

            self.key[20] = '04721f11e'
            self.label[20] = 'arXiv:1909.04721'
            self.expt[20] = 'CMS'
            self.file_name[20] = '1909.04721_CMS_Fig11_lower-row-left_pp_Ttq_tZ-tH_tq.txt'
            self.process[20] = 'pp --> Ttq --> (tZ + tH)tq --> j'
            self.energy[20] = 13
            self.luminosity[20] = 35.9

            self.key[21] = '04721f11f'
            self.label[21] = 'arXiv:1909.04721'
            self.expt[21] = 'CMS'
            self.file_name[21] = '1909.04721_CMS_Fig11_lower-row-right_pp_Ttq_tZ-tH_tq.txt'
            self.process[21] = 'pp --> Ttq --> (tZ + tH)tq --> j'
            self.energy[21] = 13
            self.luminosity[21] = 35.9

            self.key[22] = '07409f4b'
            self.label[22] = 'arXiv:1701.07409'
            self.expt[22] = 'CMS'
            self.file_name[22] = '1701.07409_CMS_Fig4right_pp_Tt_tZ_doublet.txt'
            self.process[22] = 'pp --> Ttq --> tZtq --> l+l- + j'
            self.energy[22] = 13
            self.luminosity[22] = 2.3

            self.key[23] = '04306fc'
            self.label[23] = 'arXiv:1505.04306'
            self.expt[23] = 'ATLAS'
            self.file_name[23] = '1505.04306_ATLAS_Fig18-c_pp_TT_Ht+X_Doublet.txt'
            self.process[23] = 'pp --> TT --> Ht + X --> l+ + E_T + j'
            self.energy[23] = 8
            self.luminosity[23] = 20.3

            #doublet (T, B)
            self.key[24] = '03401f12a'
            self.label[24] = 'arXiv:2305.03401'
            self.expt[24] = 'ATLAS'
            self.file_name[24] = '2305.03401_ATLAS_Fig12a_pp_Tqt_Ht_Zt_doublet-k02.txt'
            self.process[24] = 'pp --> Ttq --> tZ(H)tq --> l+ + E_T + j'
            self.energy[24] = 13
            self.luminosity[24] = 139

            self.key[25] = '03401f12b'
            self.label[25] = 'arXiv:2305.03401'
            self.expt[25] = 'ATLAS'
            self.file_name[25] = '2305.03401_ATLAS_Fig12b_pp_Tqt_Ht_Zt_doublet-k04.txt'
            self.process[25] = 'pp --> Ttq --> tZ(H)tq --> l+ + E_T + j'
            self.energy[25] = 13
            self.luminosity[25] = 139

            self.key[26] = '03401f12c'
            self.label[26] = 'arXiv:2305.03401'
            self.expt[26] = 'ATLAS'
            self.file_name[26] = '2305.03401_ATLAS_Fig12c_pp_Tqt_Ht_Zt_doublet-k06.txt'
            self.process[26] = 'pp --> Ttq --> tZ(H)tq --> l+ + E_T + j'
            self.energy[26] = 13
            self.luminosity[26] = 139

            self.key[27] = '07584f8b'
            self.label[27] = 'arXiv:2307.07584'
            self.expt[27] = 'ATLAS'
            self.file_name[27] = '2307.07584_ATLAS_Fig8b_pp_T_Ht_Zt_doublet_k03.txt'
            self.process[27] = "pp --> Ttq --> tZtq --> l+l- + l+l-l"
            self.energy[27] = 13
            self.luminosity[27] = 139

            self.key[28] = '07584f8d'
            self.label[28] = 'arXiv:2307.07584'
            self.expt[28] = 'ATLAS'
            self.file_name[28] = '2307.07584_ATLAS_Fig8d_pp_T_Ht_Zt_doublet_k05.txt'
            self.process[28] = "pp --> Ttq --> tZtq --> l+l- + l+l-l"
            self.energy[28] = 13
            self.luminosity[28] = 139

            self.key[29] = '07584f8f'
            self.label[29] = 'arXiv:2307.07584'
            self.expt[29] = 'ATLAS'
            self.file_name[29] = '2307.07584_ATLAS_Fig8f_pp_T_Ht_Zt_doublet_k07.txt'
            self.process[29] = "pp --> Ttq --> tZtq --> l+l- + l+l-l"
            self.energy[29] = 13
            self.luminosity[29] = 139

            for i in range(len(self.key)):
                if self.expt[i] == 'ATLAS':
                    current_path = os.getcwd()
                    file_path = current_path + '/ATLAS_Tables/' + self.file_name[i]
                    data = np.loadtxt(file_path)
                    self.MT[i] = data[:, 0]
                    self.obs[i] = data[:, 1]
                    self.exp[i] = data[:, 2]
                else:
                    current_path = os.getcwd()
                    file_path = current_path + '/CMS_Tables/' + self.file_name[i]
                    data = np.loadtxt(file_path)
                    self.MT[i] = data[:, 0]
                    self.obs[i] = data[:, 1]
                    self.exp[i] = data[:, 2]
      
        elif self.m.model() == 'Pure':
   
            number_of_atlas_cms_tables = 17

            self.file_name = [None]*number_of_atlas_cms_tables
            self.key = [None]*number_of_atlas_cms_tables
            self.label = [None]*number_of_atlas_cms_tables
            self.expt = [None]*number_of_atlas_cms_tables
            self.MT = [None]*number_of_atlas_cms_tables
            self.obs = [None]*number_of_atlas_cms_tables
            self.exp = [None]*number_of_atlas_cms_tables
            self.process = [None]*number_of_atlas_cms_tables
            self.energy = [None] * number_of_atlas_cms_tables
            self.luminosity = [None] * number_of_atlas_cms_tables

            self.key[0] = '05263'
            self.label[0] = 'arXiv:2212.05263'
            self.expt[0] = 'ATLAS'
            self.file_name[0] = '2212.05263_ATLAS_fig7a_pp_TT_tZ.txt'
            self.process[0] = 'pp --> TT --> Zt + X -> l+ + E_T + j'
            self.energy[0] = 13
            self.luminosity[0] = 139

            self.key[1] = '97680'
            self.label[1] = 'arXiv:1812.09768'
            self.expt[1] = 'CMS'
            self.file_name[1] = '1812.09768_CMS_fig4a_pp_TT_tZ.txt'
            self.process[1] = 'pp --> TT --> Zt + X -> l+l- + j'
            self.energy[1] = 13
            self.luminosity[1] = 36.1

            self.key[2] = '10751fig6a'
            self.label[2] = 'arXiv:1705.10751'
            self.expt[2] = 'ATLAS'
            self.file_name[2] = '1705.10751_ATLAS_fig6a_pp_TT_Zt.txt'
            self.process[2] = 'pp --> TT --> Zt + X -> l+ + E_T + j'
            self.energy[2] = 13
            self.luminosity[2] = 36.1

            self.key[3] = '17710'
            self.label[3] = 'arXiv:1808.01771'
            self.expt[3] = 'ATLAS'
            self.file_name[3] = '1808.01771_ATLAS_fig13a_pp_TT_Ht.txt'
            self.process[3] = 'pp --> TT --> tHtH --> j'
            self.energy[3] = 13
            self.luminosity[3] = 36.1

            self.key[4] = '19520'
            self.label[4] = 'arXiv:1503.01952'
            self.expt[4] = 'CMS'
            self.file_name[4] = '1503.01952_CMS_fig13_pp_TT_tH.txt'
            self.process[4] = 'pp --> TT --> tHtH --> j'
            self.energy[4] = 8
            self.luminosity[4] = 19.7

            self.key[5] = '33470fig4a'
            self.label[5] = 'arXiv:1707.03347'
            self.expt[5] = 'ATLAS'
            self.file_name[5] = '1707.03347_ATLAS_fig4a_pp_TT_Wb.txt'
            self.process[5] = 'pp --> TT --> Wb + X --> l+ + E_T + j'
            self.energy[5] = 13
            self.luminosity[5] = 36.1

            self.key[6] = '10555'
            self.label[6] = 'arXiv:1806.10555'
            self.expt[6] = 'ATLAS'
            self.file_name[6] = '1806.10555_ATLAS_Fig-13e_pp_TT_Zt.txt'
            self.process[6] = 'pp --> TT --> Zt + X -> l+l- + l+l+l-'
            self.energy[6] = 13
            self.luminosity[6] = 36.1

            self.key[7] = '08328'
            self.label[7] = 'arXiv:1701.08328'
            self.expt[7] = 'CMS'
            self.file_name[7] = '1701.08328_CMS_fig5_pp_Tbq_or_Ybq_bW.txt'
            self.process[7] = 'pp --> Tbq --> bWbq --> l+ + E_T + j'
            self.energy[7] = 13
            self.luminosity[7] = 2.3

            self.key[8] = '04177'
            self.label[8] = 'arXiv:1509.04177'
            self.expt[8] = 'CMS'
            self.file_name[8] = '1509.04177_CMS_fig8_pp_TT_bW.txt'
            self.process[8] = 'pp --> TT --> WbWb --> l+ + l+l+ + l+l+l- + l+l- + j'
            self.energy[8] = 8
            self.luminosity[8] = 19.7

            self.key[9] = '04177'
            self.label[9] = 'arXiv:1509.04177'
            self.expt[9] = 'CMS'
            self.file_name[9] = '1509.04177_CMS_fig8_pp_TT_tH.txt'
            self.process[9] = 'pp --> TT --> tHtH --> l+ + l+l+ + l+l+l- + gamma + j'
            self.energy[9] = 8
            self.luminosity[9] = 19.7

            self.key[10] = '04177'
            self.label[10] = 'arXiv:1509.04177'
            self.expt[10] = 'CMS'
            self.file_name[10] = '1509.04177_CMS_fig8_pp_TT_tZ.txt'
            self.process[10] = 'pp --> TT --> tZtZ --> l+ + l+l- + l+l+ + l+l+l- + j'
            self.energy[10] = 8
            self.luminosity[10] = 19.7

            self.key[11] = '03408'
            self.label[11] = 'arXiv:1706.03408'
            self.expt[11] = 'CMS'
            self.file_name[11] = '1706.03408_CMS_Fig-11-left_pp_TT_bW.txt'
            self.process[11] = 'pp --> TT --> WbWb --> l+'
            self.energy[11] = 13
            self.luminosity[11] = 2.6

            self.key[12] = '03408'
            self.label[12] = 'arXiv:1706.03408'
            self.expt[12] = 'CMS'
            self.file_name[12] = '1706.03408_CMS_Fig-11-right_pp_TT_tH.txt'
            self.process[12] = 'pp --> TT --> tHtH --> l+'
            self.energy[12] = 13
            self.luminosity[12] = 2.6

            self.key[13] = '0471fa'
            self.label[13] = 'arXiv:1209.0471'
            self.expt[13] = 'CMS'
            self.file_name[13] = '1209.0471_CMS_Fig6_upper_pp_TT_bW.txt'
            self.process[13] = 'pp --> TT --> WbWb --> e + j'
            self.energy[13] = 13
            self.luminosity[13] = 2.6

            self.key[14] = '0471fb'
            self.label[14] = 'arXiv:1209.0471'
            self.expt[14] = 'CMS'
            self.file_name[14] = '1209.0471_CMS_Fig6_middle_pp_TT_bW.txt'
            self.process[14] = 'pp --> TT --> WbWb --> mu + j'
            self.energy[14] = 7
            self.luminosity[14] = 5

            self.key[15] = '0471fc'
            self.label[15] = 'arXiv:1209.0471'
            self.expt[15] = 'CMS'
            self.file_name[15] = '1209.0471_CMS_Fig6_lower_pp_TT_bW.txt'
            self.process[15] = 'pp --> TT --> WbWb --> e + E_T + j'
            self.energy[13] = 7
            self.luminosity[13] = 5

            self.key[16] = '04306fa'
            self.label[16] = 'arXiv:1505.04306'
            self.expt[16] = 'CMS'
            self.file_name[16] = '1505.04306_ATLAS_Fig18-a_pp_TT_Wb+X.txt'
            self.process[16] = 'pp --> TT --> WbWb --> l + j'
            self.energy[16] = 8
            self.luminosity[16] = 20.3

            for i in range(len(self.key)):
                if self.expt[i] == 'ATLAS':
                    current_path = os.getcwd()
                    file_path = current_path + '/ATLAS_Tables/' + self.file_name[i]
                    data = np.loadtxt(file_path)
                    self.MT[i] = data[:, 0]
                    self.obs[i] = data[:, 1]
                    self.exp[i] = data[:, 2]
                else:
                    current_path = os.getcwd()
                    file_path = current_path + '/CMS_Tables/' + self.file_name[i]
                    data = np.loadtxt(file_path)
                    self.MT[i] = data[:, 0]
                    self.obs[i] = data[:, 1]
                    self.exp[i] = data[:, 2]

        else:
            raise Exception("Error in model choice")

    def all_processes(self):
        with open("processes.dat", "w") as f:
            f.write("process energy experiment  process_number identifier\n")
            for i in range(len(self.key)):
                f.write(f"{self.process[i]} {self.energy[i]} {self.expt[i]} {self.label[i]} {i}\n")

    def cs_dict(self):
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
