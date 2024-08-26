import os
from scipy import interpolate
import numpy as np
from glob import glob


def interpolate_xs(MT_exp, mT_theo, xs_theo):
    if np.min(MT_exp) <= mT_theo <= np.max(MT_exp):
        xs_QQ = interpolate.interp1d(MT_exp, xs_theo, 'linear')
        return xs_QQ(mT_theo)
    else:
        return -1


def get_xs_from_tables(path, mT, file_name):
    try:
        table = np.loadtxt(path)
        MT = table[:, 0]
        xs_pp_QQ = table[:, 1]
        return interpolate_xs(MT, mT, xs_pp_QQ)
    except FileNotFoundError:
        print(f"File '{file_name}' not found at path '{path}'")


def get_theo_xs_from_tables(mT, filename, vlq='T'):
    current_path = os.getcwd()
    path_to_table = 'data/' + vlq + 'data/Theo_Tables/' + str(filename)
    full_path = os.path.join(current_path, path_to_table)
    return get_xs_from_tables(full_path, mT, filename)


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
    "must be revisited and combined with interpolate 2d"
    current_path = os.getcwd()
    table = 'data/' + vlq + 'data/Theo_Tables'
    full_path = os.path.join(current_path, table)
    which_files = glob(f"{full_path}/*{file_key}*{model}*")

    MT, k_or_w, xsec = read_table(which_files)
    if np.min(MT) <= mT <= np.max(MT):
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


def interpolate2d(indexes, kappa, width_ratio, m_expt, m_theo, obs_exp, width_ratio_array,
                  coupling_array):
    if coupling_array is None:
        min_wr = min(width_ratio_array)
        if min_wr == 0.05:
            if width_ratio >= 0.05:
                interp = create_2d_interpolator(m_expt, width_ratio_array, obs_exp, indexes)
                return interp(m_theo, width_ratio)
            else:
                expected_or_observed = interpolate.interp1d(m_expt[indexes[0]], obs_exp[indexes[0]], 'linear')
                denominator = expected_or_observed(m_theo)
                return denominator
        elif min_wr == 0.01:
            if width_ratio >= 0.01:
                interp = create_2d_interpolator(m_expt, width_ratio_array, obs_exp, indexes)
                return interp(m_theo, width_ratio)
            else:
                return -1
    else:
        interp = create_2d_interpolator(m_expt, coupling_array, obs_exp, indexes)
        return interp(m_theo, kappa)


def linear_interp2d(mass_arr, width_or_kappa_arr, cs_arr):
    wk = []
    length = int(len(mass_arr) / len(width_or_kappa_arr))
    for i, wk_value in enumerate(width_or_kappa_arr):
        w_k = wk_value * np.ones(len(mass_arr[:length]))
        wk.append(w_k)
    wk = np.array(wk)
    wk_flat = wk.flatten()

    interp = interpolate.LinearNDInterpolator(list(zip(mass_arr, wk_flat)), cs_arr)
    return interp
