from manip import TheoryCalc
from model import *
from utils import *
from coupling import Coupling
import pandas as pd


class PyTop(Coupling):
    def __init__(self, m):
        if isinstance(m, Singlet) or isinstance(m, Doublet) or isinstance(m, PureDecay):
            TheoryCalc.__init__(self, m)
            Coupling.__init__(self, m)
            self.m = m
            self.df = c.df

    def filling_channels_data(self):
        self.initialize_tables_cms_and_atlas()
        self.all_processes()
        self.cs_dict()
        self.tb_xt_dict()

    def filling_couplings_data(self):
        self.fill_coupling_tables()
        self.all_couplings()
        self.fill_sin_and_kappa()

    def check_singlet_limit(self, m, vv, vbq, vtq, sin_l, r=None):
        if isinstance(self.m, Singlet):
            check_mass_range(m)
            check_sin(sin_l)
            try:
                validate_cross_section_value(vv)
                validate_cross_section_value(vbq)
                validate_cross_section_value(vtq)
            except Exception as e:
                print(e)
                if vbq < 0:
                    vbq = -1
                if vtq < 0:
                    vtq = -1
                if vv < 0:
                    vv = -1
            self.m = Singlet(m, vv, vbq, vtq, sin_l, r)
        else:
            raise Exception('Invalid model. Must be a singlet')

        self.check_channel()
        print(self)
        i = self.channel
        pred_cs = self.numerator(i)
        obs_cs = (1 / self.model_observed_ratio) * self.numerator(i)
        self.df = df_making(self.df, mass=self.m.mv(), coupling=self.m.universal_coupling(), predicted_cs=pred_cs,
                            observed_cs=obs_cs, width=self.m.get_width_mass_ratio(), result=self.allowed_or_excluded,
                            channel=i, obs_ratio=self.model_observed_ratio, process=self.process[i],
                            luminosity=self.luminosity[i], energy=self.energy[i], label=self.label[i],
                            model=self.m.model())

    def check_doublet_limit(self, m, pp_vv, pp_vtq, sin_r):
        if isinstance(self.m, Doublet):
            check_mass_range(m)
            check_sin(sin_r)
            try:
                validate_cross_section_value(pp_vv)
                validate_cross_section_value(pp_vtq)
            except Exception as e:
                print(e)
                if pp_vtq < 0:
                    pp_vtq = -1
                if pp_vv < 0:
                    pp_vv = -1
            self.m = Doublet(m, pp_vv, pp_vtq, sin_r)
        else:
            raise Exception('Invalid model. Must be a doublet')
        self.check_channel()
        if self.m.get_sin_up_right() is None:
            print("Warning: (T, B) couplings are not set. Doublet (T, B) "
                  "single production cross sections will not be checked.")
        print(self)
        i = self.channel
        self.df = df_making(self.df, mass=self.m.mv(), coupling=self.m.universal_coupling(),
                            width=self.m.get_width_mass_ratio(), result=self.allowed_or_excluded, channel=i,
                            obs_ratio=self.model_observed_ratio, process=self.process[i],
                            luminosity=self.luminosity[i], energy=self.energy[i],
                            label=self.label[i], model=self.m.model(), which_doublet=self.m.which_d)

    def check_TB_doublet_limit(self, m, pp_vv, pp_vtq, sin_r, sin_u_r, sin_d_r):
        if isinstance(self.m, Doublet):
            check_mass_range(m)
            #check_sin(sin_r)
            check_sin(sin_u_r)
            #check_sin(sin_d_r)
            try:
                validate_cross_section_value(pp_vv)
                validate_cross_section_value(pp_vtq)
            except Exception as e:
                print(e)
                if pp_vtq < 0:
                    pp_vtq = -1
                if pp_vv < 0:
                    pp_vv = -1
            self.m = Doublet(m, pp_vv, pp_vtq, sin_r)
            self.m.set_sin_up_right(sin_u_r)
            self.m.set_sin_down_right(sin_d_r)
            self.m.change_to_tb_doublet()
        else:
            raise Exception('Invalid model. Must be a doublet')
        self.check_channel()
        if self.m.get_sin_up_right() is None:
            print("Warning (T, B) coupling are not set, "
                  "doublet (T, B) pair and single production cross sections will not be checked")
        print(self)
        i = self.channel
        self.df = df_making(self.df, mass=self.m.mv(), coupling=self.m.universal_coupling(),
                            width=self.m.get_width_mass_ratio(), result=self.allowed_or_excluded, channel=i,
                            obs_ratio=self.model_observed_ratio, process=self.process[i],
                            luminosity=self.luminosity[i], energy=self.energy[i],
                            label=self.label[i], model=self.m.model(), which_doublet=self.m.which_d)

    def check_pure_limit(self, m, pp_vv, pp_vbq):
        if isinstance(self.m, PureDecay):
            check_mass_range(m)
            try:
                validate_cross_section_value(pp_vv)
                validate_cross_section_value(pp_vbq)
            except Exception as e:
                print(e)
                if pp_vbq < 0:
                    pp_vbq = -1
                elif pp_vv < 0:
                    pp_vv = -1
            self.m = PureDecay(m, pp_vv, pp_vbq)
        else:
            raise Exception('Invalid model. Must be PureDecay class')
        self.check_channel()
        print(self)
        i = self.channel
        self.df = df_making(self.df, mass=self.m.mv(), result=self.allowed_or_excluded, channel=i,
                            obs_ratio=self.model_observed_ratio, process=self.process[i],
                            luminosity=self.luminosity[i], energy=self.energy[i],
                            label=self.label[i], model=self.m.model())

    def check_coupling_limit(self, m, sin_l):
        if isinstance(self.m, Doublet) or isinstance(self.m, Singlet):
            check_mass_range(m)
            check_sin(sin_l)
            if self.m.model() == 'Singlet':
                self.m = Singlet(m, None, None, None, sin_l)
            else:
                self.m = Doublet(m, None, None, sin_l)

        else:
            raise Exception('Invalid model. Must be a Singlet or Doublet')
        self.coupling_limit()
        print(self)
