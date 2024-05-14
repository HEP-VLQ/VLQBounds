import numpy as np
from scipy.interpolate import interp1d 
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
        r = self.m.get_width_mass_ratio_from_wb() #which ratio wb or zt or ht
        kappa = self.m.universal_coupling()
        return r, kappa

    def singlet_single_prod_calc(self):
        """single production of T associated with bq or tq (pp->Tb(t)q)"""

        pp_vbq_bwbq = self.m.vbq() * self.m.br_vbw()
        pp_vbq_tzbq = self.m.vbq() * self.m.br_vzt()
        pp_vbq_thbq = self.m.vbq() * self.m.br_vht()

        pp_vtq_tztq = self.m.vtq() * self.m.br_vzt()

        # 2201.02227 2402.16561 1812.09743
        vb_z_nu = pp_vbq_tzbq * c.BR_Z_nunu * c.BR_t_Wb * c.BR_W_qq
        # 1708.01062  1409.5500 1701.07409
        vb_z_ll = pp_vbq_tzbq * c.BR_Z_ee * c.BR_t_Wb * c.BR_W_qq
        # 2302.12802
        vb_h_ga = pp_vbq_thbq * c.BR_h_gaga * c.BR_t_Wb * c.BR_W_enu
        # 1612.00999 2305.03401
        vb_th_lnub = pp_vbq_thbq * c.BR_t_Wb * c.BR_W_enu * c.BR_h_bb
        # 1909.04721_upper 2201.07045
        vb_h_b = pp_vbq_thbq * c.BR_t_Wb * c.BR_W_qq * c.BR_h_bb
        # 1909.04721_middle
        vb_z_q = pp_vbq_tzbq * c.BR_Z_qq * c.BR_t_Wb * c.BR_W_qq
        # 1909.04721_lower
        combined_1 = vb_z_q + vb_h_b
        # 1602.05606
        vb_v_wb = pp_vbq_bwbq * c.BR_W_enu
        # 2307.07584
        vt_z_ll = pp_vtq_tztq * c.BR_Z_ee * c.BR_t_Wb * c.BR_W_qq
        vb_z_lll = pp_vbq_tzbq * c.BR_Z_ee * c.BR_t_Wb * c.BR_W_enu
        vt_z_lll = pp_vtq_tztq * c.BR_Z_ee * c.BR_t_Wb * c.BR_W_enu

        combined_2 = vb_z_ll + vb_z_lll + vt_z_ll + vt_z_lll

        return vb_z_nu, vb_z_ll, vb_z_q, vb_h_b, vb_h_ga, vb_th_lnub, vb_v_wb, combined_1, combined_2

    def doublet_single_prod_calc(self):
        # single production of T associated with tq (pp->Ttq)
        pp_vtq_tztq = self.m.vtq() * self.m.br_vzt()
        pp_vtq_thtq = self.m.vtq() * self.m.br_vht()

        # 1612.00999 2305.03401
        vt_th_lnub = pp_vtq_thtq * c.BR_t_Wb * c.BR_W_enu * c.BR_h_bb
        # 1708.01062 1701.07409
        vt_z_l = pp_vtq_tztq * c.BR_Z_ee * c.BR_t_Wb * c.BR_W_qq
        # 1909.04721 upper
        vt_h_b = pp_vtq_thtq * c.BR_t_Wb * c.BR_W_qq * c.BR_h_bb
        # 1909.04721 middle
        vt_z_q = pp_vtq_tztq * c.BR_Z_qq * c.BR_t_Wb * c.BR_W_qq
        # 1909.04721 lower
        combined_3 = vt_h_b + vt_z_q
        # 2307.07584
        vt_z_lll = pp_vtq_tztq * c.BR_Z_ee * c.BR_t_Wb * c.BR_W_enu
        combined_4 = vt_z_l + vt_z_lll

        return vt_th_lnub, vt_z_l, vt_h_b, vt_z_q, combined_3, combined_4

    def doublet_tb_single_prod_calc(self):
        if self.m.get_sin_up_right() is not None:
            pp_vtq_tztq = self.m.vtq() * self.m.br_vzt_tb_doublet()
            pp_vtq_thtq = self.m.vtq() * self.m.br_vht_tb_doublet()

            # 1909.04721 upper
            vt_h_b = pp_vtq_thtq * c.BR_t_Wb * c.BR_W_qq * c.BR_h_bb
            # 1909.04721 middle
            vt_z_q = pp_vtq_tztq * c.BR_Z_qq * c.BR_t_Wb * c.BR_W_qq
            # 1909.04721 lower
            combined_3 = vt_h_b + vt_z_q
            # 2305
            vt_th_lnub = pp_vtq_thtq * c.BR_t_Wb * c.BR_W_enu * c.BR_h_bb

            return vt_h_b, vt_z_q, combined_3, vt_th_lnub
        else:
            return -1, -1, -1, -1

    def pair_prod_calc(self):
        # 1706.03408
        htht_e = (self.m.vv() * self.m.br_vht() * self.m.br_vht() * c.BR_t_Wb ** 2
                  * c.BR_h_bb * c.BR_h_bb * c.BR_W_enu * c.BR_W_qq)

        htht_epep = (self.m.vv() * self.m.br_vht() * self.m.br_vht() * (c.BR_h_WW ** 2) * (c.BR_t_Wb ** 2)
                     * c.BR_W_enu ** 2 * (c.BR_W_qq ** 4))
        #1808 1503
        htht_j = (self.m.vv() * self.m.br_vht() * self.m.br_vht() * c.BR_t_Wb ** 2
                  * c.BR_h_bb ** 2 * c.BR_W_qq ** 2)

        htht_gaga = (self.m.vv() * self.m.br_vht() * self.m.br_vht() * c.BR_t_Wb ** 2
                     * c.BR_h_gaga * c.BR_h_bb * c.BR_W_qq * c.BR_W_enu)

        wbht_e = self.m.vv() * self.m.br_vht() * self.m.br_vbw() * c.BR_h_bb * c.BR_t_Wb * c.BR_W_qq * c.BR_W_enu

        ztzt_eee = (self.m.vv() * self.m.br_vzt() * self.m.br_vzt() * c.BR_t_Wb ** 2 * c.BR_Z_ee
                    * c.BR_Z_qq * c.BR_W_qq * c.BR_W_enu)

        combination_1 = wbht_e + htht_epep + ztzt_eee

        ztzt_e = (self.m.vv() * self.m.br_vzt() * self.m.br_vzt() * c.BR_Z_nunu
                  * c.BR_Z_qq * c.BR_t_Wb ** 2 * c.BR_W_enu * c.BR_W_qq)
        # 1706.03406
        wbwb_e = self.m.vv() * self.m.br_vbw() * self.m.br_vbw() * c.BR_W_enu * c.BR_W_qq

        wbwb_mu = self.m.vv() * self.m.br_vbw() * self.m.br_vbw() * c.BR_W_munu * c.BR_W_qq

        wbwb_j = self.m.vv() * self.m.br_vbw() * self.m.br_vbw() * c.BR_W_qq ** 2

        ztzt_epem = (self.m.vv() * self.m.br_vzt() * self.m.br_vzt()
                     * c.BR_Z_ee * c.BR_t_Wb ** 2 * c.BR_W_qq ** 2 * c.BR_Z_qq)

        ztht_eee = self.m.vv() * self.m.br_vzt() * self.m.br_vht() * c.BR_Z_ee * c.BR_t_Wb ** 2 * c.BR_h_bb * c.BR_W_enu

        if self.m.model() == 'Doublet' and self.m.get_sin_up_right() is not None:
            ztzt_epem_from_tb_doublet = (self.m.vv() * self.m.br_vzt_tb_doublet() * self.m.br_vzt_tb_doublet()
                                         * c.BR_Z_ee * c.BR_t_Wb ** 2 * c.BR_W_qq ** 2 * c.BR_Z_qq)
            ztht_eee_from_tb_doublet = (self.m.vv() * self.m.br_vzt_tb_doublet() * self.m.br_vht_tb_doublet() *
                                        c.BR_Z_ee * c.BR_t_Wb ** 2 * c.BR_h_bb * c.BR_W_enu)
            combination_2_tb = ztzt_epem_from_tb_doublet + ztht_eee_from_tb_doublet
        else:
            combination_2_tb = -1

        combination_2 = ztzt_epem + ztht_eee

        combination_3 = htht_e + wbwb_e

        # 1509.04177
        combination_4 = wbwb_e + ztzt_epem + htht_epep + ztzt_eee + htht_j + htht_gaga + wbwb_j

        return (ztzt_e, ztzt_eee, wbwb_e, wbwb_mu, ztzt_epem, htht_j, htht_e,
                combination_1, combination_2, combination_2_tb, combination_3, combination_4)
      
    def get_process(self, k, r, pr, kappa):
        if self.m.model() == 'Singlet':
            if k in self.cs_keys['pair_prod']:
                if pr in self.process:
                    index = self.key.index(k)
                    return self.process[index]
                else:
                    raise Exception("pair production are not calculated")

            elif k in self.cs_keys['single_prod']:
                if kappa is not None:
                    if k in c.kappa_keys['k=0.1']["Singlet"] and kappa == 0.1:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.kappa_keys['k=0.2']["Singlet"] and kappa == 0.2:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.kappa_keys['k=0.3']["Singlet"] and kappa == 0.3:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.kappa_keys['k=0.4']["Singlet"] and kappa == 0.4:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.kappa_keys['k=0.5']["Singlet"] and kappa == 0.5:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.kappa_keys['k=0.6']["Singlet"] and kappa == 0.6:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.kappa_keys['k=0.7']["Singlet"] and kappa == 0.7:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.kappa_keys['k=0.9']["Singlet"] and kappa == 0.9:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.kappa_keys['k=1.1']["Singlet"] and kappa == 1.1:
                        index = self.key.index(k)
                        return self.process[index]
                    else:
                        index = self.key.index(k)
                        return self.process[index]
                else:
                    print("universal coupling is None")
                if r is not None:
                    if k in c.ratio_keys['r<=0.05']["Singlet"] and r <= 0.05:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.ratio_keys['r=0.1']["Singlet"] and r == 0.1:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.ratio_keys['r<=0.1']["Singlet"] and r <= 0.1:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.ratio_keys['r=0.2']["Singlet"] and r == 0.2:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.ratio_keys['r=0.3']["Singlet"] and r == 0.3:
                        index = self.key.index(k)
                        return self.process[index]
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
                    if k in c.kappa_keys['k=0.2']["Doublet"] and kappa == 0.2:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.kappa_keys['k=0.3']["Doublet"] and kappa == 0.3:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.kappa_keys['k=0.4']["Doublet"] and kappa == 0.4:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.kappa_keys['k=0.5']["Doublet"] and kappa == 0.5:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.kappa_keys['k=0.6']["Doublet"] and kappa == 0.6:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.kappa_keys['k=0.7']["Doublet"] and kappa == 0.7:
                        index = self.key.index(k)
                        return self.process[index]
                    else:
                        index = self.key.index(k)
                        return self.process[index]
                else:
                    print("universal coupling is None")

                if r is not None:
                    if k in c.ratio_keys['r<=0.05']["Doublet"] and r <= 0.05:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.ratio_keys['r=0.1']["Doublet"] and r == 0.1:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.ratio_keys['r<=0.1']["Doublet"] and r <= 0.1:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.ratio_keys['r=0.2']["Doublet"] and r == 0.2:
                        index = self.key.index(k)
                        return self.process[index]
                    elif k in c.ratio_keys['r=0.3']["Doublet"] and r == 0.3:
                        index = self.key.index(k)
                        return self.process[index]
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

        (ztzt_e, ztzt_eee, wbwb_e, wbwb_mu, ztzt_epem, htht_j, htht_e,
         c1, c2, c_from_tb, c3, c4) = self.pair_prod_calc()

        r, kappa = self.get_ratio_and_universal_coupling()

        if self.m.model() == 'Singlet':
            (vb_z_nu, vb_z_l, vb_z_q, vb_h_b, vb_h_ga, vb_th_lnub, vb_v_wb, combined1,
             combined2) = self.singlet_single_prod_calc()

            if self.get_process(self.key[i], r, self.process[i], kappa) == "pp --> Tbq --> tZbq --> E_T + j":
                return vb_z_nu
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Tbq --> tZbq --> l+l- + j':
                return vb_z_l
            elif self.get_process(self.key[i], r, self.process[i], kappa) == "pp --> Tbq --> tHbq --> j":
                return vb_h_b
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Tbq --> tHbq --> l+ + E_T + j'):
                return vb_th_lnub
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Tbq --> tHbq --> l+ + gamma + E_T + j'):
                return vb_h_ga
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Tbq --> tZbq --> j':
                return vb_z_q
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Tbq --> bWbq --> l+ + E_T + j'):
                return vb_v_wb
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Tbq --> (tZ + tH)bq --> j':
                return combined1
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Tbq --> tZ(H)bq --> l+ + E_T + j'):
                return vb_th_lnub
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  "pp --> Tb(t)q --> tZbq --> l+l- + l+l+l-"):
                return combined2

        if self.m.model() == 'Doublet':

            vt_th_lnub, vt_z_l, vt_h_b, vt_z_q, combined3, combined4 = self.doublet_single_prod_calc()

            vtj_h_b, vtj_z_q, combined_3, vtj_th_lnub = self.doublet_tb_single_prod_calc()

            if self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Ttq --> tZtq --> l+l- + j':
                return vt_z_l
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Ttq --> tHtq --> j':
                if self.key[i] in c.Doublet_TB:
                    return vtj_h_b
                else:
                    return vt_h_b
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Ttq --> tHtq --> l+ + E_T + j'):
                return vt_th_lnub
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Ttq --> tZtq --> j':
                if self.key[i] in c.Doublet_TB:
                    return vtj_z_q
                else:
                    return vt_z_q
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> Ttq --> (tZ + tH)tq --> j':
                if self.key[i] in c.Doublet_TB:
                    return combined_3
                else:
                    return combined3
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> Ttq --> tZ(H)tq --> l+ + E_T + j'):
                if self.key[i] in c.Doublet_TB:
                    return vtj_th_lnub
                else:
                    return vt_th_lnub
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  "pp --> Ttq --> tZtq --> l+l- + l+l-l"):
                return combined4

        if self.m.model() == 'Singlet' or self.m.model() == 'Doublet' or self.m.model() == 'PureDecay':
            if self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> TT --> Zt + X -> l+ + E_T + j':
                return ztzt_e
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> TT --> Wb + X --> l+ + E_T + j'):
                return wbwb_e
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> TT --> l+ + E_T + j':
                return wbwb_e
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> TT --> l+ + l+l+ + l+l+l-':
                return c1
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> TT --> Zt + X -> l+l- + l+l+l-'):
                if self.key[i] in c.Doublet_TB:
                    return c_from_tb
                else:
                    return c2
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> TT --> l+l+ + j':
                return ztzt_eee
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> TT --> Wb + X + Ht + X --> l+ + E_T + j'):
                return c3
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> TT --> Ht + X --> l+ + E_T + j'):
                return htht_e
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> TT --> tHtH --> j':
                return htht_j
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> TT --> WbWb --> l+ + l+l+ + l+l+l- + l+l- + j'):
                return c4
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> TT --> tHtH --> l+ + l+l+ + l+l+l- + gamma + j'):
                return c4
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> TT --> tZtZ --> l+ + l+l- + l+l+ + l+l+l- + j'):
                return c4
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> TT --> WbWb --> l+':
                return wbwb_e
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> TT --> WbWb --> e + j':
                return wbwb_e
            elif self.get_process(self.key[i], r, self.process[i], kappa) == 'pp --> TT --> WbWb --> mu + j':
                return wbwb_mu
            elif (self.get_process(self.key[i], r, self.process[i], kappa) ==
                  'pp --> TT --> WbWb --> e + mu + j'):
                return wbwb_e + wbwb_mu
            elif self.get_process(self.key[i], r, self.process[i], kappa) == '':
                return -1

    def denominator(self, num, index, t):
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

    def expected_ratio_calc(self):
        try:
            maximum = -1000000
            pos = -1
            for index, k in enumerate(self.key):
                n = self.numerator(index)
                d = self.denominator(n, index, self.obs)
                if d == -1 or n == -1:
                    continue
                rat = n/d
                if rat > maximum:
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
