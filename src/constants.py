import pandas as pd
import math

Mt = 172.52
MW = 80.43
MZ = 91.1876
Mb = 4.18
Mh = 125.09
G = 0.653
PI = math.pi
C_W = MW / MZ
Cst1 = G ** 2 / (64 * PI)
Cst2 = G ** 2 / (128 * PI * C_W ** 2)
Cst3 = G ** 2 / (128 * PI)
v = 2 * MW / G
Threshold = 0.01

df = pd.DataFrame(columns=["mass", "mixing", "coupling", "predicted_xs", "observed_xs",
                           "expected_xs", "width_ratio", "result",
                           "channel",  "obs_ratio", "exp_ratio", "process",
                           "experiment", "luminosity", "energy",
                           "label", "model", "which_doublet"])

