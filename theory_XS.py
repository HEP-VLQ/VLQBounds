import os
from scipy import interpolate
import numpy as np
from glob import glob


def interpolate_xs(MT_exp: list, mT_theo: float, xs_theo: list):
    if np.min(MT_exp) <= mT_theo <= np.max(MT_exp):
        xs_QQ = interpolate.interp1d(MT_exp, xs_theo, 'linear')
        return xs_QQ(mT_theo)
    else:
        return -1


def get_xs_from_tables(path: str, mQ: float, file_name: str):
    try:
        table = np.loadtxt(path)
        MQ = table[:, 0]
        xs_pp_QQ = table[:, 1]
        return interpolate_xs(MQ, mQ, xs_pp_QQ)
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


def get_data_from_files(file_key, model, vlq='T'):
    current_path = os.getcwd()
    table = 'data/' + vlq + 'data/Theo_Tables'
    full_path = os.path.join(current_path, table)
    which_files = glob(f"{full_path}/*{file_key}*{model}*")
    X_arr, Y_arr, Z_arr = read_table(which_files)
    return X_arr, Y_arr, Z_arr


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


def interpolate2d(expt_input: tuple, theo_input: tuple, case='expt'):
    if case == 'expt':
        (indexes, mass_arr, relative_width_arr, coupling_strength_arr, obs_or_exp_arr,
         m_theo_value, relative_width_value, coupling_strength_value) = expt_input
        if coupling_strength_arr is None:
            if min(relative_width_arr) == 0.05:
                if relative_width_value >= 0.05:
                    interp = create_2d_interpolator(mass_arr, relative_width_arr, obs_or_exp_arr, indexes)
                    return interp(m_theo_value, relative_width_value)
                else:
                    expected_or_observed = interpolate.interp1d(mass_arr[indexes[0]],
                                                                obs_or_exp_arr[indexes[0]],
                                                                'linear')
                    denominator = expected_or_observed(m_theo_value)
                    return denominator
            elif min(relative_width_arr) == 0.01:
                if relative_width_value >= 0.01:
                    interp = create_2d_interpolator(mass_arr, relative_width_arr, obs_or_exp_arr, indexes)
                    return interp(m_theo_value, relative_width_value)
                else:
                    return -1
        else:
            interp = create_2d_interpolator(mass_arr, coupling_strength_arr, obs_or_exp_arr, indexes)
            return interp(m_theo_value, coupling_strength_value)
    else:
        print("hi")
        (mass_arr, relative_width_arr, coupling_strength_arr, xs_theo_arr,
         m_theo_value, relative_width_value, coupling_strength_value) = theo_input
        if coupling_strength_arr is None:
            print("hi")
            if min(relative_width_arr) == 0.05:
                if relative_width_value >= 0.05:
                    interp2d = interpolate.LinearNDInterpolator(list(zip(mass_arr, relative_width_arr)), xs_theo_arr)
                    return interp2d(m_theo_value, relative_width_value)
                else:
                    filtering_005_xs = relative_width_arr == 0.05
                    expected_or_observed = interpolate.interp1d(mass_arr[filtering_005_xs],
                                                                xs_theo_arr[filtering_005_xs],
                                                                'linear')
                    return expected_or_observed(m_theo_value)
            elif min(relative_width_arr) == 0.01:
                if relative_width_value >= 0.01:
                    interp2d = interpolate.LinearNDInterpolator(list(zip(mass_arr, relative_width_arr)), xs_theo_arr)
                    return interp2d(m_theo_value, relative_width_value)
                else:
                    return -1

        else:
            interp2d = interpolate.LinearNDInterpolator(list(zip(mass_arr, coupling_strength_arr)), xs_theo_arr)
            return interp2d(m_theo_value, coupling_strength_value)


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
