import numpy
import numpy as np
import os
from glob import glob
import pandas as pd
from scipy import interpolate


def r_x(m1, m2): return m1/m2


def obs_exp_ratio_calc(theo, obs, exp):
    obs_ratio = theo / obs
    exp_ratio = theo / exp
    return obs_ratio, exp_ratio


def lambda_func(x, y, z):
    lamda = x ** 4 + y ** 4 + z ** 4 - 2 * x ** 2 * y ** 2 - 2 * x ** 2 * z ** 2 - 2 * y ** 2 * z ** 2
    return lamda


def validate_cross_section_value(cross_section_value, process):
    if cross_section_value is None:
        raise ValueError(f"The cross-section of the {process} cannot be None.")

    if not isinstance(cross_section_value, (int, float, numpy.ndarray)):
        raise TypeError(f"The cross-section of the process {process} must be a numeric type.")

    if cross_section_value < 0:
        raise ValueError(f"The cross-section of the process {process}  must be non-negative.")


def check_sin(s):
    if s != 0:
        if s < -1 or s > 1:
            raise ValueError("Invalid sin value. It must be in the the range [-1,1]")
    elif s == 0:
        raise ValueError("Invalid sin value. It must not equal 0")


def load_data_from_files(file_name, number_of_files, mass, expected, observed, atlas_cms, vlq='T'):
    current_path = os.getcwd()
    for i in range(number_of_files):
        if atlas_cms[i] == 'ATLAS':
            file_path = os.path.join(current_path, 'data/' + vlq + 'data/ATLAS_Tables', file_name[i])
        else:
            file_path = os.path.join(current_path, 'data/' + vlq + 'data/CMS_Tables', file_name[i])

        try:
            data = np.loadtxt(file_path)
            mass[i] = data[:, 0]
            observed[i] = data[:, 1]
            expected[i] = data[:, 2]
        except FileNotFoundError:
            print(f"File '{file_name[i]}' not found at path '{file_path}'")


def coupling_data_loading(file_name, number_of_files, mass, expected, observed, atlas_cms, model, vlq='T'):
    current_path = os.getcwd()
    for i in range(number_of_files):
        if atlas_cms[i] == 'ATLAS':
            file_path = os.path.join(current_path, 'data/' + vlq + 'data/ATLAS_Tables', file_name[i])
        else:
            file_path = os.path.join(current_path, 'data/' + vlq + 'data/CMS_Tables', file_name[i])

        if vlq == 'T':
            try:
                data = pd.read_table(file_path, comment='#', delim_whitespace=True, header=None)
                if model == 'Singlet':
                    two_masses_index = [2, 3, 6, 8, 9, 10, 12]
                    if i in two_masses_index:
                        if i == 2:
                            data.columns = ["MT_of_obs", "MT_of_exp", "obs(lower)", "obs(upper)", "exp(lower)",
                                            "exp(upper)"]
                            mass[0][i] = data["MT_of_obs"]
                            mass[1][i] = data["MT_of_exp"]
                            observed[0][i] = data["obs(lower)"]
                            observed[1][i] = data["obs(upper)"]
                            expected[0][i] = data["exp(lower)"]
                            expected[1][i] = data["exp(upper)"]
                        elif i == 3:
                            data.columns = ["MT", "obs(lower)", "obs(upper)", "exp(lower)",
                                            "exp(upper)"]
                            mass[0][i] = data["MT"]
                            mass[1][i] = mass[0][i]
                            observed[0][i] = data["obs(lower)"]
                            observed[1][i] = data["obs(upper)"]
                            expected[0][i] = data["exp(lower)"]
                            expected[1][i] = data["exp(upper)"]
                        else:
                            data.columns = ["MT_of_obs", "MT_of_exp", "obs", "exp"]
                            mass[0][i] = data["MT_of_obs"].dropna().to_numpy()
                            mass[1][i] = data["MT_of_exp"].dropna().to_numpy()
                            observed[0][i] = data["obs"].dropna().to_numpy()
                            observed[1][i] = observed[0][i]
                            expected[0][i] = data["exp"].dropna().to_numpy()
                            expected[1][i] = expected[0][i]
                    else:
                        data.columns = ["MT", "obs", "exp"]
                        mass[0][i] = data["MT"]
                        mass[1][i] = mass[0][i]
                        observed[0][i] = data["obs"]
                        observed[1][i] = observed[0][i]
                        expected[0][i] = data["exp"]
                        expected[1][i] = observed[0][i]
                else:
                    data.columns = ["MT_of_obs", "MT_of_exp", "obs", "exp"]
                    mass[0][i] = data["MT_of_obs"].dropna().to_numpy()
                    mass[1][i] = data["MT_of_exp"].dropna().to_numpy()
                    observed[0][i] = data["obs"].dropna().to_numpy()
                    observed[1][i] = observed[0][i]
                    expected[0][i] = data["exp"].dropna().to_numpy()
                    expected[1][i] = expected[0][i]
            except FileNotFoundError:
                print(f"File '{file_name[i]}' not found at path '{file_path}'")
        else:
            try:
                data = pd.read_table(file_path, comment='#', delim_whitespace=True, header=None)
                if model == 'Singlet':
                    if i in range(1, 6):
                        data.columns = ["MT", "obs", "exp"]
                        mass[0][i] = data["MT"].dropna().to_numpy()
                        mass[1][i] = mass[0][i]
                        observed[0][i] = data["obs"].dropna().to_numpy()
                        observed[1][i] = observed[0][i]
                        expected[0][i] = data["exp"]
                        expected[1][i] = expected[0][i].dropna().to_numpy()
                    else:
                        data.columns = ["MT_of_obs", "MT_of_exp", "obs", "exp"]
                        mass[0][i] = data["MT_of_obs"].dropna().to_numpy()
                        mass[1][i] = data["MT_of_exp"].dropna().to_numpy()
                        observed[0][i] = data["obs"].dropna().to_numpy()
                        observed[1][i] = observed[0][i]
                        expected[0][i] = data["exp"].dropna().to_numpy()
                        expected[1][i] = expected[0][i]
                else:
                    data.columns = ["MT", "obs", "exp"]
                    mass[0][i] = data["MT"].dropna().to_numpy()
                    mass[1][i] = mass[0][i]
                    observed[0][i] = data["obs"].dropna().to_numpy()
                    observed[1][i] = observed[0][i]
                    expected[0][i] = data["exp"]
                    expected[1][i] = expected[0][i].dropna().to_numpy()
            except FileNotFoundError:
                print(f"File '{file_name[i]}' not found at path '{file_path}'")


def df_making(df, **kwargs):
    data = pd.DataFrame(kwargs, index=[0])
    df = pd.concat([df, data], ignore_index=True)
    return df


def linear_interp2d(mass_arr, width_or_kappa_arr, cs_arr):
    wk = []
    length = int(len(mass_arr) / len(width_or_kappa_arr))
    mass = []
    for i in range(len(width_or_kappa_arr)):
        w_k = width_or_kappa_arr[i] * np.ones(len(mass_arr[:length]))
        wk.append(w_k)
    wk = np.array(wk)
    wk_flat = wk.flatten()

    interp = interpolate.LinearNDInterpolator(list(zip(mass_arr, wk_flat)), cs_arr)
    return interp


def linear1d_interp(x, y, x_extended):
    interp = interpolate.interp1d(x, y, "linear")
    return interp(x_extended)


def interpolate2d(indexes, kappa, width_ratio, m_expt, m_theo, obs_exp, width_ratio_array, coupling_array):
    if coupling_array is None:
        if width_ratio >= 0.05:
            interp = create_2d_interpolator(m_expt, width_ratio_array, obs_exp, indexes)
            return interp(m_theo, width_ratio)
        else:
            expected_or_observed = interpolate.interp1d(m_expt[indexes[0]], obs_exp[indexes[0]], 'linear')
            denominator = expected_or_observed(m_theo)  # mB
            return denominator
    else:
        interp = create_2d_interpolator(m_expt, coupling_array, obs_exp, indexes)
        return interp(m_theo, kappa)


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


def xs_pp_QQ_theo(mT):
    current_path = os.getcwd()
    path_to_table = 'data/Tdata/Theo_Tables/pp_TT_pred_NNLO.dat'
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
        print(f"File 'pp_TT_pred_NNLO.dat' not found at path '{full_path}'")


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


def interp2d_xs_theo(file_key, model, mT, kT_or_wr):
    current_path = os.getcwd()
    table = 'data/Tdata/Theo_Tables'
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


def max_min_mass_from_width_files(mass, index_width_tables):
    mass_tables = []
    for i in index_width_tables:
        mass_tables.append(mass[i])
    maxi = float('-inf')
    mini = float('inf')
    for m_table in mass_tables:
        if max(m_table) > maxi:
            maxi = max(m_table)
        if min(m_table) < mini:
            mini = min(m_table)
    return maxi, mini


def biggest_ratio(coupling_ratio, xs_ratio):
    xs_bigger = False
    if coupling_ratio >= xs_ratio:
        return xs_bigger
    else:
        return not xs_bigger
