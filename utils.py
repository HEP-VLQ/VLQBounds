import numpy as np
import os


def r_x(m1, m2): return m1/m2


def lambda_func(x, y, z):
    lamda = x ** 4 + y ** 4 + z ** 4 - 2 * x ** 2 * y ** 2 - 2 * x ** 2 * z ** 2 - 2 * y ** 2 * z ** 2
    return lamda


def check_single_prod_cs(cs):
    if cs is not None:
        if cs < 0:
            raise ValueError("Invalid single-production cross-section value. It must be positive.")


def check_pair_prod_cs(cs):
    if cs is not None:
        if cs < 0:
            raise ValueError("Invalid pair-production cross section value. It must be positive.")


def check_sin(s):
    if s != 0:
        if s < -1 or s > 1:
            raise ValueError("Invalid sin value. It must be in the the range [-1,1]")
    elif s == 0:
        raise ValueError("Invalid sin value. It must not equal 0")


def load_data_from_files(file_name, number_of_files, mass, expected, observed, atlas_cms_tevatron):
    current_path = os.getcwd()
    for i in range(number_of_files):
        if atlas_cms_tevatron[i] == 'ATLAS':
            file_path = os.path.join(current_path, 'ATLAS_Tables', file_name[i])
        else:
            file_path = os.path.join(current_path, 'CMS_Tables', file_name[i])

        try:
            data = np.loadtxt(file_path)
            mass[i] = data[:, 0]
            observed[i] = data[:, 1]
            expected[i] = data[:, 2]
        except FileNotFoundError:
            print(f"File '{file_name[i]}' not found at path '{file_path}'")

