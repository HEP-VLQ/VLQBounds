import pandas as pd
import math

Mt = 172.52
MW = 80.377
MZ = 91.1876
Mb = 4.18
Mh = 125.09
G = 0.653
PI = math.pi
C_W = MW / MZ
Cst1 = G ** 2 / (64 * PI)
Cst2 = G ** 2 / (128 * PI * C_W ** 2)
Cst3 = G ** 2 / (128 * PI)

BR_t_Wb = 1
BR_h_bb = 0.58
BR_h_WW = 0.21
BR_h_gaga = 0.0021
BR_W_enu = 0.1046
BR_W_munu = 0.1050
BR_W_qq = 0.6832
BR_Z_ee = 0.035
BR_Z_nunu = 0.2
BR_Z_qq = 0.7
BR_Z_bb = 0.1512
Threshold = 0.01
df = pd.DataFrame(columns=["mass", "mixing", "coupling", "predicted_xs", "observed_xs",
                           "expected_xs", "width_ratio", "result",
                           "channel",  "obs_ratio", "exp_ratio", "process",
                           "experiment", "luminosity", "energy",
                           "label", "model", "which_doublet"])

T_width_mass_ratio_keys = {
    'r==0.01': {
        "Singlet": ['05071f4ur', '05071f4ul', '05071f4ll', '05071f4lr']
    },

    'r<=0.05': {
        "Singlet": ['02227fa', '12802', '04721f8a', '04721f8c', '04721f8e', '17605f35'],
        "Doublet": ['04721f10a', '04721f10c', '04721f10e']
    },

    '0.05<r<=0.3': {
        "Singlet": ['02227fb', '02227fc', '02227fd', '04721f8b',
                    '04721f8d', '04721f8f', '04721f9a', '04721f9b',
                    '04721f9c', '04721f9d', '04721f9e', '04721f9f'],
        "Doublet": ['04721f10b', '04721f10d', '04721f10f', '04721f11a', '04721f11b',
                    '04721f11c', '04721f11d', '04721f11e', '04721f11f']
    },

    'r<=0.1': {
        "Singlet": ['01062f5a', '00999f10a', '05606f6', '05336f4ul',
                    '072f8', '07409f4a', '09743f4c'],
        "Doublet": ['07409f4b', '00999f10b', '05336f4lr', '01062f5b']
    }
}

T_kappa_keys = {
    '0.2<=k<=0.6': {
        "Singlet": ['03401f11a', '03401f11b', '03401f11c'],
        "Doublet": ['03401f12a', '03401f12b', '03401f12c']
    },

    '0.1<=k<=1.1': {
        "Singlet": ['07045f8a', '07045f8b', '07045f8c', '07045f8d', '07045f8e', '07045f8f']
    },

    '0.3<=k<=0.7': {
        "Singlet": ['07584f8a', '07584f8c', '07584f8e'],
        "Doublet": ['07584f8b', '07584f8d', '07584f8f']
    },

    'k==0.5': {
        "Singlet": ['10555f15', '16561f9c', '09743f4c'],
        "Doublet": []
    }
}

B_kappa_keys = {
    '0.3<=k<=0.5': {
        "Singlet": ['02595f8a', '02595f8c', '02595f8e'],
        "Doublet": ['02595f8b', '02595f8d', '02595f8f']
    }
}

B_width_mass_ratio_keys = {

    '0.05<r<=0.3': {
        "Singlet": ['01486Fig6a', '01486Fig6b', '01486Fig6c', '01486Fig6d'],
        "Doublet": ['01486Fig6a', '01486Fig6b', '01486Fig6c', '01486Fig6d']
    },

    'r<=0.1': {
        "Singlet": ['07409f5r', '10216f4l', '10216f4r', '07409f5l', ],
        "Doublet": ['10216f4ld', '10216f4rd']
    }
}