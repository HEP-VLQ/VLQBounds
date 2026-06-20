import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from numpy.typing import NDArray
import numpy as np
from .models import *
from .manip import TheoryCalc
from scipy.interpolate import interp1d
from .utils import coupling_data_loading, obs_exp_ratio_calc, biggest_ratio, from_cf_to_kappa


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class CouplingTableEntry:
    """One experimental coupling-limit table row."""
    key: str
    label: str
    expt: str
    file_name: str
    process: str
    which_coupling: str
    energy: int
    luminosity: float


# ---------------------------------------------------------------------------
# Table catalogues (pure data - no logic)
# ---------------------------------------------------------------------------

_B_SINGLET_COUPLING: List[CouplingTableEntry] = [
    CouplingTableEntry('02595f9a',  'arXiv:2308.02595', 'ATLAS', '2308.02595_ATLAS_Fig9a_pp_B_bH_k_singlet.dat', 'pp --> Bbq --> bH --> 0l', 'k_B', 13, 139.0),
    CouplingTableEntry('01486f43',  'arXiv:1802.01486', 'CMS',   '2405.17605_Fig43_upper_pp_B_bH_singlet_1802.01486_cf.dat',  'pp --> Bqq --> bH --> b,bb,bq',                  'k_B', 13,  35.9),
    CouplingTableEntry('01486f43b', 'arXiv:1809.08597', 'CMS',   '2405.17605_Fig43_upper_pp_Bbq_tW_singlet_1809.08597_cf.dat',  'pp --> Bbq --> tW --> bqq,lnu/blnu,qq',       'k_B', 13,  35.9),
    CouplingTableEntry('10216f43',  'arXiv:2111.10216', 'CMS',   '2405.17605_Fig43_upper_pp_Bbq_tW_singlet_2111.10216_cf.dat', 'pp --> Bbq --> tW --> bqq,lnu/qq',               'k_B', 13, 138.0),
    CouplingTableEntry('01486f43t', 'arXiv:1809.08597', 'CMS',   '2405.17605_Fig43_upper_pp_Btq_tW_singlet_1809.08597_cf.dat',  'pp --> Btq --> tW --> bqq,lnu/blnu,qq',          'k_B', 13,  35.9),
    CouplingTableEntry('10216f43t', 'arXiv:2111.10216', 'CMS',   '2405.17605_Fig43_upper_pp_Btq_tW_singlet_2111.10216_cf.dat', 'pp --> Btq --> tW --> bqq,lnu/qq',               'k_B', 13, 138.0),
    CouplingTableEntry('01423f10a', 'arXiv:2606.01423', 'CMS',   '2606.01423_CMS_Fig10a_pp_Bbq_wtbq_singlet.txt',    'pp --> Bbq --> tW --> l',   'k_B', 13,  138),
    CouplingTableEntry('01423f10b', 'arXiv:2606.01423', 'CMS',   '2606.01423_CMS_Fig10b_pp_Btq_wttq_singlet.txt',     'pp --> Btq --> tW --> l',   'k_B', 13, 138.0),
]

_B_DOUBLET_COUPLING: List[CouplingTableEntry] = [
    CouplingTableEntry('02595f9b',  'arXiv:2308.02595', 'ATLAS', '2308.02595_ATLAS_Fig9b_pp_B_bH_k_doublet.dat',                              'pp --> Bbq --> bH --> 0l',                       'k_B', 13, 139.0),
    CouplingTableEntry('01486f43l', 'arXiv:1802.01486', 'CMS',   '2405.17605_Fig43_lower_pp_B_bH_doublet_1802.01486_cf.dat',                  'pp --> Bbq --> bH --> 0l',                       'k_B', 13,  35.9),
]

_X_DOUBLET_COUPLING: List[CouplingTableEntry] = [
    CouplingTableEntry('08597Fig44l', 'arXiv:1809.08597', 'CMS',   '2405.17605_CMS_Fig44_left_pp_tqX_tW_1809.08597.dat',                      'pp --> Xtq --> tW --> bqq,lnu/blnu,qq ',         'k_x', 13,  35.9),
    CouplingTableEntry('10216Fig44l', 'arXiv:2111.10216', 'CMS',   '2405.17605_CMS_Fig44_left_pp_tqX_tW_2111.10216.dat',                      'pp --> Xtq --> tW --> bqq,lnu/blnu,qq ',         'k_x', 13, 138.0),
    CouplingTableEntry('11883f10b',   'arXiv:1807.11883', 'ATLAS', '1807.11883_ATLAS_Fig10b_pp_XX_Wt_coupling.dat',                            'pp --> XX(Xtq) --> tW --> l+l+ ',                'k_x', 13,  36.1),
]

_Y_DOUBLET_COUPLING: List[CouplingTableEntry] = [
    CouplingTableEntry('08328Fig44r', 'arXiv:1701.08328',    'CMS',   '2405.17605_CMS_Fig44_right_pp_tqY_bW_1701.08328.dat',                  'pp --> Ytq --> bW --> bqq,lnu/blnu,qq ',         'k_y',  13,   2.3),
    CouplingTableEntry('05606f8b',    'arXiv:1602.05606',    'ATLAS', '1602.05606_ATLAS_Fig8b_pp_Ybj_Wb_Doublet_sinR.dat',                    'pp --> Ybq --> bW --> b,lnu ',                   'k_y',   8,  20.3),
    CouplingTableEntry('072f10b',     'ATLAS_CONF_2016_072', 'ATLAS', 'ATLAS_CONF_2016_072_fig10b_doublet.dat',                               'pp --> Ybq --> bW --> b,lnu ',                   'k_y',  13,   3.2),
    CouplingTableEntry('07343f8c',    'arXiv:1812.07343',    'ATLAS', '1812.07343_ATLAS_pp_Ybq_Wbbq_Fig8c_doublet_Y_RH_sinR.dat',             'pp --> Ybq --> bW --> b,lnu ',                   'k_y',  13,  36.1),
    CouplingTableEntry('20273',       'arXiv:2409.20273',    'ATLAS', '2409.20273_ATLAS_Fig6_pp_Ybq_Wb_doublet_BY.dat',                       'pp --> Ybq --> bW --> b, qq',                    'k_y',  13,  36.1),
]

_Y_TRIPLET_COUPLING: List[CouplingTableEntry] = [
    CouplingTableEntry('07343f8b', 'ArXiv:1812.07343', 'ATLAS', '1812.07343_ATLAS_Fig8b_pp_Ybq_Wb_triplet_Y_LH_sinL.dat',                      'pp --> Ybq --> bW --> b,lnu',                    's_d_l', 13, 36.1),
]

_T_SINGLET_COUPLING: List[CouplingTableEntry] = [
    CouplingTableEntry('05606f7b',      'arXiv:1602.05606',    'ATLAS', '1602.05606_ATLAS_f7b_pp_Tbj_Wbbj_s_L_Singlet.dat',                   'pp --> Tbq --> Wb --> lnu,b ',                   's_l',  8,  20.3),
    CouplingTableEntry('07343f8as_L',   'arXiv:1812.07343',    'ATLAS', '1812.07343_ATLAS_f8a_pp_Tbq_wbbq_Singlet_s_L.dat',                   'pp --> Tbq --> Wb --> 1l ',                      's_l', 13,  36.1),
    CouplingTableEntry('09743f6b_s_L',  'arXiv:1812.09743',    'ATLAS', '1812.09743_ATLAS_f6b_pp_Tbq_tZbq_s_L_Singlet.dat',                   'pp --> Tbq --> tZ --> 0l+1l ',                   's_l', 13,  36.1),
    CouplingTableEntry('10555f16b_s_L', 'arXiv:1806.10555',    'ATLAS', '1806.10555_ATLAS_f16b_pp_Tbq_Zt_s_L_Singlet.dat',                    'pp --> Tbq --> tZ --> l+l-+>=3l',                's_l', 13,  36.1),
    CouplingTableEntry('072f10b',       'ATLAS-CONF-2016-072', 'ATLAS', 'ATLAS-CONF-2016-072_ATLAS_f10a_pp_Tqb_Wb_singlet_s_L.dat',           'pp --> Tbq --> bW --> 1l',                       's_l', 13,  36.1),
    CouplingTableEntry('12802f5',       'arXiv:2302.12802',    'CMS',   '2302.12802_CMS_Fig5_pp_Tbq_tH_cf.dat',                                'pp --> Tbq --> tH --> gamma gamma, 0l/1l',       'k_T', 13,  36.1),
    CouplingTableEntry('16561f12a_k_T', 'arXiv:2402.16561',    'ATLAS', '2402.16561_ATLAS_Fig12a_pp_T_Ht_Zt_k_T_singlet.dat',                  'pp --> Tbq --> tZ --> 0l',                       'k_T', 13, 139.0),
    CouplingTableEntry('07045f9_k_T',   'arXiv:2201.07045',    'ATLAS', '2201.07045_ATLAS_f9_pp_Tbq_Htbq_k_T_singlet.dat',                    'pp --> Tbq --> tH --> 0l',                       'k_T', 13, 139.0),
    CouplingTableEntry('03401f13a',     'arXiv:2305.03401',    'ATLAS', '2305.03401_ATLAS_f13a_pp_Tbq_Ztbq_singlet_k_T.dat',                  'pp --> Tbq --> tZ(H) --> 1l',                    'k_T', 13, 139.0),
    CouplingTableEntry('07584f9a',      'arXiv:2307.07584',    'ATLAS', '2307.07584_ATLAS_f9a_pp_Tbq_Ztbq_k_T_singlet.dat',                   'pp --> Tbq --> tZ --> l+l-+3l ',                 'k_T', 13, 139.0),
    CouplingTableEntry('01062f42u',     'arXiv:1708.01062',    'CMS',   '2405.17605_CMS_Fig42_upper_pp_Tbq_tZ_ll_singlet_1708.01062_cf.dat',  'pp --> Tbq --> tZbq --> l+l-',                   'k_T', 13,  35.9),
    CouplingTableEntry('08328f42u',     'arXiv:1701.08328',    'CMS',   '2405.17605_CMS_Fig42_upper_pp_T_bW_singlet_1701.08328_cf.dat',       'pp --> Tbq --> tZbq --> 1l',                     'k_T', 13,   2.3),
    CouplingTableEntry('17605f42u',     'arXiv:2405.17605',    'CMS',   '2405.17605_CMS_Fig42_upper_pp_T_combination_singlet_cf.dat',         'pp --> Tbq --> tZbq --> 0l',                     'k_T', 13, 138.0),
    CouplingTableEntry('04721f42up1',   'arXiv:1909.04721',    'CMS',   '2405.17605_CMS_Fig42_upper_pp_Ttq_tZ_tH_singlet_part1_1909.04721_cf.dat', 'pp --> Tbq --> tZbq --> 0l',                  'k_T', 13,  35.9),
    CouplingTableEntry('04721f42up2',   'arXiv:1909.04721',    'CMS',   '2405.17605_CMS_Fig42_upper_pp_Ttq_tZ_tH_part2_singlet_1909.04721_cf.dat', 'pp --> Tbq --> tZbq --> 0l',                  'k_T', 13,  35.9),
    CouplingTableEntry('01062f42utq',   'arXiv:1708.01062',    'CMS',   '2405.17605_CMS_Fig42_upper_pp_Ttq_tZ_singlet_1708.01062_cf.dat',     'pp --> Tbq --> tZbq --> l+l-',                   'k_T', 13,  35.9),
    CouplingTableEntry('02227f42u',     'arXiv:2201.02227',    'CMS',   '2405.17605_CMS_Fig42_upper_pp_T_tZ_singlet_2201.02227_cf.dat',       'pp --> Tbq --> tZbq --> 0l',                     'k_T', 13, 137.0),
    CouplingTableEntry('05071f42u',     'arXiv:2405.05071',    'CMS',   '2405.17605_CMS_Fig42_upper_pp_T_tZ_tH_singlet_2405.05071_cf.dat',    'pp --> Tbq --> tZbq --> 0l',                     'k_T', 13, 138.0),
    CouplingTableEntry('04721f42ubq1',  'arXiv:1909.04721',    'CMS',   '2405.17605_CMS_Fig42_upper_pp_Tbq_tZ_tH_singlet_part1_1909.04721_cf.dat', 'pp --> Tbq --> (tZ + tH)bq --> bqq, bb',      'k_T', 13,  35.9),
    CouplingTableEntry('04721f42ubq2',  'arXiv:1909.04721',    'CMS',   '2405.17605_CMS_Fig42_upper_pp_Tbq_tZ_tH_singlet_part2_1909.04721_cf.dat', 'pp --> Tbq --> (tZ + tH)bq --> bqq, bb',      'k_T', 13,  35.9),
    CouplingTableEntry('08789f6a',      'arXiv:2408.08789',    'ATLAS', '2408.08789_ATLAS_Fig6a_pp_Tbq_Ht_Zt_singlet.dat',                    'pp --> Tb(t)q --> tZ/H --> 0l+1l+>=2l',          'k_T', 13, 139.0),
    CouplingTableEntry('15515f6a',   'arXiv:2506.15515',      'ATLAS', '2506.15515_ATLAS_Fig6a_pp_Tbq_Wb_singlet.txt',  'pp -->  Tbq --> Wbbq --> 1l', 'k_T', 13, 140.0),
    
    CouplingTableEntry('17564f4b',   'arXiv:2604.17564',      'CMS',   '2604.17564_CMS_Fig4b_pp_VLQ_Wb_Tsinglet.txt',  'pp --> T --> Wb --> 1l', 'k_T', 13, 138.0),
]

_T_DOUBLET_COUPLING: List[CouplingTableEntry] = [
    CouplingTableEntry('03401f13b', 'arXiv:2305.03401', 'ATLAS', '2305.03401_ATLAS_f13b_pp_Tbq_Ztbq_k_T_doublet.dat',                          'pp --> Tbq --> tZbq --> 1l',                     'k_T', 13, 139.0),
    CouplingTableEntry('07584f9b',  'arXiv:2307.07584', 'ATLAS', '2307.07584_ATLAS_f9b_pp_Tbq_Ztbq_k_T_doublet.dat',                           'pp --> Tbq --> tZbq --> l+l-+3l',                'k_T', 13, 139.0),
    CouplingTableEntry('01062f42l', 'arXiv:1708.01062', 'CMS',   '2405.17605_CMS_Fig42_lower_pp_T_tZ_doublet_1708.01062_cf.dat',               'pp --> Tbq --> tZbq --> l+l-',                   'k_T', 13,  35.9),
    CouplingTableEntry('04721f42lp1', 'arXiv:1909.04721', 'CMS', '2405.17605_CMS_Fig42_lower_pp_T_tZ_tH_doublet_part1_1909.04721_cf.dat',      'pp --> Tbq --> tZbq --> 0l',                     'k_T', 13,  35.9),
    CouplingTableEntry('04721f42lp2', 'arXiv:1909.04721', 'CMS', '2405.17605_Fig42_lower_pp_T_tZ_tH_doublet_part2_cf_1909.04721.dat',          'pp --> Tbq --> tZbq --> 0l',                     'k_T', 13,  35.9),
    CouplingTableEntry('08789f6b',  'arXiv:2408.08789', 'ATLAS', '2408.08789_ATLAS_Fig6b_pp_Tbq_Ht_Zt_doublet.dat',                            'pp --> Tb(t)q --> tZ/H --> 1l + 2l + >=3l',      'k_T', 13, 139.0),
]

# Model type -> catalogue of coupling-limit tables.
# Note: Pure* models have no coupling-limit tables (mirrors the original
# `get_number_of_tables` warning/zero-table behaviour).
_COUPLING_CATALOGUE: Dict[type, List[CouplingTableEntry]] = {
    SingletB: _B_SINGLET_COUPLING,
    DoubletB: _B_DOUBLET_COUPLING,
    DoubletX: _X_DOUBLET_COUPLING,
    DoubletY: _Y_DOUBLET_COUPLING,
    TripletY: _Y_TRIPLET_COUPLING,
    SingletT: _T_SINGLET_COUPLING,
    DoubletT: _T_DOUBLET_COUPLING,
}

# VLQ tag used for mass-array attribute names (coupling_M{tag}_obs/_exp)
# and passed through to coupling_data_loading(..., vlq=tag).
_COUPLING_VLQ_TAG: Dict[type, str] = {
    SingletB: 'B', DoubletB: 'B',
    DoubletX: 'X',
    DoubletY: 'Y', TripletY: 'Y',
    SingletT: 'T', DoubletT: 'T',
}


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

    # ------------------------------------------------------------------
    # Catalogue-driven setup (replaces the old per-branch hand-written
    # initialize_coupling_data / fill_coupling_tables)
    # ------------------------------------------------------------------

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

    def initialize_coupling_data(self):
        entries = _COUPLING_CATALOGUE.get(type(self.m))
        if not entries:
            print(f"Warning. There is no coupling limits for this model {self.m.model()}")
            return
        self.initialize_coupling_lists(len(entries))

    def _load_coupling_data(self, vlq_tag):
        """Read the data files for the currently-loaded catalogue and fill
        the observed/expected/mass arrays (mirrors the repeated
        `expected = [...]; observed = [...]; mass = [...]; coupling_data_loading(...)`
        block that used to appear after every branch)."""
        mass_obs = getattr(self, f'coupling_M{vlq_tag}_obs')
        mass_exp = getattr(self, f'coupling_M{vlq_tag}_exp')
        expected = [self.coupling_exp_upper, self.coupling_exp_lower]
        observed = [self.coupling_obs_lower, self.coupling_obs_upper]
        mass = [mass_obs, mass_exp]
        coupling_data_loading(self.coupling_file_name, len(self.coupling_key), mass, expected, observed,
                              self.coupling_expt, vlq=vlq_tag)

    def fill_coupling_tables(self):
        entries = _COUPLING_CATALOGUE.get(type(self.m))
        if not entries:
            return

        self.coupling_key = [e.key for e in entries]
        self.coupling_label = [e.label for e in entries]
        self.coupling_expt = [e.expt for e in entries]
        self.coupling_file_name = [e.file_name for e in entries]
        self.coupling_process = [e.process for e in entries]
        self.which_coupling = [e.which_coupling for e in entries]
        self.coupling_energy = [e.energy for e in entries]
        self.coupling_luminosity = [e.luminosity for e in entries]

        vlq_tag = _COUPLING_VLQ_TAG[type(self.m)]
        self._load_coupling_data(vlq_tag)

        # Only B and T models convert cf-style files into kappa couplings
        # (matches the original: VLX/VLY branches never called this).
        if self.VLB:
            self.coupling_factor_to_coupling_strength('B')
        elif not self.VLX and not self.VLY:
            self.coupling_factor_to_coupling_strength()

    # ------------------------------------------------------------------
    # Everything below is unchanged business logic
    # ------------------------------------------------------------------

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
