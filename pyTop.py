from vector_like_T import *
from vector_like_B import *
from utils import *
from coupling import Coupling


class PyTop(Coupling):
    def __init__(self, m):
        if isinstance(m, (SingletT, DoubletT, PureTDecay, SingletB, DoubletB, PureBDecay)):
            super().__init__(m)
            self.m = m
            self.df = c.df

    def set_VLQ_type(self, vlq):
        if vlq not in ['T', 'B']:
            raise ValueError("Error, VLQ must be 'T' or 'B'")
        if vlq == 'B':
            self.VLB = True

    def filling_channels_data(self):
        self.initialize_tables_cms_and_atlas()
        self.all_processes()
        self.cs_dict()
        self.tb_xt_dict()

    def filling_couplings_data(self):
        self.fill_coupling_tables()
        self.all_couplings()
        self.fill_sin_and_kappa()

    def filling_couplings_and_xs_limits(self):
        self.initialize_tables_cms_and_atlas()
        self.cs_dict()
        self.tb_xt_dict()
        self.fill_coupling_tables()
        self.fill_sin_and_kappa()
        self.coupling_and_xs_info()

    def validate_params(self, kwargs, required_mass_key, valid_keys):
        if len(kwargs) != 2:
            raise ValueError("Error, exactly 2 keyword arguments are required.")

        if required_mass_key not in kwargs or kwargs[required_mass_key] is None:
            raise ValueError(f"Error, mass ({required_mass_key}) is not provided or is None")

        other_key = set(kwargs.keys()) - {required_mass_key}
        if not other_key or other_key.pop() not in valid_keys:
            raise ValueError(f"Error, input must contain one of {valid_keys} besides '{required_mass_key}'")

    def set_mass_and_coupling(self, kwargs, mass_key, coupling_key, width_key, sin_key):
        if coupling_key in kwargs:
            if kwargs[coupling_key] is None:
                raise ValueError(f"Error, {coupling_key} must not be None")
            self.m.set_coupling_strength(abs(kwargs[coupling_key]))

        elif width_key in kwargs:
            if kwargs[width_key] is None or kwargs[width_key] <= 0:
                raise ValueError(f"Error, {width_key} must be greater than 0")
            self.m.set_width_mass_ratio(kwargs[width_key])

        elif sin_key in kwargs:
            if kwargs[sin_key] is None:
                raise ValueError(f"Error, {sin_key} must not be None")
            check_sin(kwargs[sin_key])
            if isinstance(self.m, (SingletT, SingletB)):
                self.m.set_sin_l(kwargs[sin_key])
            elif isinstance(self.m, DoubletT):
                if self.m.get_which_doublet() == 'XT':
                    self.m.set_sin_r(kwargs[sin_key])
                elif self.m.get_which_doublet() == 'TB':
                    self.m.set_sin_u_r(kwargs[sin_key])
            elif isinstance(self.m, DoubletB):
                if self.m.get_which_doublet() == 'YB':
                    self.m.set_sin_r(kwargs[sin_key])
                elif self.m.get_which_doublet() == 'TB':
                    self.m.set_sin_d_r(kwargs[sin_key])

        if isinstance(self.m, SingletT):
            self.m.set_mT(kwargs[mass_key])
            self.check_mass_range(kwargs[mass_key])

        elif isinstance(self.m, SingletB):
            self.m.set_mB(kwargs[mass_key])
            self.check_mass_range(kwargs[mass_key], 'B')

        if isinstance(self.m, DoubletT):
            self.m.set_mT(kwargs[mass_key])
            self.check_mass_range(kwargs[mass_key])

        elif isinstance(self.m, DoubletB):
            self.m.set_mB(kwargs[mass_key])
            self.check_mass_range(kwargs[mass_key], 'B')


    def T_singlet_params(self, **kwargs):
        self.validate_params(kwargs, "mT", {"k_T", "w_m", "s_l"})
        self.set_mass_and_coupling(kwargs, "mT", "k_T", "w_m", "s_l")

    def B_singlet_params(self, **kwargs):
        self.validate_params(kwargs, "mB", {"k_B", "w_m", "s_l"})
        self.set_mass_and_coupling(kwargs, "mB", "k_B", "w_m", "s_l")

    def T_in_doublet_TB_params(self, **kwargs):
        self.validate_params(kwargs, "mT", {"k_T", "w_m", "s_u_r"})
        self.m.change_to_TB()
        self.set_mass_and_coupling(kwargs, "mT", "k_T", "w_m", "s_u_r")

    def B_in_doublet_TB_params(self, **kwargs):
        self.validate_params(kwargs, "mT", {"k_T", "w_m", "s_d_r"})
        self.m.change_to_TB()
        self.set_mass_and_coupling(kwargs, "mT", "k_T", "w_m", "s_d_r")

    def doublet_XT_params(self, **kwargs):
        self.validate_params(kwargs, "mT", {"k_T", "w_m", "s_r"})
        self.set_mass_and_coupling(kwargs, "mT", "k_T", "w_m", "s_r")

    def doublet_BY_params(self, **kwargs):
        self.validate_params(kwargs, "mB", {"k_B", "w_m", "s_r"})
        self.set_mass_and_coupling(kwargs, "mB", "k_B", "w_m", "s_r")

    def check_singlet_limit(self):
        self.check_channel()
        self.print_result()
        i = self.channel
        self.data_frame(i)

    def check_SM_TX_doublet_limit(self):
        self.check_channel()
        self.print_result()
        if self.m.get_sin_up_right() is None:
            print("Warning: (T, B) couplings are not set. Doublet (T, B) "
                  "single production cross sections will not be checked.")
        i = self.channel
        self.data_frame(i)

    def check_SM_YB_doublet_limit(self):
        self.check_channel()
        self.print_result()
        if self.m.get_sin_down_right() is None:
            print("Warning: (T, B) couplings are not set. Doublet (T, B) "
                  "single production cross sections will not be checked.")
        i = self.channel
        self.data_frame(i)

    def check_SM_plus_TB_doublet_limit(self):
        self.check_channel()
        self.print_result()
        i = self.channel
        self.data_frame(i)

    def check_pure_limit(self):
        self.check_channel()
        self.print_result()
        i = self.channel
        self.data_frame(i)

    def check_coupling_limit(self):
        _, _, _, _ = self.coupling_limit()
        self.print_result()
        i = self.channel
        self.data_frame(i)

    def check_against_xs_and_coupling_limits(self):
        self.check_xs_and_coupling_limits()
        self.print_result()
        i = self.channel
        self.data_frame(i)

    def data_frame(self, i):
        if self.coupling_key is not None:
            if len(self.key) <= i:
                i -= len(self.key)

        mass = self.m.get_mB() if self.VLB else self.m.get_mT()
        mixing = self.get_mixing()
        which_doublet = self.m.get_which_doublet() if self.m.model() == 'Doublet' else None

        #xs_theo = self.numerator(i)
        #obs_xs = (1 / self.obs_ratio) * xs_theo
        #exp_xs = (1 / self.exp_ratio) * xs_theo
        self.df = df_making(
            self.df,
            mass=mass,
            mixing=mixing,
            coupling=self.m.get_coupling_strength(),
            width_ratio=self.m.get_width_mass_ratio(),
            result=self.result,
            channel=i,
            obs_ratio=self.obs_ratio,
            exp_ratio=self.exp_ratio,
            process=self.process[i],
            experiment=self.expt[i],
            luminosity=self.luminosity[i],
            energy=self.energy[i],
            label=self.label[i],
            model=self.m.model(),
            which_doublet=which_doublet
        )

    def get_mixing(self):
        if self.m.model() == 'Singlet':
            return self.m.get_sin_left()

        if self.VLB:
            if self.m.get_which_doublet() == 'YB':
                return self.m.get_sin_right()
            else:
                return self.m.get_sin_down_right()
        else:
            if self.m.get_which_doublet() == 'TX':
                return self.m.get_sin_right()
            else:
                return self.m.get_sin_up_right()

    def print_result(self):
        print('', end='\t\t')
        print('PyTop v-0.1')
        print("-----------------------------------------------")
        if self.VLB:
            print(f"Vector-like B mass: {self.m.get_mB()}")
            print(f"Width-to-mass ratio: {self.m.get_width_mass_ratio()}")
            print(f"coupling strength: {self.m.get_coupling_strength()}")
            if self.m.model() == 'Singlet':
                print("sin_left:", self.m.get_sin_left())
            elif self.m.model() == 'Doublet' and self.m.get_which_doublet() == 'YB':
                print(f"sin_right:", self.m.get_sin_right())
            elif self.m.model() == 'Doublet' and self.m.get_which_doublet() == 'TB':
                print(f"sin_down_right:", self.m.get_sin_down_right())
            if self.channel != -1:
                if not is_array_full_of_none(self.key) and not is_array_full_of_none(self.coupling_key):
                    if self.channel < len(self.key):
                        print(f"Experiment: {self.expt[self.channel]}")
                    else:
                        print(f"Experiment: {self.coupling_expt[self.channel - len(self.key)]}")
                elif not is_array_full_of_none(self.key):
                    print(f"Experiment: {self.expt[self.channel]}")
                elif not is_array_full_of_none(self.coupling_key):
                    print(f"Experiment: {self.coupling_expt[self.channel]}")
            print(self)
        else:
            print(f"Vector-like T mass: {self.m.get_mT()}")
            print(f"Width-to-mass ratio: {self.m.get_width_mass_ratio()}")
            print(f"coupling strength: {self.m.get_coupling_strength()}")
            if self.m.model() == 'Singlet':
                print("sin_left:", self.m.get_sin_left())
            elif self.m.model() == 'Doublet' and self.m.get_which_doublet() == 'TX':
                print(f"sin_right:", self.m.get_sin_right())
            elif self.m.model() == 'Doublet' and self.m.get_which_doublet() == 'TB':
                print(f"sin_up_right:", self.m.get_sin_up_right())
            if self.channel != -1:
                if not is_array_full_of_none(self.key) and not is_array_full_of_none(self.coupling_key):
                    if self.channel < len(self.key):
                        print(f"Experiment: {self.expt[self.channel]}")
                    else:
                        print(f"Experiment: {self.coupling_expt[self.channel - len(self.key)]}")
                elif not is_array_full_of_none(self.key):
                    print(f"Experiment: {self.expt[self.channel]}")
                elif not is_array_full_of_none(self.coupling_key):
                    print(f"Experiment: {self.coupling_expt[self.channel]}")
            print(self)

    def check_mass_range(self, m, vlq='T'):
        if vlq == 'T':
            if not is_array_full_of_none(self.coupling_key):
                if is_array_full_of_none(self.key):
                    M_vlq = self.coupling_MT_obs
                    key = self.coupling_key
                else:
                    key = self.key + self.coupling_key
                    M_vlq = self.MT + self.coupling_MT_obs
            else:
                if is_array_full_of_none(self.key):
                    raise Exception("Error. Experimental data are not filled")
                else:
                    key = self.key
                    M_vlq = self.MT
        else:
            if not is_array_full_of_none(self.coupling_key):
                if is_array_full_of_none(self.key):
                    M_vlq = self.coupling_MB_obs
                    key = self.coupling_key
                else:
                    key = self.key + self.coupling_key
                    M_vlq = self.MB + self.coupling_MB_obs
            else:
                if is_array_full_of_none(self.key):
                    raise Exception("Error. Experimental data are not filled")
                else:
                    key = self.key
                    M_vlq = self.MB

        mini = float("inf")
        maxi = float("-inf")
        for i, k in enumerate(key):
            #print(i, M_vlq[i])
            if min(M_vlq[i]) < mini:
                mini = min(M_vlq[i])
            if max(M_vlq[i]) > maxi:
                maxi = max(M_vlq[i])
        if m < mini or m > maxi:
            raise Exception(f"Error in mass range. It must between {mini} and {maxi}")


