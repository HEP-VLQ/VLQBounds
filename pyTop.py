#from manip import TheoryCalc
from model import *
from utils import *
from coupling import Coupling
import math


class PyTop(Coupling):
    def __init__(self, m):
        if isinstance(m, Singlet) or isinstance(m, Doublet) or isinstance(m, PureDecay):
            #TheoryCalc.__init__(self, m)
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

    def singlet_params(self, **kwargs):
        if "mT" not in kwargs or kwargs["mT"] is None:
            raise ValueError("Error, T mass (mT) is not provided")

        check_mass_range(kwargs["mT"])
        self.m.set_mT(kwargs["mT"])

        if "k_T" in kwargs:
            if kwargs["k_T"] is None:
                raise ValueError("Error, coupling strength (k_T) must not be None")
            self.m.set_coupling_strength(abs(kwargs["k_T"]))

        elif "w_m" in kwargs:
            if kwargs["w_m"] is None or kwargs["w_m"] <= 0:
                raise ValueError("Error, width-to-mass ratio (w_m) must be greater than 0")
            self.m.set_width_mass_ratio(kwargs["w_m"])

        elif "s_l" in kwargs:
            if kwargs["s_l"] is None:
                raise ValueError("Error, sin_l (s_l) must not be None")
            check_sin(kwargs["s_l"])
            self.m.set_sin_l(kwargs["s_l"])
        else:
            raise ValueError("Error, input must contain 'k_T', 'w_m', or 's_l' besides 'mT'")

    def doublet_TB_params(self, **kwargs):
        self.m.change_to_TB()
        if "mT" not in kwargs or kwargs["mT"] is None:
            raise ValueError("Error, T mass (mT) is not provided")

        check_mass_range(kwargs["mT"])
        self.m.set_mT(kwargs["mT"])

        if "k_T" in kwargs:
            self.m.set_coupling_strength(kwargs["k_T"])
        elif "w_m" in kwargs:
            if kwargs["w_m"] <= 0:
                raise ValueError("Error, width-to-mass ratio (w_m) must be greater than 0")
            self.m.set_width_mass_ratio(kwargs["w_m"])
        elif "s_u_r" in kwargs:
            check_sin(kwargs["s_u_r"])
            self.m.set_sin_u_r(kwargs["s_u_r"])
        else:
            raise ValueError("Error, input must contain 'k_T', 'w_m', or 's_u_r' besides 'mT'")

    def doublet_XT_params(self, **kwargs):
        if "mT" not in kwargs or kwargs["mT"] is None:
            raise ValueError("Error, T mass (mT) is not provided")

        check_mass_range(kwargs["mT"])
        self.m.set_mT(kwargs["mT"])

        if "k_T" in kwargs:
            self.m.set_coupling_strength(kwargs["k_T"])
        elif "w_m" in kwargs:
            if kwargs["w_m"] <= 0:
                raise ValueError("Error, width-to-mass ratio (w_m) must be greater than 0")
            self.m.set_width_mass_ratio(kwargs["w_m"])
        elif "s_r" in kwargs:
            check_sin(kwargs["s_r"])
            self.m.set_sin_u_r(kwargs["s_r"])
        else:
            raise ValueError("Error, input must contain 'k_T', 'w_m', or 's_r' besides 'mT'")

    def check_singlet_limit(self):
        self.check_channel()
        self.print_result()
        i = self.channel
        xs_theo = self.numerator(i)
        obs_xs = (1 / self.obs_ratio) * self.numerator(i)
        exp_xs = (1 / self.exp_ratio) * self.numerator(i)
        self.df = df_making(self.df, mass=self.m.get_mT(), coupling=self.m.get_coupling_strength(),
                            predicted_xs=xs_theo, observed_xs=obs_xs, expected_xs=exp_xs,
                            width_ratio=self.m.get_width_mass_ratio(), result=self.result,
                            channel=i, obs_ratio=self.obs_ratio, exp_ratio=self.exp_ratio,
                            process=self.process[i], experiment=self.expt[i], luminosity=self.luminosity[i],
                            energy=self.energy[i], label=self.label[i], model=self.m.model())

    def check_SM_plus_TX_doublet_limit(self, m, k):
        self.m.set_mT(m)
        self.m.set_coupling_strength(k)
        self.check_channel()
        self.print_result()
        if self.m.get_sin_up_right() is None:
            print("Warning: (T, B) couplings are not set. Doublet (T, B) "
                  "single production cross sections will not be checked.")
        i = self.channel
        xs_theo = self.numerator(i)
        obs_xs = (1 / self.obs_ratio) * self.numerator(i)
        exp_xs = (1 / self.exp_ratio) * self.numerator(i)
        self.df = df_making(self.df, mass=self.m.get_mT(), coupling=self.m.get_coupling_strength(),
                            predicted_xs=xs_theo, observed_xs=obs_xs, expected_xs=exp_xs,
                            width_ratio=self.m.get_width_mass_ratio(), result=self.result,
                            channel=i, obs_ratio=self.obs_ratio, exp_ratio=self.exp_ratio,
                            process=self.process[i], experiment=self.expt[i], luminosity=self.luminosity[i],
                            energy=self.energy[i], label=self.label[i], model=self.m.model(),
                            which_doublet=self.m.which_d)

    def check_SM_plus_TB_doublet_limit(self, m, k):
        self.m.set_mT(m)
        self.m.set_coupling_strength(k)
        self.check_channel()
        self.print_result()
        i = self.channel
        xs_theo = self.numerator(i)
        obs_xs = (1 / self.obs_ratio) * self.numerator(i)
        exp_xs = (1 / self.exp_ratio) * self.numerator(i)
        self.df = df_making(self.df, mass=self.m.get_mT(), coupling=self.m.get_coupling_strength(),
                            predicted_xs=xs_theo, observed_xs=obs_xs, expected_xs=exp_xs,
                            width_ratio=self.m.get_width_mass_ratio(), result=self.result,
                            channel=i, obs_ratio=self.obs_ratio, exp_ratio=self.exp_ratio,
                            process=self.process[i], experiment=self.expt[i], luminosity=self.luminosity[i],
                            energy=self.energy[i], label=self.label[i], model=self.m.model(),
                            which_doublet=self.m.which_d)

    def check_pure_limit(self):
        self.check_channel()
        self.print_result()
        i = self.channel
        xs_theo = self.numerator(i)
        obs_xs = (1 / self.pred_obs_rat) * self.numerator(i)
        exp_xs = (1 / self.pred_exp_rat) * self.numerator(i)
        self.df = df_making(self.df, mass=self.m.get_mT(), predicted_xs=xs_theo, observed_xs=obs_xs, expected_xs=exp_xs,
                            result=self.allowed_or_excluded, channel=i,
                            obs_ratio=self.obs_ratio, process=self.process[i], experiment=self.expt[i],
                            luminosity=self.luminosity[i], energy=self.energy[i],
                            label=self.label[i], model=self.m.model())

    def check_coupling_limit(self, **kwargs):
        self.coupling_limit()
        self.print_result()
        i = self.channel
        if self.m.model() == 'Singlet':
            self.df = df_making(self.df, mass=self.m.get_mT(), coupling=self.m.get_sin_left(),
                            width=self.m.get_width_mass_ratio(), result=self.result,
                            channel=i, obs_ratio=self.obs_ratio, process=self.process[i],
                            experiment=self.expt[i], luminosity=self.luminosity[i], energy=self.energy[i],
                            label=self.label[i], model=self.m.model())
        else:
            self.df = df_making(self.df, mass=self.m.get_mT(), coupling=self.m.get_coupling_strength(),
                                width=self.m.get_width_mass_ratio(), result=self.result,
                                channel=i, obs_ratio=self.obs_ratio, exp_ratio=self.exp_ratio, process=self.process[i],
                                experiment=self.expt[i], luminosity=self.luminosity[i], energy=self.energy[i],
                                label=self.label[i], model=self.m.model())

    def print_result(self):
        print('', end='\t\t')
        print('PyTop v-0.1')
        print("-----------------------------------------------")
        print(f"Vector-like T mass: {self.m.get_mT()}")
        print(f"width-to-mass ratio: {self.m.get_width_mass_ratio()}")
        print(f"coupling strength: {self.m.get_coupling_strength()}")
        if self.m.model() == 'Singlet':
            print("sin_left:", self.m.get_sin_left())
        elif self.m.model() == 'Doublet' and self.m.get_which_doublet() == 'TX':
            print(f"sin_right:", self.m.get_sin_right())
        elif self.m.model() == 'Doublet' and self.m.get_which_doublet() == 'TB':
            print(f"sin_up_right:", self.m.get_sin_up_right())
        if self.channel != -1:
            print(f"Experiment: {self.expt[self.channel]}")
        print(self)
        print("-----------------------------------------------")
