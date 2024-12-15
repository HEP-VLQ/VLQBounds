import datetime
from .models import *
from .utils import *
from .coupling import Coupling


models = (SingletT, DoubletT, PureT, SingletB, DoubletB, PureB, DoubletX, DoubletY, TripletY)


class VLQBounds(Coupling):
    def __init__(self, m):
        self.first_run = True
        if isinstance(m, models):
            super().__init__(m)
            self.m = m
            self.df = c.df
            self.welcome_message()
            self.set_VLQ_type()

    def initialize_xs_data(self):
        self.initialize_tables_cms_and_atlas()
        self.all_processes()
        self.cs_dict()
        self.tb_xt_dict()

    def initialize_coupling_bounds(self):
        self.fill_coupling_tables()
        self.all_couplings()
        self.fill_sin_and_kappa()

    def initialize_vlq_bounds(self):
        self.initialize_tables_cms_and_atlas()
        self.cs_dict()
        self.tb_xt_dict()
        if not isinstance(self.m, (PureT, PureB)):
            self.fill_coupling_tables()
            self.fill_sin_and_kappa()
            self.coupling_and_xs_info()

    def singletT_params(self, **kwargs):
        validate_params(kwargs, "mT", {"k_T", "w_m", "s_l"})
        self.set_mass_and_coupling(kwargs, "mT", "k_T", "w_m", "s_l")

    def singletB_params(self, **kwargs):
        validate_params(kwargs, "mB", {"k_B", "w_m", "s_l"})
        self.set_mass_and_coupling(kwargs, "mB", "k_B", "w_m", "s_l")


    def doubletT_TB_params(self, **kwargs):
        validate_params(kwargs, "mT", {"k_T", "w_m", "s_u_r"})
        self.m.change_to_TB()
        self.set_mass_and_coupling(kwargs, "mT", "k_T", "w_m", "s_u_r")

    def doubletB_TB_params(self, **kwargs):
        validate_params(kwargs, "mB", {"k_B", "w_m", "s_d_r"})
        self.m.change_to_TB()
        self.set_mass_and_coupling(kwargs, "mB", "k_B", "w_m", "s_d_r")

    def doubletT_XT_params(self, **kwargs):
        validate_params(kwargs, "mT", {"k_T", "w_m", "s_r"})
        self.set_mass_and_coupling(kwargs, "mT", "k_T", "w_m", "s_r")

    def doubletX_XT_params(self, **kwargs):
        validate_params(kwargs, "mX", {"k_X", "w_m", "s_r"})
        self.set_mass_and_coupling(kwargs, "mX", "k_X", "w_m", "s_r")

    def doubletB_BY_params(self, **kwargs):
        validate_params(kwargs, "mB", {"k_B", "w_m", "s_r"})
        self.set_mass_and_coupling(kwargs, "mB", "k_B", "w_m", "s_r")

    def doubletY_BY_params(self, **kwargs):
        validate_params(kwargs, "mY", {"k_Y", "w_m", "s_r"})
        self.set_mass_and_coupling(kwargs, "mY", "k_Y", "w_m", "s_r")

    def tripletY_TBY_params(self, **kwargs):
        validate_params(kwargs, "mY", {"k_Y", "w_m", "s_d_l"})
        self.set_mass_and_coupling(kwargs, "mY", "k_Y", "w_m", "s_d_l")

    def pure_T_to_Wb(self, mT:float)-> None:
        self.to_H, self.to_W, self.to_Z = False, True, False
        self.m.set_mT(mT)

    def pure_T_to_Zt(self, mT:float)-> None:
        self.to_H, self.to_W, self.to_Z = False, False, True
        self.m.set_mT(mT)

    def pure_T_to_Ht(self, mT:float) -> None:
        self.to_H, self.to_W, self.to_Z = True, False, False
        self.m.set_mT(mT)

    def pure_B_to_Wt(self, mB:float) -> None:
        self.to_H, self.to_W, self.to_Z = False, True, False
        self.m.set_mB(mB)

    def pure_B_to_Zb(self, mB:float) -> None:
        self.to_H, self.to_W, self.to_Z = False, False, True
        self.m.set_mB(mB)

    def pure_B_to_Hb(self, mB:float) -> None:
        self.to_H, self.to_W, self.to_Z = True, False, False
        self.m.set_mB(mB)

    def check_against_xs_limits(self):
        self.check_channel()
        self.print_result()
        i = self._channel
        self.data_frame(i)

    def check_against_coupling_limits(self):
        _, _, _, _ = self.coupling_limit()
        self.print_result()
        i = self._channel
        self.data_frame(i)

    def check_against_xs_and_coupling_limits(self):
        self.check_xs_and_coupling_limits()
        i = self._channel
        self.data_frame(i)

    def get_key(self):
        self.get_sensitive_limits_info()

    def set_VLQ_type(self):
        if not isinstance(self.m, models):
            raise ValueError("Error, this model is not included")
        if isinstance(self.m, (SingletB, DoubletB, PureB)):
            self.VLB = True
        elif isinstance(self.m, DoubletX):
            self.VLX = True
        elif isinstance(self.m, (DoubletY, TripletY)):
            self.VLY = True

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
                if self.m.get_which_doublet() == 'BY':
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

    def set_df_attributes(self, mass, mixing, process, expt, luminosity, energy, label, which_doublet, channel):
        self.df = df_making(
            self.df,
            mass=mass,
            mixing=mixing if not self.m.model() == 'Pure' else None,
            coupling=self.m.get_coupling_strength() if not self.m.model() == 'Pure' else None,
            width_ratio=self.m.get_width_mass_ratio() if not self.m.model() == 'Pure' else None,
            result=self._result,
            channel=channel,
            obs_ratio=self._obs_ratio,
            exp_ratio=self._exp_ratio,
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
        def get_mixing():
            if self.m.model() == 'Singlet':
                return self.m.get_sin_left()
            if self.VLB:
                if self.m.model() == 'Doublet':
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
                if self.m.model() == 'Doublet':
                    if self.m.get_which_doublet() == 'TX':
                        return self.m.get_sin_right()
                    else:
                        return self.m.get_sin_up_right()

        def get_vlq_mass():
            if self.VLB:
                return self.m.get_mB()
            elif self.VLX:
                return self.m.get_mX()
            elif self.VLY:
                return self.m.get_mY()
            else:
                return self.m.get_mT()

        m_vlq = get_vlq_mass()
        mixing = get_mixing()
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

    def print_result(self):
        print('', end='\t\t')
        print('VLQBounds v-0.1')
        print("-----------------------------------------------")
        if self.VLB:
            print(f"mB: {self.m.get_mB()}")
            if self.m.model() == 'Singlet':
                print(f"Relative width: {self.m.get_width_mass_ratio()}")
                print(f"k_B: {self.m.get_coupling_strength()}")
                print("s_L:", self.m.get_sin_left())
            elif self.m.model() == 'Doublet' and self.m.get_which_doublet() == 'YB':
                print(f"Relative width: {self.m.get_width_mass_ratio()}")
                print(f"k_B: {self.m.get_coupling_strength()}")
                print(f"s_R:", self.m.get_sin_right())
            elif self.m.model() == 'Doublet' and self.m.get_which_doublet() == 'TB':
                print(f"Relative width: {self.m.get_width_mass_ratio()}")
                print(f"k_B: {self.m.get_coupling_strength()}")
                print(f"s_d_r:", self.m.get_sin_down_right())
            if self._channel != -1:
                if not is_array_full_of_none(self.key) and not is_array_full_of_none(self.coupling_key):
                    if self._channel < len(self.key):
                        print(f"Experiment: {self.expt[self._channel]}")
                    else:
                        print(f"Experiment: {self.coupling_expt[self._channel - len(self.key)]}")
                elif not is_array_full_of_none(self.key):
                    print(f"Experiment: {self.expt[self._channel]}")
                elif not is_array_full_of_none(self.coupling_key):
                    print(f"Experiment: {self.coupling_expt[self._channel]}")
            print(self)
        elif self.VLX:
            print(f"mX: {self.m.get_mX()}")
            print(f"Relative width: {self.m.get_width_mass_ratio()}")
            print(f"k_X: {self.m.get_coupling_strength()}")
            print(f"s_R:", self.m.get_sin_right())
            if self._channel != -1:
                if not is_array_full_of_none(self.key) and not is_array_full_of_none(self.coupling_key):
                    if self._channel < len(self.key):
                        print(f"Experiment: {self.expt[self._channel]}")
                    else:
                        print(f"Experiment: {self.coupling_expt[self._channel - len(self.key)]}")
                elif not is_array_full_of_none(self.key):
                    print(f"Experiment: {self.expt[self._channel]}")
                elif not is_array_full_of_none(self.coupling_key):
                    print(f"Experiment: {self.coupling_expt[self._channel]}")
            print(self)
        elif self.VLY:
            print(f"mY: {self.m.get_mY()}")
            print(f"Relative width: {self.m.get_width_mass_ratio()}")
            print(f"k_Y: {self.m.get_coupling_strength()}")
            if self.m.model() == 'Doublet':
                print(f"s_R:", self.m.get_sin_right())
            else:
                print(f"s_d_l:", self.m.get_sin_down_left())
            if self._channel != -1:
                if not is_array_full_of_none(self.key) and not is_array_full_of_none(self.coupling_key):
                    if self._channel < len(self.key):
                        print(f"Experiment: {self.expt[self._channel]}")
                    else:
                        print(f"Experiment: {self.coupling_expt[self._channel - len(self.key)]}")
                elif not is_array_full_of_none(self.key):
                    print(f"Experiment: {self.expt[self._channel]}")
                elif not is_array_full_of_none(self.coupling_key):
                    print(f"Experiment: {self.coupling_expt[self._channel]}")
            print(self)
        else:
            print(f"mT: {self.m.get_mT()}")
            if self.m.model() == 'Singlet':
                print(f"Relative width: {self.m.get_width_mass_ratio()}")
                print(f"k_T: {self.m.get_coupling_strength()}")
                print("s_L:", self.m.get_sin_left())
            elif self.m.model() == 'Doublet' and self.m.get_which_doublet() == 'TX':
                print(f"Relative width: {self.m.get_width_mass_ratio()}")
                print(f"k_T: {self.m.get_coupling_strength()}")
                print(f"s_R:", self.m.get_sin_right())
            elif self.m.model() == 'Doublet' and self.m.get_which_doublet() == 'TB':
                print(f"Relative width: {self.m.get_width_mass_ratio()}")
                print(f"k_T: {self.m.get_coupling_strength()}")
                print(f"s_u_R:", self.m.get_sin_up_right())
            if self._channel != -1:
                if not is_array_full_of_none(self.key) and not is_array_full_of_none(self.coupling_key):
                    if self._channel < len(self.key):
                        print(f"Experiment: {self.expt[self._channel]}")
                    else:
                        print(f"Experiment: {self.coupling_expt[self._channel - len(self.key)]}")
                elif not is_array_full_of_none(self.key):
                    print(f"Experiment: {self.expt[self._channel]}")
                elif not is_array_full_of_none(self.coupling_key):
                    print(f"Experiment: {self.coupling_expt[self._channel]}")
            print(self)
        print("-----------------------------------------------")

    def check_mass_range(self, m, vlq='T'):
        key = ''
        M_vlq = -1
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

    def welcome_message(self):
        self.first_run = False
        current_time = datetime.datetime.now().strftime("%Y-%m-%d") #%H:%M:%S
        print("****************************************************")
        print("*                                                  *")
        print("*                   VLQBounds v-0.1                *")
        print("*               Rachid Benbrik, Mohamed Boukidi    *")
        print("*               Mohamed Ech-chaouy, Khawla Salime  *")
        print(f"*                 Compiled on {current_time}           *")
        print("*                                                  *")
        print("****************************************************")


def validate_params(kwargs, required_mass_key, valid_keys):
    if len(kwargs) != 2:
        raise ValueError("Error, exactly 2 keyword arguments are required.")

    if required_mass_key not in kwargs or kwargs[required_mass_key] is None:
        raise ValueError(f"Error, mass ({required_mass_key}) is not provided or is None")

    other_key = set(kwargs.keys()) - {required_mass_key}
    if not other_key or other_key.pop() not in valid_keys:
        raise ValueError(f"Error, input must contain one of {valid_keys} besides '{required_mass_key}'")
