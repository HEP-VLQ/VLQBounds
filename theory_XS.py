import os
from scipy import interpolate
import numpy as np
import pandas as pd
from glob import glob


def xs_pp_QQ_theo(mT):
    current_path = os.getcwd()
    path_to_table = 'data/Tdata/Theo_Tables/pp_QQ_NNLO.dat'
    full_path = os.path.join(current_path, path_to_table)
    try:
        table = np.loadtxt(full_path)
        MT = table[:, 0]
        xsec_pp_TT = table[:, 1]
        if np.min(MT) <= mT <= np.max(MT):
            xsec_TT = interpolate.interp1d(MT, xsec_pp_TT, 'linear')
            return xsec_TT(mT)
        else:
            return -1
    except FileNotFoundError:
        print(f"File 'pp_QQ_NNLO.dat' not found at path '{full_path}'")


def xs_pp_Vb_qWb(mT, filename, vlq='T'):
    current_path = os.getcwd()
    if vlq == 'T':
        path_to_table = 'data/Tdata/Theo_Tables/' + str(filename)
        full_path = os.path.join(current_path, path_to_table)
        try:
            table = np.loadtxt(full_path)
            MT = table[:, 0]
            xsec_pp_T_bW = table[:, 1]
            if np.min(MT) <= mT <= np.max(MT):
                xs_Tbq_wbbq = interpolate.interp1d(MT, xsec_pp_T_bW, 'linear')
                return xs_Tbq_wbbq(mT)
            else:
                return -1
        except FileNotFoundError:
            print(f"File '{filename}' not found at path '{full_path}'")
    else:
        path_to_table = 'data/Bdata/Theo_Tables/' + str(filename)
        full_path = os.path.join(current_path, path_to_table)
        try:
            table = np.loadtxt(full_path)
            MT = table[:, 0]
            xs_pp_B_tW = table[:, 1]
            if np.min(MT) <= mT <= np.max(MT):
                xs_B_tW = interpolate.interp1d(MT, xs_pp_B_tW, 'linear')
                return xs_B_tW(mT)
            else:
                return -1
        except FileNotFoundError:
            print(f"File '{filename}' not found at path '{full_path}'")


def xs_pp_Vb_qZb(mT, filename, vlq='T'):
    current_path = os.getcwd()
    if vlq == 'T':
        path_to_table = 'data/Tdata/Theo_Tables/' + str(filename)
        full_path = os.path.join(current_path, path_to_table)
        try:
            table = np.loadtxt(full_path)
            MT = table[:, 0]
            xsec_pp_T_Zt = table[:, 1]
            if np.min(MT) <= mT <= np.max(MT):
                xs_Tbq_Ztbq = interpolate.interp1d(MT, xsec_pp_T_Zt, 'linear')
                return xs_Tbq_Ztbq(mT)
            else:
                return -1
        except FileNotFoundError:
            print(f"File '{filename}' not found at path '{full_path}'")
    else:
        path_to_table = 'data/Bdata/Theo_Tables/' + str(filename)
        full_path = os.path.join(current_path, path_to_table)
        try:
            table = np.loadtxt(full_path)
            MT = table[:, 0]
            xs_pp_B_Zb = table[:, 1]
            if np.min(MT) <= mT <= np.max(MT):
                xs_Bbq_bZbq = interpolate.interp1d(MT, xs_pp_B_Zb, 'linear')
                return xs_Bbq_bZbq(mT)
            else:
                return -1
        except FileNotFoundError:
            print(f"File '{filename}' not found at path '{full_path}'")


def read_table(which_files):
    k_or_w = []
    mT = []
    xs = []
    for file in which_files:
        data = np.loadtxt(file)
        m_T = data[:, 0]
        kappa = data[:, 1]
        xsec = data[:, 2]
        xs.append(xsec)
        k_or_w.append(kappa)
        mT.append(m_T)
    xs = np.concatenate(xs)
    mT = np.concatenate(mT)
    k_or_w = np.concatenate(k_or_w)
    return mT, k_or_w, xs


def interp2d_xs_theo(file_key, model, mT, kT_or_wr, vlq='T'):
    current_path = os.getcwd()
    table = 'data/' + vlq + 'data/Theo_Tables'
    full_path = os.path.join(current_path, table)
    which_files = glob(f"{full_path}/*{file_key}*{model}*")
    if len(which_files) == 1:
        data = pd.read_table(which_files[0], comment='#', delim_whitespace=True, header=None)
        data.columns = ['Mass', 'C', 'xs']
        MT = data['Mass']
        xs = data['xs']
        if np.min(MT) <= mT <= np.max(MT):
            linear_interp = interpolate.interp1d(MT, xs)
            return linear_interp(mT)
        else:
            return -1
    else:
        MT, k_or_w, xsec = read_table(which_files)
        if np.min(MT) <= mT <= np.max(MT) and np.min(k_or_w) <= kT_or_wr <= np.max(k_or_w):
            linear_interp = interpolate.LinearNDInterpolator(list(zip(MT, k_or_w)), xsec)
            return linear_interp(mT, kT_or_wr)
        else:
            return -1


def linear1d_interp(x, y, x_extended):
    interp = interpolate.interp1d(x, y, "linear")
    return interp(x_extended)


def create_2d_interpolator(x_array, y_array, interpolated, indexes):
    appended_x = []
    appended_y = []
    interp = []

    for i, y in zip(indexes, y_array):
        min_val = np.min(x_array[i])
        max_val = np.max(x_array[i])
        x_extended = np.linspace(min_val, max_val, 100)
        appended_x.append(x_extended)
        appended_y.append(y * np.ones_like(x_extended))
        interp_1d = linear1d_interp(x_array[i], interpolated[i], x_extended)
        interp.append(interp_1d)

    interp = np.array(interp)
    appended_y = np.array(appended_y)
    appended_x = np.array(appended_x)

    return interpolate.LinearNDInterpolator(list(zip(appended_x.flatten(), appended_y.flatten())), interp.flatten())


def interpolate2d(indexes, kappa, width_ratio, m_expt, m_theo, obs_exp, width_ratio_array, coupling_array):
    if coupling_array is None:
        if width_ratio >= 0.01: #0.05
            interp = create_2d_interpolator(m_expt, width_ratio_array, obs_exp, indexes)
            return interp(m_theo, width_ratio)
        else:
            expected_or_observed = interpolate.interp1d(m_expt[indexes[0]], obs_exp[indexes[0]], 'linear')
            denominator = expected_or_observed(m_theo)  # mB
            return denominator
    else:
        interp = create_2d_interpolator(m_expt, coupling_array, obs_exp, indexes)
        return interp(m_theo, kappa)
