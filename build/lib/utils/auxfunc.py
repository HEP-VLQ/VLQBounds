import numpy as np
import os
import pandas as pd
from vlqBounds import constants as c


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

    if not isinstance(cross_section_value, (int, float, np.ndarray)):
        raise TypeError(f"The cross-section of the process {process} must be a numeric type.")

    if cross_section_value < 0:
        raise ValueError(f"The cross-section of the process {process}  must be non-negative.")


def check_sin(s):
    if s != 0:
        if s < -1 or s > 1.0:
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


def coupling_data_loading(file_name, number_of_files, mass, expected, observed, atlas_cms, vlq='T'):
    current_path = os.getcwd()
    for i in range(number_of_files):
        if atlas_cms[i] == 'ATLAS':
            file_path = os.path.join(current_path, 'data/' + vlq + 'data/ATLAS_Tables', file_name[i])
        else:
            file_path = os.path.join(current_path, 'data/' + vlq + 'data/CMS_Tables', file_name[i])

        try:
            data = pd.read_table(file_path, comment='#', delim_whitespace=True, header=None)
            cols = data.shape[1]

            if cols == 6:
                data.columns = ["MT_of_obs", "MT_of_exp", "obs(lower)", "obs(upper)", "exp(lower)", "exp(upper)"]
                mass[0][i] = data["MT_of_obs"].dropna().to_numpy()
                mass[1][i] = data["MT_of_exp"].dropna().to_numpy()
                observed[0][i] = data["obs(lower)"].dropna().to_numpy()
                observed[1][i] = data["obs(upper)"].dropna().to_numpy()
                expected[0][i] = data["exp(lower)"].dropna().to_numpy()
                expected[1][i] = data["exp(upper)"].dropna().to_numpy()
            elif cols == 5:
                data.columns = ["MT", "obs(lower)", "obs(upper)", "exp(lower)", "exp(upper)"]
                mass[0][i] = data["MT"].dropna().to_numpy()
                mass[1][i] = mass[0][i]
                observed[0][i] = data["obs(lower)"].dropna().to_numpy()
                observed[1][i] = data["obs(upper)"].dropna().to_numpy()
                expected[0][i] = data["exp(lower)"].dropna().to_numpy()
                expected[1][i] = data["exp(upper)"].dropna().to_numpy()
            elif cols == 4:
                data.columns = ["MT_of_obs", "MT_of_exp", "obs", "exp"]
                mass[0][i] = data["MT_of_obs"].dropna().to_numpy()
                mass[1][i] = data["MT_of_exp"].dropna().to_numpy()
                observed[0][i] = data["obs"].dropna().to_numpy()
                observed[1][i] = observed[0][i]
                expected[0][i] = data["exp"].dropna().to_numpy()
                expected[1][i] = expected[0][i]
            elif cols == 3:
                data.columns = ["MT", "obs", "exp"]
                mass[0][i] = data["MT"].dropna().to_numpy()
                mass[1][i] = mass[0][i]
                observed[0][i] = data["obs"].dropna().to_numpy()
                observed[1][i] = observed[0][i]
                expected[0][i] = data["exp"].dropna().to_numpy()
                expected[1][i] = expected[0][i]
            else:
                raise Exception("Error, number of columns is not in the range [3,6]")
        except FileNotFoundError:
            print(f"File '{file_name[i]}' not found at path '{file_path}'")


def df_making(df, **kwargs):
    data = pd.DataFrame(kwargs, index=[0])
    df = pd.concat([df, data], ignore_index=True)
    return df


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


def calculate_width(constant: float, mQ_theo: float, m_A: float, coupling: list, m_q: float) -> float:
    c1, c2 = coupling
    width = (constant * mQ_theo / (m_A ** 2) * np.sqrt(lambda_func(mQ_theo, m_q, m_A))
             * (c1 + c2) ** 2 * ((1 + r_x(m_A, mQ_theo) ** 2 - 2 * r_x(m_q, mQ_theo) ** 2
                                 - 2 * r_x(m_A, mQ_theo) ** 4 + r_x(m_q, mQ_theo) ** 4
                                 + r_x(m_q, mQ_theo) ** 2 * r_x(m_A, mQ_theo) ** 2)
                                 - 12 * r_x(m_A, mQ_theo) ** 2 * r_x(m_q, mQ_theo) * c1 * c2))

    return width


def calculate_width_to_higgs_from_k(constant: float, mQ_theo: float, coupling: float, m_q: float) -> float:
    width = (constant * mQ_theo / (c.MW ** 2) * np.sqrt(lambda_func(mQ_theo, m_q, c.Mh))
             * coupling ** 2 * (1 + r_x(m_q, mQ_theo) ** 2 - r_x(c.Mh, mQ_theo) ** 2))

    return width


def calculate_width_to_higgs_from_mixing(constant: float, mQ_theo: float, coupling: float, m_q: float) -> float:
    width = (constant * mQ_theo / (c.MW ** 2) * np.sqrt(lambda_func(mQ_theo, c.Mt, c.Mh))
             * coupling ** 2 * (1 + 6 * r_x(m_q, mQ_theo) ** 2 - r_x(c.Mh, mQ_theo) ** 2 + r_x(m_q, mQ_theo) ** 4
                                - r_x(m_q, mQ_theo) ** 2 * r_x(c.Mh, mQ_theo) ** 2))

    return width


def is_array_full_of_none(array):
    return all(element is None for element in array)


def which_equivalence(a_string):
    if 'r' in a_string:
        which_letter = 'r'
    else:
        which_letter = 'k'
    if which_letter in a_string:
        if '==' in a_string:
            equal_array = a_string.split('==')
            values_from_string = [float(st) for st in equal_array if st != which_letter]
            from_equal = True
            return values_from_string, from_equal
        elif '<=' in a_string:
            leq_array = a_string.split('<=')
            values_from_string = [float(st) for st in leq_array if st != which_letter]
            from_equal = False
            return values_from_string, from_equal
