
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

