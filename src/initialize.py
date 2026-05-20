from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np
from numpy.typing import NDArray

from .models import (
    DoubletB, DoubletT, DoubletX, DoubletY,
    PureB, PureT, SingletB, SingletT, TripletY,
)
from .utils import load_data_from_files


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class TableEntry:
    """One experimental limit table row."""
    key: str
    label: str
    expt: str
    file_name: str
    process: str
    energy: int
    luminosity: float
    which_doublet: Optional[str] = None


# ---------------------------------------------------------------------------
# Table catalogues  (pure data – no logic)
# ---------------------------------------------------------------------------

# Each catalogue is a list[TableEntry].  Entries are looked up by VLQ type
# and model via _CATALOGUE below.

_B_SINGLET: List[TableEntry] = [
    TableEntry('01762fb',   'arXiv:1806.01762', 'ATLAS', '1806.01762_ATLAS_fig4b_pp_BB_Wt_singlet.dat',                             'pp --> BB --> Wt --> 1l',             13,  36.1),
    TableEntry('10555f13b', 'arXiv:1806.10555', 'ATLAS', '1806.10555_ATLAS_fig13b_pp_BB_Zb_singlet.dat',                            'pp --> BB --> Zb --> l+l-+>=3l',      13,  36.1),
    TableEntry('15413f7b',  'arXiv:2210.15413', 'ATLAS', '2210.15413_ATLAS_fig7b_pp_BB_Zb_singlet.dat',                             'pp --> BB --> Zb --> l+l-+3l',        13, 139.0),
    TableEntry('05263f7d',  'arXiv:2212.05263', 'ATLAS', '2212.05263_ATLAS_fig7d_pp_BB_Wt_singlet.dat',                             'pp --> BB --> Wt --> 1l',             13, 139.0),
    TableEntry('01486Fig6a','arXiv:1802.01486', 'CMS',   '1802.01486_Fig6a_CMS_upper_left_pp_B_bH_Gamma_M1_singlet_or_doublet.dat', 'pp --> Bbq --> bHbq --> 0l',          13,  35.9),
    TableEntry('01486Fig6b','arXiv:1802.01486', 'CMS',   '1802.01486_Fig6b_CMS_upper_right_pp_B_bH_Gamma_M10_singlet_or_doublet.dat','pp --> Bbq --> bHbq --> 0l',         13,  35.9),
    TableEntry('01486Fig6c','arXiv:1802.01486', 'CMS',   '1802.01486_Fig6c_CMS_lower_left_pp_B_bH_Gamma_M20_singlet_or_doublet.dat','pp --> Bbq --> bHbq --> 0l',          13,  35.9),
    TableEntry('01486Fig6d','arXiv:1802.01486', 'CMS',   '1802.01486_Fig6d_CMS_lower_right_pp_B_bH_Gamma_M30_singlet_or_doublet.dat','pp --> Bbq --> bHbq --> 0l',         13,  35.9),
    TableEntry('04758f8ll', 'arXiv:1805.04758', 'CMS',   '1805.04758_CMS_Fig8_lower_left_singlet.dat',                              'pp --> BB --> 1l+l+l++3l',            13,  35.9),
    TableEntry('07327f9c',  'arXiv:2209.07327', 'CMS',   '2209.07327_CMS_f9c_pp_BB_singlet.dat',                                    'pp --> BB --> 1l+l+l++3l',            13, 138.0),
    TableEntry('5500f12a',  'arXiv:1409.5500',  'ATLAS', '1409.5500_ATLAS_Fig12a_pp_BB_singlet.dat',                                'pp --> BB --> l+l-+3l',                8,  20.3),
    TableEntry('05425f8',   'arXiv:1503.05425', 'ATLAS', '1503.05425_ATLAS_Fig8_pp_BB_Wt_Zb_HB_singlet.dat',                        'pp --> BB --> 1l',                     8,  20.3),
    TableEntry('04605f7a',  'arXiv:1504.04605', 'ATLAS', '1504.04605_ATLAS_Fig7a_pp_BB_singlet.dat',                                'pp --> BB --> l+l+',                   8,  20.3),
    TableEntry('04306f22b', 'arXiv:1505.04306', 'ATLAS', '1505.04306_ATLAS_Fig22b_pp_BB_Hb_singlet.dat',                            'pp --> BB --> 1l',                     8,  20.3),
    TableEntry('02343f3a',  'arXiv:1808.02343', 'ATLAS', '1808.02343_ATLAS_Fig3a_pp_BB_singlet.dat',                                'pp --> BB --> 1l+l+l++3l',            13,  36.1),
    TableEntry('02595f8a',  'arXiv:2308.02595', 'ATLAS', '2308.02595_ATLAS_Fig8a_pp_B_bH_k03_singlet.dat',                          'pp --> Bb(t)q --> bHb(t)q --> 0l',    13, 139.0),
    TableEntry('02595f8c',  'arXiv:2308.02595', 'ATLAS', '2308.02595_ATLAS_Fig8c_pp_B_bH_k04_singlet.dat',                          'pp --> Bb(t)q --> bHb(t)q --> 0l',    13, 139.0),
    TableEntry('02595f8e',  'arXiv:2308.02595', 'ATLAS', '2308.02595_ATLAS_Fig8e_pp_B_bH_k05_singlet.dat',                          'pp --> Bb(t)q --> bHb(t)q --> 0l',    13, 139.0),
    TableEntry('07409f5l',  'arXiv:1701.07409', 'CMS',   '1701.07409_CMS_Fig5_left_pp_Bt_bZ_cWt05_singlet.dat',                     'pp --> Btq --> bZtq --> 0l',          13,   2.3),
    TableEntry('07409f5r',  'arXiv:1701.07409', 'CMS',   '1701.07409_CMS_Fig5_right_pp_Bb_bZ_cbZ05_singlet.dat',                    'pp --> Bbq --> bZbq --> 0l',          13,   2.3),
    TableEntry('10216f4l',  'arXiv:2111.10216', 'CMS',   '2111.10216_CMS_Fig4_left_pp_B_Wt_singlet_doublet.dat',                    'pp --> Bbq --> tWbq --> 1l',          13, 138.0),
    TableEntry('10216f4r',  'arXiv:2111.10216', 'CMS',   '2111.10216_CMS_Fig4_right_pp_B_Wt_singlet_doublet.dat',                   'pp --> Btq --> tWtq --> 1l',          13, 138.0),
    TableEntry('17605f39ll','arXiv:2405.17605', 'CMS',   '2405.17605_CMS_Fig39_lower_left_pp_BB_singlet.dat',                       'pp --> BB --> 0l',                    13, 138.0),
]

_B_DOUBLET: List[TableEntry] = [
    TableEntry('10555f13d',  'arXiv:1806.10555', 'ATLAS', '1806.10555_ATLAS_fig13d_pp_BB_BY_doublet.dat',                             'pp --> BB --> l+l-+>=3l',        13,  36.1, 'BY'),
    TableEntry('01771f13c',  'arXiv:1808.01771', 'ATLAS', '1808.01771_ATLAS_fig13c_pp_BB_BY_doublet.dat',                             'pp --> BB --> 0l',               13,  36.1, 'BY'),
    TableEntry('05263f7f',   'arXiv:2212.05263', 'ATLAS', '2212.05263_ATLAS_fig7f_pp_QQ_mass_degenerate_BYorTB_doublet.dat',          'pp --> BB --> 1l',               13, 139.0, 'TB'),
    TableEntry('01486Fig6a', 'arXiv:1802.01486', 'CMS',   '1802.01486_Fig6a_CMS_upper_left_pp_B_bH_Gamma_M1_singlet_or_doublet.dat',  'pp --> Bbq --> bHbq --> 0l',     13,  35.9, 'BYorTB'),
    TableEntry('01486Fig6b', 'arXiv:1802.01486', 'CMS',   '1802.01486_Fig6b_CMS_upper_right_pp_B_bH_Gamma_M10_singlet_or_doublet.dat','pp --> Bbq --> bHbq --> 0l',     13,  35.9, 'BYorTB'),
    TableEntry('01486Fig6c', 'arXiv:1802.01486', 'CMS',   '1802.01486_Fig6c_CMS_lower_left_pp_B_bH_Gamma_M20_singlet_or_doublet.dat', 'pp --> Bbq --> bHbq --> 0l',     13,  35.9, 'BYorTB'),
    TableEntry('01486Fig6d', 'arXiv:1802.01486', 'CMS',   '1802.01486_Fig6d_CMS_lower_right_pp_B_bH_Gamma_M30_singlet_or_doublet.dat','pp --> Bbq --> bHbq --> 0l',     13,  35.9, 'BYorTB'),
    TableEntry('04758Fig8lr','arXiv:1805.04758', 'CMS',   '1805.04758_CMS_Fig8_lower_right_pp_BB_doublet.dat',                        'pp --> BB --> 1l+l+l++3l',       13,  35.9, 'BYorTB'),
    TableEntry('09768Fig7ur','arXiv:1812.09768', 'CMS',   '1812.09768_CMS_Fig7_upper_right_pp_BB_doublet.dat',                        'pp --> BB --> l+l-',             13,  35.9, 'BYorTB'),
    TableEntry('09835Fig11l','arXiv:2008.09835', 'CMS',   '2008.09835_CMS_Fig11_lower_pp_BB_doublet.dat',                             'pp --> BB --> 0l',               13, 137.0, 'BYorTB'),
    TableEntry('07327f9d',   'arXiv:2209.07327', 'CMS',   '2209.07327_CMS_f9d_pp_BB_doublet.dat',                                     'pp --> BB --> 1l+l+l++3l',       13, 137.0, 'BYorTB'),
    TableEntry('02343f3b',   'arXiv:1808.02343', 'ATLAS', '1808.02343_ATLAS_Fig3b_pp_BB_TB_doublet.dat',                              'pp --> BB --> 1l+l+l++3l',       13,  36.1, 'TB'),
    TableEntry('02343f3c',   'arXiv:1808.02343', 'ATLAS', '1808.02343_ATLAS_Fig3c_pp_BB_BY_doublet.dat',                              'pp --> BB --> 1l+l+l++3l',       13,  36.1, 'BY'),
    TableEntry('02595f8b',   'arXiv:2308.02595', 'ATLAS', '2308.02595_ATLAS_Fig8b_pp_B_bH_k03_BY_doublet.dat',                        'pp --> Bb(t)q --> bHb(t)q --> 0l',13,139.0, 'BY'),
    TableEntry('02595f8d',   'arXiv:2308.02595', 'ATLAS', '2308.02595_ATLAS_Fig8d_pp_B_bH_k04_BY_doublet.dat',                        'pp --> Bb(t)q --> bHb(t)q --> 0l',13,139.0, 'BY'),
    TableEntry('02595f8f',   'arXiv:2308.02595', 'ATLAS', '2308.02595_ATLAS_Fig8f_pp_B_bH_k05_BY_doublet.dat',                        'pp --> Bb(t)q --> bHb(t)q --> 0l',13,139.0, 'BY'),
    TableEntry('03408f13r',  'arXiv:1706.03408', 'CMS',   '1706.03408_CMS_Fig13_right_pp_BB_doublet.dat',                             'pp --> BB --> 1l',               13,   2.6, 'BYorTB'),
    TableEntry('13808f18ll', 'arXiv:2402.13808', 'CMS',   '2402.13808_CMS_Fig18_lower_left_pp_BB_TB_doublet.dat',                     'pp --> BB --> 0l+l+l-',          13, 138.0, 'TB'),
    TableEntry('10216f4ld',  'arXiv:2111.10216', 'CMS',   '2111.10216_CMS_Fig4_left_pp_B_Wt_singlet_doublet.dat',                     'pp --> Bbq --> tWbq --> 1l',     13, 138.0, 'BYorTB'),
    TableEntry('17605f39lr', 'arXiv:2405.17605', 'CMS',   '2405.17605_CMS_Fig39_lower_right_pp_BB_doublet.dat',                       'pp --> BB --> 0l',               13, 138.0, 'BYorTB'),
    TableEntry('15413f7d',   'arXiv:2210.15413', 'ATLAS', '2210.15413_ATLAS_fig7d_pp_BB_BY_doublet.dat',                              'pp --> BB --> l+l-+3l',          13, 139.0, 'BY'),
]

_B_PURE: List[TableEntry] = [
    TableEntry('01762f4a',    'arXiv:1806.01762',      'ATLAS', '1806.01762_ATLAS_fig4a_pp_BB_Wt.dat',                       'pp --> BB --> WtWt --> 1l',          13,  36.1),
    TableEntry('15413fig7f',  'arXiv:2210.15413',      'ATLAS', '2210.15413_ATLAS_fig7f_pp_BB_Zb.dat',                       'pp --> BB --> ZbZb --> >= l+l-',     13, 139.0),
    TableEntry('09768fig7ul', 'arXiv:1812.09768',      'CMS',   '1812.09768_CMS_Fig7_upper_left_pp_BB_bZ.dat',               'pp --> BB --> ZbZb --> l+l-',        13,  35.9),
    TableEntry('09835fig11ul','arXiv:2008.09835',      'CMS',   '2008.09835_CMS_fig11_upper_left_pp_B_bH.dat',               'pp --> BB --> HbHb --> 0l',          13, 137.0),
    TableEntry('09835fig11ur','arXiv:2008.09835',      'CMS',   '2008.09835_CMS_fig11_upper_right_pp_B_bZ.dat',              'pp --> BB --> ZbZb --> 0l',          13, 137.0),
    TableEntry('1265f5',      'arXiv:1204.1265',       'ATLAS', '1204.1265_ATLAS_Fig5_pp_BB_Zb.dat',                         'pp --> BB --> ZbZb --> l+l-',        13, 137.0),
    TableEntry('04605f6a',    'arXiv:1504.04605',      'ATLAS', '1504.04605_ATLAS_Fig6a_pp_BB_Wt.dat',                       'pp --> BB --> WtWt --> l+l+',         8,  20.3),
    TableEntry('04306f22a',   'arXiv:1505.04306',      'ATLAS', '1505.04306_ATLAS_Fig22a_pp_BB_Hb.dat',                      'pp --> BB --> HbHb --> 1l',           8,  20.3),
    TableEntry('13808f18ul',  'arXiv:2402.13808',      'CMS',   '2402.13808_CMS_Fig18_upper_left_pp_BB_bH.dat',              'pp --> BB --> HbHb --> 0l+l+l-',     13, 138.0),
    TableEntry('13808f18ur',  'arXiv:2402.13808',      'CMS',   '2402.13808_CMS_Fig18_upper_right_pp_BB_bZ.dat',             'pp --> BB --> ZbZb --> 0l+l+l-',     13, 138.0),
    TableEntry('07129f13l',   'arXiv:1507.07129',      'CMS',   '1507.07129_Fig13_left_pp_BB_Wt.dat',                        'pp --> BB --> WtWt --> 1l+2l+>=2l',   8,  19.7),
    TableEntry('07129f13m',   'arXiv:1507.07129',      'CMS',   '1507.07129_Fig13_middle_pp_BB_bZ.dat',                      'pp --> BB --> ZbZb --> 1l+2l+>=2l',   8,  19.7),
    TableEntry('07129f13r',   'arXiv:1507.07129',      'CMS',   '1507.07129_Fig13_right_pp_BB_bH.dat',                       'pp --> BB --> HbHb --> 1l+2l+>=2l',   8,  19.7),
    TableEntry('17605f38l',   'arXiv:2405.17605',      'CMS',   '2405.17605_CMS_Fig38_lower_pp_BB_tW.dat',                   'pp --> BB --> WtWt --> 0l+>=1l+2l',  13,  19.7),
    TableEntry('17605f38ul',  'arXiv:2405.17605',      'CMS',   '2405.17605_CMS_Fig38_upper_left_pp_BB_bZ.dat',              'pp --> BB --> ZbZb --> 0l+2l',       13, 138.0),
    TableEntry('17605f38ur',  'arXiv:2405.17605',      'CMS',   '2405.17605_CMS_Fig38_upper_right_pp_BB_bH.dat',             'pp --> BB --> HbHb --> 0l+2l',       13, 138.0),
    TableEntry('05263f7f',    'arXiv:2212.05263',      'ATLAS', '2212.05263_ATLAS_fig7b_pp_BB_BYorTB_doublet.dat',           'pp --> BB --> WtWt --> 1l',          13, 139.0),
]

_X_DOUBLET: List[TableEntry] = [
    TableEntry('03188f7a',  'arXiv:1810.03188', 'CMS',   '1810.03188_CMS_Fig7a_pp_XX_tW_left_handed.dat',              'pp --> XX --> Wt --> 1l+l+l+', 13, 35.9),
    TableEntry('03188f7b',  'arXiv:1810.03188', 'CMS',   '1810.03188_CMS_Fig7b_pp_XX_tW_right_handed.dat',             'pp --> XX --> Wt --> 1l+l+l+', 13, 35.9),
    TableEntry('03188f7c',  'arXiv:1810.03188', 'CMS',   '1810.03188_CMS_Fig7c_pp_XX_tW_left_handed.dat',              'pp --> XX --> Wt --> 1l+l+l+', 13, 35.9),
    TableEntry('03188f7d',  'arXiv:1810.03188', 'CMS',   '1810.03188_CMS_Fig7d_pp_XX_tW_right_handed.dat',             'pp --> XX --> Wt --> 1l+l+l+', 13, 35.9),
    TableEntry('03188f7d2', 'arXiv:1810.03188', 'CMS',   '1810.03188_CMS_Fig7d_pp_XX_tW_right_handed.dat',             'pp --> XX --> Wt --> 1l+l+l+', 13, 35.9),
    TableEntry('03188f8a',  'arXiv:1810.03188', 'CMS',   '1810.03188_CMS_Fig8a_pp_XX_tW_left_handed_combination.dat',  'pp --> XX --> Wt --> 1l+l+l+', 13, 35.9),
    TableEntry('03188f8b',  'arXiv:1810.03188', 'CMS',   '1810.03188_CMS_Fig8b_pp_XX_tW_right_handed_combination.dat', 'pp --> XX --> Wt --> 1l+l+l+', 13, 35.9),
    TableEntry('03347f4a',  'arXiv:1707.03347', 'ATLAS', '1707.03347_ATLAS_fig4a_pp_XX_Wb.dat',                        'pp --> XX --> Wb --> 1l',       13, 36.1),
    TableEntry('01762f4a',  'arXiv:1806.01762', 'ATLAS', '1806.01762_ATLAS_Fig4a_pp_XX_Wt.dat',                        'pp --> XX --> Wt --> 1l',       13, 36.1),
    TableEntry('11883f10a', 'arXiv:1807.11883', 'ATLAS', '1807.11883_ATLAS_Fig10a_pp_XX_Wt.dat',                       'pp --> XX --> l+l+',            13, 36.1),
    TableEntry('05263f7b',  'arXiv:2212.05263', 'ATLAS', '2212.05263_ATLAS_fig7b_pp_XX_Wt_doublet.dat',                'pp --> XX --> Wt --> 1l',       13, 139.0),
    TableEntry('05263f7f',  'arXiv:2212.05263', 'ATLAS', '2212.05263_ATLAS_fig7f_pp_XX_Wt_doublet.dat',                'pp --> XX --> Wt --> 1l',       13, 139.0),
    TableEntry('04605f10a', 'arXiv:1504.04605', 'ATLAS', '1504.04605_ATLAS_fig10a_pp_XX_Wt.dat',                       'pp --> XX --> Wt --> l+l+',      8,  20.3),
    TableEntry('08597f8ur', 'arXiv:1809.08597', 'CMS',   '1809.08597_Fig8_upper_right_pp_X_Wt_gamma_M1.dat',           'pp --> Xtq --> Wt --> 1l',      13,  35.9),
]

_Y_DOUBLET: List[TableEntry] = [
    TableEntry('08328f5',   'arXiv:1701.08328', 'CMS',   '1701.08328_CMS_Fig5_pp_Ybq_bWbq_c05.dat',                                   'pp --> Ybq --> bW --> 1l',  13,   2.3),
    TableEntry('01539f4',   'arXiv:1710.01539', 'CMS',   '1710.01539_CMS_Fig4_upper_pp_YY_Wb.dat',                                     'pp --> YY --> Wb --> 1l',   13,  35.8),
    TableEntry('03347f4a',  'arXiv:1707.03347', 'ATLAS', '1707.03347_ATLAS_fig4a_pp_YY_Wb.dat',                                        'pp --> YY --> Wb --> 1l',   13,  36.1),
    TableEntry('17165f5a',  'arXiv:2401.17165', 'ATLAS', '2401.17165_ATLAS_Fig5a_pp_YY_bW.dat',                                        'pp --> YY --> Wb --> 1l',   13, 140.0),
    TableEntry('05606f6',   'arXiv:1602.05606', 'ATLAS', '1602.05606_ATLAS_Fig6_pp_Ybj_Wb.dat',                                        'pp --> Ybq --> bW --> 1l',   8,  20.3),
    TableEntry('07343f9',   'arXiv:1812.07343', 'ATLAS', '1812.07343_fig9_pp_Y_Wb.dat',                                                'pp --> Ybq --> bW --> 1l',  13,  36.1),
    TableEntry('20273f5a',  'arXiv:2409.20273', 'ATLAS', '2409.20273_ATLAS_Fig5a_pp_Qbq_Wb_k05_Tsinglet_Ydoublet.dat',                 'pp --> Ybq --> bW --> 0l',  13, 139.0),
    TableEntry('20273f5b',  'arXiv:2409.20273', 'ATLAS', '2409.20273_ATLAS_Fig5b_pp_Qbq_Wb_k07_Tsinglet_YDoublet.dat',                 'pp --> Ybq --> bW --> 0l',  13, 139.0),
]

# Y-Triplet reuses the first 4 entries of Y-Doublet
_Y_TRIPLET: List[TableEntry] = _Y_DOUBLET[:4]

_T_SINGLET: List[TableEntry] = [
    TableEntry('10751fig6b', 'arXiv:1705.10751',      'ATLAS', '1705.10751_ATLAS_fig6b_pp_TT_Zt_Singlet.txt',                           'pp --> TT --> 1l',                             13,  36.1),
    TableEntry('73270',      'arXiv:2209.07327',      'CMS',   '2209.07327_CMS_f9a_pp_TTbar_Singlet.txt',                               'pp --> TT --> 1l+l+l++3l',                     13, 138.0),
    TableEntry('33470fig4b', 'arXiv:1707.03347',      'ATLAS', '1707.03347_ATLAS_fig4b_pp_TT_Singlet.txt',                              'pp --> TT --> 1l',                             13,  36.1),
    TableEntry('05263',      'arXiv:2212.05263',      'ATLAS', '2212.05263_ATLAS_fig7c_pp_TT_Zt_Singlet.txt',                           'pp --> TT --> 1l',                             13, 139.0),
    TableEntry('10555',      'arXiv:1806.10555',      'ATLAS', '1806.10555_ATLAS_Fig-13_a_pp_TT_Zt_singlet.txt',                        'pp --> TT --> l+l-,≥3l',                       13,  36.1),
    TableEntry('04758',      'arXiv:1805.04758',      'CMS',   '1805.04758_CMS_Fig8-upper-row-left_pp_TT_bW_Zt_tH_Singlet.txt',         'pp --> TT --> 1l+l+l++3l',                     13,  35.9),
    TableEntry('11883',      'arXiv:1807.11883',      'ATLAS', '1807.11883_ATLAS_pp_TT_Wb_Zt_Ht_Fig_8_b_Singlet.txt',                  'pp --> TT --> l+l+',                           13,  36.1),
    TableEntry('03408',      'arXiv:1706.03408',      'CMS',   '1706.03408_CMS_Fig-12-left_pp_TT_bW_Zt_tH_Singlet.txt',                'pp --> TT --> 1l',                             13,   2.6),
    TableEntry('5500fc',     'arXiv:1409.5500',       'ATLAS', '1409.5500_ATLAS_Fig-12-c_pp_TT_Zt_Singlet.txt',                         'pp --> TT --> l+l-+3l',                         8,  20.3),
    TableEntry('04306fb',    'arXiv:1505.04306',      'ATLAS', '1505.04306_ATLAS_Fig18-b_pp_TT_Ht+X-Wb+X_Singlet.txt',                  'pp --> TT --> 1l',                              8,  20.3),
    TableEntry('02227fa',    'arXiv:2201.02227',      'CMS',   '2201.02227_CMS_f8a_pp_Tbq_tZ_gamma_mT_0.05_Singlet.txt',                'pp --> Tbq --> tZbq --> 0l',                   13, 137.0),
    TableEntry('02227fb',    'arXiv:2201.02227',      'CMS',   '2201.02227_CMS_f8b_pp_Tbq_tZ_gamma_mT_0.1_Singlet.txt',                 'pp --> Tbq --> tZbq --> 0l',                   13, 137.0),
    TableEntry('02227fc',    'arXiv:2201.02227',      'CMS',   '2201.02227_CMS_fig8c_pp_Tbq_tZ_gamma_mT_0.2_Singlet.txt',               'pp --> Tbq --> tZbq --> 0l',                   13, 137.0),
    TableEntry('02227fd',    'arXiv:2201.02227',      'CMS',   '2201.02227_CMS_fig8d_pp_Tbq_tZ_gamma_mT_0.3_Singlet.txt',               'pp --> Tbq --> tZbq --> 0l',                   13, 137.0),
    TableEntry('01062f5a',   'arXiv:1708.01062',      'CMS',   '1708.01062_CMS_Fig5-left_pp_Tbq_tZbq_Singlet-LH.txt',                  'pp --> Tbq --> tZbq --> l+l-',                 13,  35.9),
    TableEntry('17605f35',   'arXiv:2405.17605',      'CMS',   '2405.17605_CMS_fig35_pp_Tbq_singlet.dat',                               'pp --> Tbq --> 0l',                            13, 138.0),
    TableEntry('12802',      'arXiv:2302.12802',      'CMS',   '2302.12802_CMS_f4_pp_Tbq_tH_Singlet.txt',                               'pp --> Tbq --> tHbq --> 0l+1l',                13, 138.0),
    TableEntry('00999f10a',  'arXiv:1612.00999',      'CMS',   '1612.00999_CMS_Fig10-left_pp_TT_tH.txt',                                'pp --> Tbq --> tHbq --> 0l',                   13,   2.3),
    TableEntry('04721f8a',   'arXiv:1909.04721',      'CMS',   '1909.04721_CMS_Fig8_upper-row-left_pp_Tbq_tHbq.txt',                    'pp --> Tbq --> tHbq --> 0l',                   13,  35.9),
    TableEntry('04721f8b',   'arXiv:1909.04721',      'CMS',   '1909.04721_CMS_Fig8_upper-row-right_pp_Tbq_tHbq.txt',                   'pp --> Tbq --> tHbq --> 0l',                   13,  35.9),
    TableEntry('04721f8c',   'arXiv:1909.04721',      'CMS',   '1909.04721_CMS_Fig8_middle-row-left_pp_Tbq_tZbq.txt',                   'pp --> Tbq --> tZbq --> 0l',                   13,  35.9),
    TableEntry('04721f8d',   'arXiv:1909.04721',      'CMS',   '1909.04721_CMS_Fig8_middle-row-right_pp_Tbq_tZbq.txt',                  'pp --> Tbq --> tZbq --> 0l',                   13,  35.9),
    TableEntry('04721f8e',   'arXiv:1909.04721',      'CMS',   '1909.04721_CMS_Fig8_lower-row-left_pp_Tbq_tH+tZ_bq.txt',                'pp --> Tbq --> (tZ + tH)bq --> 0l',            13,  35.9),
    TableEntry('04721f8f',   'arXiv:1909.04721',      'CMS',   '1909.04721_CMS_Fig8_lower-row-right_pp_Tbq_tH+tZ_bq.txt',               'pp --> Tbq --> (tZ + tH)bq --> 0l',            13,  35.9),
    TableEntry('04721f9a',   'arXiv:1909.04721',      'CMS',   '1909.04721_CMS_Fig9_upper-row-left_pp_Tbq_tHbq.txt',                    'pp --> Tbq --> tHbq --> 0l',                   13,  35.9),
    TableEntry('04721f9b',   'arXiv:1909.04721',      'CMS',   '1909.04721_CMS_Fig9_upper-row-right_pp_Tbq_tHbq.txt',                   'pp --> Tbq --> tHbq --> 0l',                   13,  35.9),
    TableEntry('04721f9c',   'arXiv:1909.04721',      'CMS',   '1909.04721_CMS_Fig9_middle-row-left_pp_Tbq_tZbq.txt',                   'pp --> Tbq --> tZbq --> 0l',                   13,  35.9),
    TableEntry('04721f9d',   'arXiv:1909.04721',      'CMS',   '1909.04721_CMS_Fig9_middle-row-right_pp_Tbq_tZbq.txt',                  'pp --> Tbq --> tZbq --> 0l',                   13,  35.9),
    TableEntry('04721f9e',   'arXiv:1909.04721',      'CMS',   '1909.04721_CMS_Fig9_lower-row-left_pp_Tbq_tHbq_tZbq.txt',               'pp --> Tbq --> (tZ + tH)bq --> 0l',            13,  35.9),
    TableEntry('04721f9f',   'arXiv:1909.04721',      'CMS',   '1909.04721_CMS_Fig9_lower-row-right_pp_Tbq_tHbq_tZbq.txt',              'pp --> Tbq --> (tZ + tH)bq --> 0l',            13,  35.9),
    TableEntry('05606f6',    'arXiv:1602.05606',      'ATLAS', '1602.05606_ATLAS_Fig6_pp_Tbj_Wb_singlet.txt',                           'pp --> Tbq --> bWbq --> 1l',                    8,  20.3),
    TableEntry('07409f4a',   'arXiv:1701.07409',      'CMS',   '1701.07409_CMS_Fig4left_pp_Tb_tZ_singlet.txt',                          'pp --> Tbq --> tZbq --> 0l',                   13,   2.3),
    TableEntry('03401f11a',  'arXiv:2305.03401',      'ATLAS', '2305.03401_ATLAS_Fig11a_pp_Tqt_Wb_Ht_Zt_singlet-k02.txt',               'pp --> Tb(t)q --> tZ(H)b(t)q --> 1l',          13, 139.0),
    TableEntry('03401f11b',  'arXiv:2305.03401',      'ATLAS', '2305.03401_ATLAS_Fig11b_pp_Tqt_Wb_Ht_Zt_singlet-k04.txt',               'pp --> Tb(t)q --> tZ(H)b(t)q --> 1l',          13, 139.0),
    TableEntry('03401f11c',  'arXiv:2305.03401',      'ATLAS', '2305.03401_ATLAS_Fig11c_pp_Tqt_Wb_Ht_Zt_singlet-k06.txt',               'pp --> Tb(t)q --> tZ(H)b(t)q --> 1l',          13, 139.0),
    TableEntry('16561f9c',   'arXiv:2402.16561',      'ATLAS', '2402.16561_ATLAS_Fig9c_pp_T_Ht_Zt_singlet.txt',                         'pp --> Tb(t)q --> tZb(t)q --> 0l',             13, 139.0),
    TableEntry('09743f4c',   'arXiv:1812.09743',      'ATLAS', '1812.09743_ATLAS_Fig4c_pp_Tbq_Wb_Ht_Zt_singlet.txt',                    'pp --> Tbq --> tZbq --> 0l+1l',                13,  36.1),
    TableEntry('07045f8a',   'arXiv:2201.07045',      'ATLAS', '2201.07045_ATLAS_Fig8-a_pp_TT_tH_k_T-0.1_singlet.txt',                  'pp --> Tbq --> tHbq --> 0l',                   13, 139.0),
    TableEntry('07045f8b',   'arXiv:2201.07045',      'ATLAS', '2201.07045_ATLAS_Fig8-b_pp_TT_tH_k_T-0.3_singlet.txt',                  'pp --> Tbq --> tHbq --> 0l',                   13, 139.0),
    TableEntry('07045f8c',   'arXiv:2201.07045',      'ATLAS', '2201.07045_ATLAS_Fig8-c_pp_TT_tH_k_T-0.5_singlet.txt',                  'pp --> Tbq --> tHbq --> 0l',                   13, 139.0),
    TableEntry('07045f8d',   'arXiv:2201.07045',      'ATLAS', '2201.07045_ATLAS_Fig8-d_pp_TT_tH_k_T-0.7_singlet.txt',                  'pp --> Tbq --> tHbq --> 0l',                   13, 139.0),
    TableEntry('07045f8e',   'arXiv:2201.07045',      'ATLAS', '2201.07045_ATLAS_Fig8-e_pp_TT_tH_k_T-0.9_singlet.txt',                  'pp --> Tbq --> tHbq --> 0l',                   13, 139.0),
    TableEntry('07045f8f',   'arXiv:2201.07045',      'ATLAS', '2201.07045_ATLAS_Fig8-f_pp_TT_tH_k_T-1.1_singlet.txt',                  'pp --> Tbq --> tHbq --> 0l',                   13, 139.0),
    TableEntry('07584f8a',   'arXiv:2307.07584',      'ATLAS', '2307.07584_ATLAS_Fig8a_pp_T_Wb_Ht_Zt_singlet_k03.txt',                  'pp --> Tb(t)q --> tZb(t)q --> l+l-+3l',        13, 139.0),
    TableEntry('07584f8c',   'arXiv:2307.07584',      'ATLAS', '2307.07584_ATLAS_Fig8c_pp_T_Wb_Ht_Zt_singlet_k05.txt',                  'pp --> Tb(t)q --> tZb(t)q --> l+l-+3l',        13, 139.0),
    TableEntry('07584f8e',   'arXiv:2307.07584',      'ATLAS', '2307.07584_ATLAS_Fig8e_pp_T_Wb_Ht_Zt_singlet_k07.txt',                  'pp --> Tb(t)q --> tZb(t)q --> l+l-+3l',        13, 139.0),
    TableEntry('05336f4ul',  'arXiv:1612.05336',      'CMS',   '1612.05336_CMS_fig4_upper_left_pp_Tbq_tHbq_LH_coupling.txt',            'pp --> Tbq --> tHbq --> 0l',                   13,   2.3),
    TableEntry('032f6b',     'ATLAS-CONF-2016-032',   'ATLAS', 'ATLAS-CONF-2016-032_ATLAS_Fig6b_pp_TT_Wb_Zt_Ht_Singlet.txt',            'pp --> TT --> l+l+',                           13,   3.2),
    TableEntry('104f16a',    'ATLAS-CONF-2016-104',   'ATLAS', 'ATLAS-CONF-2016-104_ATLAS_Fig16b_pp_TT_HtX_singlet.txt',                'pp --> TT --> 0l',                             13,  13.2),
    TableEntry('7667f6',     'arXiv:1311.7667',       'CMS',   '1311.7667_CMS_Fig6_pp_TT_bW_tH_Zt.txt',                                'pp --> TT --> 1l',                              8,  19.5),
    TableEntry('05071f4ur',  'arXiv:2405.05071',      'CMS',   '2405.05071_CMS_Fig7_upper_right_pp_Tbq_tZbq.txt',                       'pp --> Tbq --> tZbq --> tbbbq --> 0l',          13, 138.0),
    TableEntry('05071f4ul',  'arXiv:2405.05071',      'CMS',   '2405.05071_CMS_Fig7_upper_left_pp_Tbq_tHbq.txt',                        'pp --> Tbq --> tHbq --> tbbbq --> 0l',          13, 138.0),
    TableEntry('05071f4ll',  'arXiv:2405.05071',      'CMS',   '2405.05071_CMS_Fig7_lower_left_pp_Tbq_tZbq_tHbq.txt',                   'pp --> Tbq --> (tH + tZ)bq --> tbbbq --> 0l',  13, 138.0),
    TableEntry('05071f4lr',  'arXiv:2405.05071',      'CMS',   '2405.05071_CMS_Fig7_lower_right_pp_Tbq_tZbq_tHbq.txt',                  'pp --> Tbq --> (tH + tZ)bq --> tbbbq --> 0l',  13, 138.0),
    TableEntry('04605f7b',   'arXiv:1504.04605',      'ATLAS', '1504.04605_ATLAS_Fig7b_pp_TT_bW_tH_Zt_singlet.txt',                     'pp --> TT --> l+l+',                            8,  20.3),
    TableEntry('09678f17b',  'arXiv:1803.09678',      'ATLAS', '1803.09678_ATLAS_Fig17-b_pp_TT_Wb_Ht_Zt_Singlet.txt',                   'pp --> TT --> 1l',                             13,  36.1),
    TableEntry('15413f7a',   'arXiv:2210.15413',      'ATLAS', '2210.15413_ATLAS_Fig7-a_pp_TT_Wb-Zt_Ht_Singlet.txt',                    'pp --> TT --> l+l-+3l',                        13, 139.0),
    TableEntry('10555f15',   'arXiv:1806.10555',      'ATLAS', '1806.10555_ATLAS_Fig15_pp_T_Zt_Singlet.txt',                             'pp --> Tbq --> tZbq --> l+l-+>=3l',            13,  36.1),
    TableEntry('08328',      'arXiv:1701.08328',      'CMS',   '1701.08328_CMS_fig5_pp_Tbq_or_Ybq_bW.txt',                              'pp --> Tbq --> bWbq --> 1l',                   13,   2.3),
    TableEntry('20273f5a',   'arXiv:2409.20273',      'ATLAS', '2409.20273_ATLAS_Fig5a_pp_Qbq_Wb_k05_Tsinglet_Ydoublet.dat',            'pp --> Tbq --> bWbq --> 0l',                   13, 139.0),
    TableEntry('20273f5b',   'arXiv:2409.20273',      'ATLAS', '2409.20273_ATLAS_Fig5b_pp_Qbq_Wb_k07_Tsinglet_YDoublet.dat',            'pp --> Tbq --> bWbq --> 0l',                   13, 139.0),
]

_T_DOUBLET: List[TableEntry] = [
    TableEntry('10751',      'arXiv:1705.10751',    'ATLAS', '1705.10751_ATLAS_fig6c_pp_TT_Doublet.txt',                              'pp --> TT --> 1l',                       13,  36.1, 'XTorTB'),
    TableEntry('07327',      'arXiv:2209.07327',    'CMS',   '2209.07327_CMS_f9b_pp_TTbar_Doublet.txt',                               'pp --> TT --> 1l+l+l++3l',               13, 138.0, 'XTorTB'),
    TableEntry('05263',      'arXiv:2212.05263',    'ATLAS', '2212.05263_ATLAS_fig7e_pp_TT_Zt_T,B_or_X,T_Doublet.txt',               'pp --> TT --> 1l',                       13,  36.1, 'XTorTB'),
    TableEntry('10555',      'arXiv:1806.10555',    'ATLAS', '1806.10555_ATLAS_Fig-13_c_pp_TT_Zt_doublet.txt',                        'pp --> TT --> l+l-+>=3l',                13, 139.0, 'XT'),
    TableEntry('04758',      'arXiv:1805.04758',    'CMS',   '1805.04758_CMS_Fig8-upper-row-right_pp_TT_Zt_tH_Doublet.txt',           'pp --> TT --> 1l+l+l++3l',               13,  35.9, 'XTorTB'),
    TableEntry('00999f10b',  'arXiv:1612.00999',    'CMS',   '1612.00999_CMS_Fig10-right_pp_Ttq_tH.txt',                              'pp --> Ttq --> tHtq --> 1l',             13,   2.3, 'XTorTB'),
    TableEntry('03408',      'arXiv:1706.03408',    'CMS',   '1706.03408_CMS_Fig-12-right_pp_TT_Zt_tH_Doublet.txt',                   'pp --> TT --> 1l',                       13,   2.6, 'XTorTB'),
    TableEntry('01062f5b',   'arXiv:1708.01062',    'CMS',   '1708.01062_CMS_Fig5-right_pp_Ttq_tZtq_Doublet-RH.txt',                  'pp --> Ttq --> tZtq --> l+l-',           13,  35.9, 'XTorTB'),
    TableEntry('5500fd',     'arXiv:1409.5500',     'ATLAS', '1409.5500_ATLAS_Fig-12-d_pp_TT_Zt_doublet.txt',                         'pp --> TT --> l+l-+3l',                   8,  20.3, 'TB'),
    TableEntry('04721f10a',  'arXiv:1909.04721',    'CMS',   '1909.04721_CMS_Fig10_upper-row-left_pp_Ttq_tHtq.txt',                    'pp --> Ttq --> tHtq --> 0l',             13,  35.9, 'TB'),
    TableEntry('04721f10b',  'arXiv:1909.04721',    'CMS',   '1909.04721_CMS_Fig10_upper-row-right_pp_Ttq_tHtq.txt',                   'pp --> Ttq --> tHtq --> 0l',             13,  35.9, 'TB'),
    TableEntry('04721f10c',  'arXiv:1909.04721',    'CMS',   '1909.04721_CMS_Fig10_middle-row-left_pp_Ttq_tZtq.txt',                   'pp --> Ttq --> tZtq --> 0l',             13,  35.9, 'TB'),
    TableEntry('04721f10d',  'arXiv:1909.04721',    'CMS',   '1909.04721_CMS_Fig10_middle-row-right_pp_Ttq_tZtq.txt',                  'pp --> Ttq --> tZtq --> 0l',             13,  35.9, 'TB'),
    TableEntry('04721f10e',  'arXiv:1909.04721',    'CMS',   '1909.04721_CMS_Fig10_lower-row-left_pp_Ttq_tH-tZ_tq.txt',                'pp --> Ttq --> (tZ + tH)tq --> 0l',     13,  35.9, 'TB'),
    TableEntry('04721f10f',  'arXiv:1909.04721',    'CMS',   '1909.04721_CMS_Fig10_lower-row-right_pp_Ttq_tH-tZ_tq.txt',               'pp --> Ttq --> (tZ + tH)tq --> 0l',     13,  35.9, 'TB'),
    TableEntry('04721f11a',  'arXiv:1909.04721',    'CMS',   '1909.04721_CMS_Fig11_upper-row-left_pp_Ttq_tHtq.txt',                    'pp --> Ttq --> tHtq --> 0l',             13,  35.9, 'TB'),
    TableEntry('04721f11b',  'arXiv:1909.04721',    'CMS',   '1909.04721_CMS_Fig11_upper-row-right_pp_Ttq_tHtq.txt',                   'pp --> Ttq --> tHtq --> 0l',             13,  35.9, 'TB'),
    TableEntry('04721f11c',  'arXiv:1909.04721',    'CMS',   '1909.04721_CMS_Fig11_middle-row-left_pp_Ttq_tZtq.txt',                   'pp --> Ttq --> tZtq --> 0l',             13,  35.9, 'TB'),
    TableEntry('04721f11d',  'arXiv:1909.04721',    'CMS',   '1909.04721_CMS_Fig11_middle-row-right_pp_Ttq_tZtq.txt',                  'pp --> Ttq --> tZtq --> 0l',             13,  35.9, 'TB'),
    TableEntry('04721f11e',  'arXiv:1909.04721',    'CMS',   '1909.04721_CMS_Fig11_lower-row-left_pp_Ttq_tZ-tH_tq.txt',                'pp --> Ttq --> (tZ + tH)tq --> 0l',     13,  35.9, 'TB'),
    TableEntry('04721f11f',  'arXiv:1909.04721',    'CMS',   '1909.04721_CMS_Fig11_lower-row-right_pp_Ttq_tZ-tH_tq.txt',               'pp --> Ttq --> (tZ + tH)tq --> 0l',     13,  35.9, 'TB'),
    TableEntry('07409f4b',   'arXiv:1701.07409',    'CMS',   '1701.07409_CMS_Fig4right_pp_Tt_tZ_doublet.txt',                          'pp --> Ttq --> tZtq --> 0l',             13,   2.3, 'XTorTB'),
    TableEntry('04306fc',    'arXiv:1505.04306',    'ATLAS', '1505.04306_ATLAS_Fig18-c_pp_TT_Ht+X_Doublet.txt',                        'pp --> TT --> 1l',                        8,  20.3, 'XTorTB'),
    TableEntry('03401f12a',  'arXiv:2305.03401',    'ATLAS', '2305.03401_ATLAS_Fig12a_pp_Tqt_Ht_Zt_doublet-k02.txt',                   'pp --> Tb(t)q --> tZ(H)b(t)q --> 1l',   13, 139.0, 'TB'),
    TableEntry('03401f12b',  'arXiv:2305.03401',    'ATLAS', '2305.03401_ATLAS_Fig12b_pp_Tqt_Ht_Zt_doublet-k04.txt',                   'pp --> Tb(t)q --> tZ(H)b(t)q --> 1l',   13, 139.0, 'TB'),
    TableEntry('03401f12c',  'arXiv:2305.03401',    'ATLAS', '2305.03401_ATLAS_Fig12c_pp_Tqt_Ht_Zt_doublet-k06.txt',                   'pp --> Tb(t)q --> tZ(H)b(t)q --> 1l',   13, 139.0, 'TB'),
    TableEntry('07584f8b',   'arXiv:2307.07584',    'ATLAS', '2307.07584_ATLAS_Fig8b_pp_T_Ht_Zt_doublet_k03.txt',                       'pp --> Ttq --> tZtq --> l+l-+3l',       13, 139.0, 'XTorTB'),
    TableEntry('07584f8d',   'arXiv:2307.07584',    'ATLAS', '2307.07584_ATLAS_Fig8d_pp_T_Ht_Zt_doublet_k05.txt',                       'pp --> Ttq --> tZtq --> l+l-+3l',       13, 139.0, 'XTorTB'),
    TableEntry('07584f8f',   'arXiv:2307.07584',    'ATLAS', '2307.07584_ATLAS_Fig8f_pp_T_Ht_Zt_doublet_k07.txt',                       'pp --> Ttq --> tZtq --> l+l-+3l',       13, 139.0, 'XTorTB'),
    TableEntry('05336f4lr',  'arXiv:1612.05336',    'CMS',   '1612.05336_CMS_fig4_lower_right_pp_Tbq_tHbq_RH_coupling.txt',             'pp --> Ttq --> tHtq --> 0l',             13,   2.3, 'XTorTB'),
    TableEntry('104f16a',    'ATLAS-CONF-2016-104', 'ATLAS', 'ATLAS-CONF-2016-104_ATLAS_Fig16a_pp_TT_HtX_doublet.txt',                  'pp --> TT --> 0l+1l',                   13,  13.2, 'XTorTB'),
    TableEntry('09678f17a',  'arXiv:1803.09678',    'ATLAS', '1803.09678_ATLAS_Fig17-a_pp_TT_Ht_Zt_Doublet.txt',                        'pp --> TT --> 1l',                      13,  36.1, 'XTorTB'),
    TableEntry('15413f7c',   'arXiv:2210.15413',    'ATLAS', '2210.15413_ATLAS_Fig7-c_pp_TT_Zt_Ht_Doublet-X-T.txt',                    'pp --> TT --> l+l-+3l',                 13, 139.0, 'XT'),
]

_T_PURE: List[TableEntry] = [
    TableEntry('05263',     'arXiv:2212.05263',      'ATLAS', '2212.05263_ATLAS_fig7a_pp_TT_tZ.txt',                         'pp --> TT --> ZtZt --> 1l',               13, 139.0),
    TableEntry('97680',     'arXiv:1812.09768',      'CMS',   '1812.09768_CMS_fig4a_pp_TT_tZ.txt',                           'pp --> TT --> ZtZt --> l+l-',             13,  36.1),
    TableEntry('10751fig6a','arXiv:1705.10751',      'ATLAS', '1705.10751_ATLAS_fig6a_pp_TT_Zt.txt',                         'pp --> TT --> ZtZt --> 1l',               13,  36.1),
    TableEntry('17710',     'arXiv:1808.01771',      'ATLAS', '1808.01771_ATLAS_fig13a_pp_TT_Ht.txt',                        'pp --> TT --> HtHt --> 0l',               13,  36.1),
    TableEntry('19520',     'arXiv:1503.01952',      'CMS',   '1503.01952_CMS_fig13_pp_TT_tH.txt',                           'pp --> TT --> HtHt --> 0l',                8,  19.7),
    TableEntry('33470fig4a','arXiv:1707.03347',      'ATLAS', '1707.03347_ATLAS_fig4a_pp_TT_Wb.txt',                         'pp --> TT --> WbWb --> 1l',               13,  36.1),
    TableEntry('10555',     'arXiv:1806.10555',      'ATLAS', '1806.10555_ATLAS_Fig-13e_pp_TT_Zt.txt',                       'pp --> TT --> ZtZt --> l+l-',             13,  36.1),
    TableEntry('04177bW',   'arXiv:1509.04177',      'CMS',   '1509.04177_CMS_fig8_pp_TT_bW.txt',                            'pp --> TT --> WbWb --> 0l+1l+2l',          8,  19.7),
    TableEntry('04177tH',   'arXiv:1509.04177',      'CMS',   '1509.04177_CMS_fig8_pp_TT_tH.txt',                            'pp --> TT --> HtHt --> 0l+1l+2l',          8,  19.7),
    TableEntry('04177tZ',   'arXiv:1509.04177',      'CMS',   '1509.04177_CMS_fig8_pp_TT_tZ.txt',                            'pp --> TT --> ZtZt --> 0l+1l+2l',          8,  19.7),
    TableEntry('03408bW',   'arXiv:1706.03408',      'CMS',   '1706.03408_CMS_Fig-11-left_pp_TT_bW.txt',                     'pp --> TT --> WbWb --> 1l',               13,   2.6),
    TableEntry('03408tH',   'arXiv:1706.03408',      'CMS',   '1706.03408_CMS_Fig-11-right_pp_TT_tH.txt',                    'pp --> TT --> HtHt --> 1l',               13,   2.6),
    TableEntry('0471fa',    'arXiv:1209.0471',       'CMS',   '1209.0471_CMS_Fig6_upper_pp_TT_bW.txt',                       'pp --> TT --> WbWb --> 1l',               13,   2.6),
    TableEntry('0471fb',    'arXiv:1209.0471',       'CMS',   '1209.0471_CMS_Fig6_middle_pp_TT_bW.txt',                      'pp --> TT --> WbWb --> 1l',                7,   5.0),
    TableEntry('0471fc',    'arXiv:1209.0471',       'CMS',   '1209.0471_CMS_Fig6_lower_pp_TT_bW.txt',                       'pp --> TT --> WbWb --> 1l',                7,   5.0),
    TableEntry('04306fa',   'arXiv:1505.04306',      'ATLAS', '1505.04306_ATLAS_Fig18-a_pp_TT_Wb+X.txt',                     'pp --> TT --> WbWb --> 1l',                8,  20.3),
    TableEntry('5468',      'arXiv:1210.5468',       'ATLAS', '1210.5468_ATLAS_Fig-3_pp_tt_Wb.txt',                          'pp --> TT --> WbWb --> 1l',                7,   4.7),
    TableEntry('01539',     'arXiv:1710.01539',      'CMS',   '1710.01539_CMS_Fig4_upper_pp_TT_bW.txt',                      'pp --> TT --> WbWb --> 1l',               13,  35.8),
    TableEntry('104f15a',   'ATLAS-CONF-2016-104',   'ATLAS', 'ATLAS-CONF-2016-104_ATLAS_Fig15a_pp_TT_tH.txt',               'pp --> TT --> HtHt --> 0l+1l',            13,  13.2),
    TableEntry('104f15b',   'ATLAS-CONF-2016-104',   'ATLAS', 'ATLAS-CONF-2016-104_ATLAS_Fig15b_pp_TT_tZ.txt',               'pp --> TT --> ZtZt --> 0l+1l',            13,  13.2),
    TableEntry('11903fa',   'arXiv:1906.11903',      'CMS',   '1906.11903_CMS_Fig6_lower_left_pp_TT_bW.txt',                 'pp --> TT --> WbWb --> 0l',               13,  35.9),
    TableEntry('11903fc',   'arXiv:1906.11903',      'CMS',   '1906.11903_CMS_Fig6_upper_left_pp_TT_tZ.txt',                 'pp --> TT --> ZtZt --> 0l',               13,  35.9),
    TableEntry('11903ff',   'arXiv:1906.11903',      'CMS',   '1906.11903_CMS_Fig6_middle_left_pp_TT_tH.txt',                'pp --> TT --> HtHt --> 0l',               13,  35.9),
    TableEntry('5410f2',    'arXiv:1203.5410',       'CMS',   '1203.5410_CMS_Fig2_pp_tt_bWbW.txt',                           'pp --> TT --> WbWb --> l+l-',              7,   5.0),
    TableEntry('3076f2',    'arXiv:1202.3076',       'ATLAS', '1202.3076_ATLAS_Fig2_pp_tt_WbWb.txt',                         'pp --> TT --> WbWb --> 1l',                7,   1.04),
    TableEntry('03903f9',   'arXiv:1606.03903',      'ATLAS', '1606.03903_ATLAS_Fig9_pp_TT_Zt.txt',                          'pp --> TT --> ZtZt --> 1l',               13,   3.2),
    TableEntry('15413f7e',  'arXiv:2210.15413',      'ATLAS', '2210.15413_ATLAS_Fig7-e_pp_TT_Zt.txt',                        'pp --> TT --> ZtZt --> l+l-',             13, 139.0),
    TableEntry('17165f5a',  'arXiv:2401.17165',      'ATLAS', '2401.17165_ATLAS_Fig5a_pp_TT_bW.dat',                         'pp --> TT --> WbWb --> 1l + jets',        13, 140.0),
    TableEntry('07327fwb',  'arXiv:2209.07327',      'CMS',   '2209.07327_CMS_Table11_pp_TT_Wb.dat',                         'pp --> TT --> WbWb --> >=1l + jets',      13, 138.0),
    TableEntry('07327fzt',  'arXiv:2209.07327',      'CMS',   '2209.07327_CMS_Table11_pp_TT_Zt.dat',                         'pp --> TT --> ZtZt --> >=1l + jets',      13, 138.0),
    TableEntry('07327fht',  'arXiv:2209.07327',      'CMS',   '2209.07327_CMS_Table11_pp_TT_Ht.dat',                         'pp --> TT --> HtHt --> >=1l + jets',      13, 138.0),
]

# Map model type → catalogue
_CATALOGUE: Dict[type, List[TableEntry]] = {
    SingletB:  _B_SINGLET,
    DoubletB:  _B_DOUBLET,
    PureB:     _B_PURE,
    DoubletX:  _X_DOUBLET,
    DoubletY:  _Y_DOUBLET,
    TripletY:  _Y_TRIPLET,
    SingletT:  _T_SINGLET,
    DoubletT:  _T_DOUBLET,
    PureT:     _T_PURE,
}

# VLQ tag used in load_data_from_files
_VLQ_TAG: Dict[type, str] = {
    SingletB: 'B', DoubletB: 'B', PureB: 'B',
    DoubletX: 'X',
    DoubletY: 'Y', TripletY: 'Y',
    SingletT: 'T', DoubletT: 'T', PureT: 'T',
}

# Mass-array attribute name per VLQ family
_MASS_ATTR: Dict[type, str] = {
    SingletB: 'MB', DoubletB: 'MB', PureB: 'MB',
    DoubletX: 'MX',
    DoubletY: 'MY', TripletY: 'MY',
    SingletT: 'MT', DoubletT: 'MT', PureT: 'MT',
}

# Pair-production prefixes per VLQ family
_PAIR_PREFIX: Dict[str, str] = {
    'B': 'pp --> BB',
    'X': 'pp --> XX',
    'Y': 'pp --> YY',
    'T': 'pp --> TT',
}

# Single-production prefixes per VLQ family
_SINGLE_PREFIXES: Dict[str, tuple] = {
    'B': ('pp --> Bb', 'pp --> Bt'),
    'X': ('pp --> Xt',),
    'Y': ('pp --> Yb',),
    'T': ('pp --> Tb', 'pp --> Tt'),
}


# ---------------------------------------------------------------------------
# Tables class
# ---------------------------------------------------------------------------

class Tables:
    """
    Loads and holds experimental limits tables for a given VLQ model.

    After construction call ``initialize_tables_cms_and_atlas()`` to populate
    the numpy arrays, then ``cs_dict()`` / ``tb_xt_dict()`` to build the
    key-grouping dictionaries.
    """

    def __init__(self, m) -> None:
        self.m = m

        # Per-entry metadata (populated from catalogue)
        self.key: List[str] = []
        self.label: List[str] = []
        self.expt: List[str] = []
        self.file_name: List[str] = []
        self.process: List[str] = []
        self.energy: List[int] = []
        self.luminosity: List[float] = []
        self.which_doublet: Optional[List[Optional[str]]] = None

        # Per-entry numerical data (populated by load_data_from_files)
        self.exp: List[Optional[NDArray[np.float64]]] = []
        self.obs: List[Optional[NDArray[np.float64]]] = []

        # Mass arrays – only the one relevant to this VLQ type is initialised
        self.MB: Optional[List[Optional[NDArray[np.float64]]]] = None
        self.MX: Optional[List[Optional[NDArray[np.float64]]]] = None
        self.MY: Optional[List[Optional[NDArray[np.float64]]]] = None
        self.MT: Optional[List[Optional[NDArray[np.float64]]]] = None

        # Key-grouping dicts
        self.cs_keys: Dict[str, List[str]] = {}
        self.TB_XT_keys: Dict[str, List[str]] = {}
        self.TB_YB_keys: Dict[str, List[str]] = {}

        # Convenience flags (set once, queried cheaply)
        self.VLB: bool = isinstance(m, (SingletB, DoubletB, PureB))
        self.VLX: bool = isinstance(m, DoubletX)
        self.VLY: bool = isinstance(m, (DoubletY, TripletY))

        self._load_catalogue()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load_catalogue(self) -> None:
        """Populate metadata lists from the static catalogue."""
        entries = _CATALOGUE.get(type(self.m))
        if not entries:
            raise ValueError(f"No catalogue defined for model type {type(self.m)}")

        n = len(entries)
        mass_attr = _MASS_ATTR[type(self.m)]
        has_doublet = any(e.which_doublet is not None for e in entries)

        self.key          = [e.key         for e in entries]
        self.label        = [e.label       for e in entries]
        self.expt         = [e.expt        for e in entries]
        self.file_name    = [e.file_name   for e in entries]
        self.process      = [e.process     for e in entries]
        self.energy       = [e.energy      for e in entries]
        self.luminosity   = [e.luminosity  for e in entries]

        if has_doublet:
            self.which_doublet = [e.which_doublet for e in entries]

        setattr(self, mass_attr, [None] * n)
        self.exp = [None] * n
        self.obs = [None] * n

    @property
    def _vlq_tag(self) -> str:
        return _VLQ_TAG[type(self.m)]

    @property
    def _mass_list(self) -> List:
        return getattr(self, _MASS_ATTR[type(self.m)])

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def initialize_tables_cms_and_atlas(self) -> None:
        """Fill numerical data by reading the data files."""
        load_data_from_files(
            self.file_name,
            len(self.key),
            self._mass_list,
            self.exp,
            self.obs,
            self.expt,
            vlq=self._vlq_tag,
        )

    def all_processes(self) -> None:
        """Write a human-readable summary of all loaded channels."""
        import os
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'keys', 'coupling_info.dat')
        )
        with open(file_path, "w") as f:
            f.write("************* File for each cross section limit information*****************\n")
            f.write("This File has been generated with PyTop version 0.1\n")
            f.write(f"With the T quark in the {self.m.model()} scenario\n")
            for i, proc in enumerate(self.process):
                f.write("***********************************************************************\n")
                f.write(f"channel {i}:\n")
                f.write(
                    f"{proc} \t\t {self.label[i]} ({self.expt[i]}) "
                    f"\t sqrt(s) = {self.energy[i]} TeV"
                    f"\t luminosity = {self.luminosity[i]} fb-1\n"
                )

    def cs_dict(self) -> None:
        """Group keys by pair vs single production."""
        tag = self._vlq_tag
        pair_pfx   = _PAIR_PREFIX[tag]
        single_pfx = _SINGLE_PREFIXES[tag]

        self.cs_keys = {
            'pair_prod':   [k for k, p in zip(self.key, self.process) if p.startswith(pair_pfx)],
            'single_prod': [k for k, p in zip(self.key, self.process) if p.startswith(single_pfx)],
        }

    def tb_xt_dict(self) -> None:
        """Group doublet keys by their sub-type (TB / XT / BY)."""
        if self.which_doublet is None:
            # Singlet / Pure models have no doublet sub-grouping
            self.TB_XT_keys = {}
            self.TB_YB_keys = {}
            return

        pairs = list(zip(self.key, self.which_doublet))

        if self.VLB:
            self.TB_YB_keys = {
                '(T,B)': [k for k, d in pairs if d and d.endswith('TB')],
                '(B,Y)': [k for k, d in pairs if d and d.startswith('BY')],
            }
        elif self.VLX or self.VLY:
            self.TB_XT_keys = {}
        else:
            self.TB_XT_keys = {
                '(T,B)': [k for k, d in pairs if d and d.endswith('TB')],
                '(X,T)': [k for k, d in pairs if d and d.startswith('XT')],
            }