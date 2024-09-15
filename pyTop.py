from vector_like_T import *
from vector_like_B import *
from vector_like_X import *
from vector_like_Y import *
from utils import *
from coupling import Coupling


models = (SingletT, DoubletT, PureTDecay, SingletB, DoubletB, PureBDecay, DoubletX, DoubletY, TripletY)


class VLQBounds(Coupling):
    def __init__(self, m):
        if isinstance(m, models):
            super().__init__(m)
            self.m = m
            self.df = c.df

    def set_VLQ_type(self, vlq):
        if vlq not in ['T', 'B', 'X', 'Y']:
            raise ValueError("Error, VLQ must be 'T' or 'B'")
        if vlq == 'B':
            self.VLB = True
        elif vlq == 'X':
            self.VLX = True
        elif vlq == 'Y':
            self.VLY = True

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
            elif isinstance(self.m, (DoubletT, DoubletX)):
                if self.m.get_which_doublet() == 'XT':
                    self.m.set_sin_r(kwargs[sin_key])
                elif self.m.get_which_doublet() == 'TB':
                    self.m.set_sin_u_r(kwargs[sin_key])
            elif isinstance(self.m, (DoubletB, DoubletY)):
                if self.m.get_which_doublet() == 'YB':
                    self.m.set_sin_r(kwargs[sin_key])
                elif self.m.get_which_doublet() == 'TB':
                    self.m.set_sin_d_r(kwargs[sin_key])
            elif isinstance(self.m, TripletY):
                self.m.set_sin_down_left(kwargs[sin_key])

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

        elif isinstance(self.m, DoubletX):
            self.m.set_mX(kwargs[mass_key])
            self.check_mass_range(kwargs[mass_key], 'X')

        elif isinstance(self.m, (DoubletY, TripletY)):
            self.m.set_mY(kwargs[mass_key])
            self.check_mass_range(kwargs[mass_key], 'Y')


    def singletT_params(self, **kwargs):
        self.validate_params(kwargs, "mT", {"k_T", "w_m", "s_l"})
        self.set_mass_and_coupling(kwargs, "mT", "k_T", "w_m", "s_l")

    def singletB_params(self, **kwargs):
        self.validate_params(kwargs, "mB", {"k_B", "w_m", "s_l"})
        self.set_mass_and_coupling(kwargs, "mB", "k_B", "w_m", "s_l")

    def doubletT_TB_params(self, **kwargs):
        self.validate_params(kwargs, "mT", {"k_T", "w_m", "s_u_r"})
        self.m.change_to_TB()
        self.set_mass_and_coupling(kwargs, "mT", "k_T", "w_m", "s_u_r")

    def doubletB_TB_params(self, **kwargs):
        self.validate_params(kwargs, "mB", {"k_B", "w_m", "s_d_r"})
        self.m.change_to_TB()
        self.set_mass_and_coupling(kwargs, "mB", "k_B", "w_m", "s_d_r")

    def doubletT_XT_params(self, **kwargs):
        self.validate_params(kwargs, "mT", {"k_T", "w_m", "s_r"})
        self.set_mass_and_coupling(kwargs, "mT", "k_T", "w_m", "s_r")

    def doubletX_XT_params(self, **kwargs):
        self.validate_params(kwargs, "mX", {"k_X", "w_m", "s_r"})
        self.set_mass_and_coupling(kwargs, "mX", "k_X", "w_m", "s_r")

    def doubletB_BY_params(self, **kwargs):
        self.validate_params(kwargs, "mB", {"k_B", "w_m", "s_r"})
        self.set_mass_and_coupling(kwargs, "mB", "k_B", "w_m", "s_r")

    def doubletY_BY_params(self, **kwargs):
        self.validate_params(kwargs, "mY", {"k_Y", "w_m", "s_r"})
        self.set_mass_and_coupling(kwargs, "mY", "k_Y", "w_m", "s_r")

    def tripletY_TBY_params(self, **kwargs):
        self.validate_params(kwargs, "mY", {"k_Y", "w_m", "s_d_l"})
        self.set_mass_and_coupling(kwargs, "mY", "k_Y", "w_m", "s_d_l")

    def check_singlet_limit(self):
        self.check_channel()
        self.print_result()
        i = self.channel
        self.data_frame(i)

    def check_SM_TX_doublet_limit(self):
        self.check_channel()
        self.print_result()
        i = self.channel
        self.data_frame(i)

    def check_SM_YB_doublet_limit(self):
        self.check_channel()
        self.print_result()
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

    def get_key(self):
        self.get_sensitive_limits_info()

    def set_df_attributes(self, mass, mixing, process, expt, luminosity, energy, label, which_doublet, channel):
        self.df = df_making(
            self.df,
            mass=mass,
            mixing=mixing,
            coupling=self.m.get_coupling_strength(),
            width_ratio=self.m.get_width_mass_ratio(),
            result=self.result,
            channel=channel,
            obs_ratio=self.obs_ratio,
            exp_ratio=self.exp_ratio,
            process=process[channel],
            experiment=expt[channel],
            luminosity=luminosity[channel],
            energy=energy[channel],
            label=label[channel],
            model=self.m.model(),
            which_doublet=which_doublet
        )
        return self.df

    def data_frame(self, chan):
        m_vlq = self.get_vlq_mass()
        mixing = self.get_mixing()
        which_doublet = self.m.get_which_doublet() if self.m.model() == 'Doublet' else None

        if not is_array_full_of_none(self.key) and is_array_full_of_none(self.coupling_key):
            self.df = self.set_df_attributes(m_vlq,
                                             mixing,
                                             self.process,
                                             self.expt,
                                             self.luminosity,
                                             self.energy,
                                             self.label,
                                             which_doublet,
                                             chan)
        elif is_array_full_of_none(self.key) and not is_array_full_of_none(self.coupling_key):
            self.df = self.set_df_attributes(m_vlq,
                                             mixing,
                                             self.coupling_process,
                                             self.coupling_expt,
                                             self.coupling_luminosity,
                                             self.coupling_energy,
                                             self.coupling_label,
                                             which_doublet,
                                             chan)
        elif not is_array_full_of_none(self.key) and not is_array_full_of_none(self.coupling_key):
            if len(self.key) <= chan:
                chan -= len(self.key)
                self.df = self.set_df_attributes(m_vlq,
                                                 mixing,
                                                 self.coupling_process,
                                                 self.coupling_expt,
                                                 self.coupling_luminosity,
                                                 self.coupling_energy,
                                                 self.coupling_label,
                                                 which_doublet,
                                                 chan)
            else:
                self.df = self.set_df_attributes(m_vlq,
                                                 mixing,
                                                 self.process,
                                                 self.expt,
                                                 self.luminosity,
                                                 self.energy,
                                                 self.label,
                                                 which_doublet,
                                                 chan)
                
    def get_mixing(self):
        if self.m.model() == 'Singlet':
            return self.m.get_sin_left()

        if self.VLB:
            if self.m.get_which_doublet() == 'YB':
                return self.m.get_sin_right()
            else:
                return self.m.get_sin_down_right()
        elif self.VLY:
            if self.m.model() == 'Doublet':
                return self.m.get_sin_right()
            else:
                return self.m.get_sin_down_left()
        elif self.VLX:
            if self.m.model() == 'Doublet':
                return self.m.get_sin_right()
        else:
            if self.m.get_which_doublet() == 'TX':
                return self.m.get_sin_right()
            else:
                return self.m.get_sin_up_right()

    def get_vlq_mass(self):
        if self.VLB:
            return self.m.get_mB()
        elif self.VLX:
            return self.m.get_mX()
        elif self.VLY:
            return self.m.get_mY()
        else:
            return self.m.get_mT()

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
        elif self.VLX:
            print(f"Vector-like X mass: {self.m.get_mX()}")
            print(f"Width-to-mass ratio: {self.m.get_width_mass_ratio()}")
            print(f"coupling strength: {self.m.get_coupling_strength()}")
            print(f"sin_right:", self.m.get_sin_right())
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
        elif self.VLY:
            print(f"Vector-like Y mass: {self.m.get_mY()}")
            print(f"Width-to-mass ratio: {self.m.get_width_mass_ratio()}")
            print(f"coupling strength: {self.m.get_coupling_strength()}")
            if self.m.model() == 'Doublet':
                print(f"sin_right:", self.m.get_sin_right())
            else:
                print(f"s_d_l:", self.m.get_sin_down_left())
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
        elif vlq == 'B':
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

        elif vlq == 'X':
            if not is_array_full_of_none(self.coupling_key):
                if is_array_full_of_none(self.key):
                    M_vlq = self.coupling_MX_obs
                    key = self.coupling_key
                else:
                    key = self.key + self.coupling_key
                    M_vlq = self.MX + self.coupling_MX_obs
            else:
                if is_array_full_of_none(self.key):
                    raise Exception("Error. Experimental data are not filled")
                else:
                    key = self.key
                    M_vlq = self.MX

        elif vlq == 'Y':
            if not is_array_full_of_none(self.coupling_key):
                if is_array_full_of_none(self.key):
                    M_vlq = self.coupling_MY_obs
                    key = self.coupling_key
                else:
                    key = self.key + self.coupling_key
                    M_vlq = self.MY + self.coupling_MY_obs
            else:
                if is_array_full_of_none(self.key):
                    raise Exception("Error. Experimental data are not filled")
                else:
                    key = self.key
                    M_vlq = self.MY


        mini = float("inf")
        maxi = float("-inf")
        for i, k in enumerate(key):
            if min(M_vlq[i]) < mini:
                mini = min(M_vlq[i])
            if max(M_vlq[i]) > maxi:
                maxi = max(M_vlq[i])
        if m < mini or m > maxi:
            print(f"the vlq mass {m} is beyond the experimental mass range [{mini}, {maxi}]")


