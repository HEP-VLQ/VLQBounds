from manip import TheoryCalc
from model import *
from utils import *
from coupling import Coupling


class PyTop(Coupling):
    def __init__(self, m):
        if isinstance(m, Singlet) or isinstance(m, Doublet) or isinstance(m, PureDecay):
            TheoryCalc.__init__(self, m)
            Coupling.__init__(self, m)
            self.m = m

    def filling_channels_data(self):
        self.initialize_tables_cms_and_atlas()
        self.all_processes()
        self.cs_dict()

    def filling_couplings_data(self):
        self.fill_coupling_tables()
        self.all_couplings()
        self.fill_sin_and_kappa()

    def check_singlet_limit(self, m, vv, vbq, vtq, sin_l):
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
                    vbq = -1
                if vv < 0:
                    vv = -1
            self.m = Singlet(m, vv, vbq, vtq, sin_l)
        else:
            raise Exception('Invalid model. Must be a singlet')

        self.check_channel()
        print(self)

    def check_doublet_limit(self, m, pp_vv, pp_vtq, sin_l):
        if isinstance(self.m, Doublet):
            check_mass_range(m)
            check_sin(sin_l)
            try:
                validate_cross_section_value(pp_vv)
                validate_cross_section_value(pp_vtq)
            except Exception as e:
                print(e)
                if pp_vtq < 0:
                    pp_vtq = -1
                if pp_vv < 0:
                    pp_vv = -1
            self.m = Doublet(m, pp_vv, pp_vtq, sin_l)
        else:
            raise Exception('Invalid model. Must be a doublet')
        self.check_channel()
        if self.m.get_sin_up_right() is None:
            print("Warning (T, B) coupling are not set, "
                  "doublet (T, B) pair and single production cross sections will not be checked")
        print(self)

    def check_doublet_limit_with_TB_doublet(self, m, pp_vv, pp_vtq, sin_l, sin_u_r, sin_d_r):
        if isinstance(self.m, Doublet):
            check_mass_range(m)
            check_sin(sin_l)
            check_sin(sin_u_r)
            check_sin(sin_d_r)
            try:
                validate_cross_section_value(pp_vv)
                validate_cross_section_value(pp_vtq)
            except Exception as e:
                print(e)
                if pp_vtq < 0:
                    pp_vtq = -1
                if pp_vv < 0:
                    pp_vv = -1
            self.m = Doublet(m, pp_vv, pp_vtq, sin_l)
            self.m.set_sin_up_right(sin_u_r)
            self.m.set_sin_down_right(sin_d_r)
        else:
            raise Exception('Invalid model. Must be a doublet')
        self.check_channel()
        if self.m.get_sin_up_right() is None:
            print("Warning (T, B) coupling are not set, "
                  "doublet (T, B) pair and single production cross sections will not be checked")
        print(self)

    def check_pure_limit(self, m, pp_vv, pp_vbq, pp_vtq):
        if isinstance(self.m, PureDecay):
            check_mass_range(m)
            try:
                validate_cross_section_value(pp_vv)
                validate_cross_section_value(pp_vbq)
                validate_cross_section_value(pp_vtq)
            except Exception as e:
                print(e)
                if pp_vbq < 0:
                    pp_vbq = -1
                if pp_vtq < 0:
                    pp_vbq = -1
                if pp_vv < 0:
                    pp_vv = -1
            self.m = PureDecay(m, pp_vv, pp_vbq, pp_vtq)
        else:
            raise Exception('Invalid model. Must be a PureDecay')
        self.check_channel()
        print(self)

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
