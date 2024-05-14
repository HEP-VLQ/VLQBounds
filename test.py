from output import Result
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
import random as rd
from model import check_mass_range
from pyTop import *

#with open("data/coupling_results_2channels.txt","w") as f:
  #f.write("mass s_L res ratio channel\n")

s_l = np.linspace(0.01,1,500)

#mass = np.linspace(1000,2200,500)

cs = np.linspace(10,0.01,500)
'''
with open("data/kappa_test_5.txt","w") as f:
 for k in kappa:
  for m, c in zip(mass,cs):   
   s = Singlet(m,-1,k*c,-1) # pp -> Tbq -> bWbq
   s.set_width_mass_ratio(0.05)
   s.set_couplings(-1,-1,k,0.2)
   T = TheoryCalc(s)
   T.find_limit()
   print(f"The mass: {m}")
   print(T)
   f.write(f"{s.mv()} {k} {k*c} {T.allowed} {T.obsratio} {T.channel}\n")
   '''
''''
with open("k_T.dat","w") as f:
    #kappa = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1]
    #f.write("mass s_L allowed obs_ratio channel label\n")
    for i in range(200000):
        mass = rd.uniform(400,2300)
        kappa = rd.uniform(0,2)
        #kap = rd.choice(kappa)
        cs = rd.uniform(0.01,100)
        s = Singlet(mass,cs,-1,-1)
        s.set_width_mass_ratio(0.1)
        s.set_couplings(-1,-1,-1,-1)
        T = TheoryCalc(s)
        T.find_limit()
        print("---------------------------")
        print("mass: ",mass)
        #print("kappa:",kap)
        print(T)
        j = T.channel
        f.write(f"{mass} {T.allowed} {T.obsratio} {T.channel} {T.label[j]}\n")
 '''
'''for i in range(1000000):
   M_T = rd.uniform(600,2000)
   s_L = rd.uniform(0,1)
   s = Singlet(M_T,0.1,0.2,-1)
   s.set_width_mass_ratio(0.3)
   s.set_couplings(0,s_L,0)
   T = TheoryCalc(s)
   T.find_limit()
   print(T)'''
  # f.write(f"{s.MT()} {s_L} {T.allowed} {T.obsratio} {T.channel}\n")

'''
for i in range(10000):
   M_T = rd.uniform(600,2000)
   s_L = rd.uniform(0,1)
   d = Doublet(M_T,0.1,0.2,0.9)
   d.set_width_mass_ratio(0.3)
   d.set_couplings(0,s_L,0)
   T = TheoryCalc(d)
   T.find_limit()
   print(T)
'''
'''
for i in range(10000):
   M_T = rd.uniform(600,2000)
   s_L = rd.uniform(0,1)
   p = PureDecay(M_T,0.1,1,-1,1,0,0)
   T = TheoryCalc(p)
   T.find_limit()
   print(T)'''

'''if __name__ == '__main__':
  s= Singlet(1100,0.9,1,1) 
  s.set_couplings(0,0.1,0)
  theo = TheoryCalc(s)
  theo.find_singlet_limit()
  print(theo)
  '''
'''
wb = []
zt = []
ht = []
for m in range(300, 1000, 1):
    s = Singlet(m, 10, 10, 10)
    s.set_couplings(0.1,0.1)
    br_wb = s.br_vbw()
    br_zt = s.br_vzt()
    br_ht = s.br_vht()
    wb.append(br_wb)
    zt.append(br_zt)
    ht.append(br_ht)

mass = np.arange(300,1000,1)
plt.plot(mass,wb, color = 'green')
plt.plot(mass,zt, color = 'yellow')
plt.plot(mass,ht)
plt.show()
'''

'''
wb = []
zt = []
ht = []

cross = [1000,200,90,30,9,2,0.8,0.2]
mass = [600,800,1000,1200,1400,1600,1800,2000]
pair_prod = interp1d(mass, cross, 'linear')


with open("data/file.dat", "w") as f:
    for m in range(600, 2000, 10):
        sin_l = rd.choice(s_l)
        s = Singlet(m, pair_prod(m) / 1000, -1, -1)
        s.set_couplings(sin_l, -1)
        T = TheoryCalc(s)
        print(T.key)
       # T.initialize_tables_cms_and_atlas()
        T.check_channel()
        #T.find_limit()
        print("----------------------------------")
        print(m)
        print(sin_l)
        print(pair_prod(m) / 1000)
        print(T)
        f.write(f"{s.mv()} {sin_l} {T.allowed_or_excluded} {T.model_observed_ratio}\n")

#T.all_processes()

mass = np.arange(300,1000,1)
plt.plot(mass,wb, color = 'red')
plt.plot(mass,zt, color = 'gray')
plt.plot(mass,ht,color = 'brown')
plt.show()
'''
'''
s = Singlet()
pt = PyTop(s)
pt.filling_channels_data()
cross = [1000,200,90,30,9,2,0.8,0.2]
mass = [600,800,1000,1200,1400,1600,1800,2000]
pair_prod = interp1d(mass, cross, 'linear')
sin_l = np.linspace(0,1,2000 - 600 + 1)
with open("data/sin_l_test.dat", "w") as f:
    f.write("mass sin_left result observed_ratio\n")
    for i in range(50):
        for m in range(600, 2000, 1):
            s_l = rd.choice(sin_l)
            print("----------------------------------")
            print(f"mass: {m}")
            print(f"sin_left = {s_l}")
            pt.check_singlet_limit(m, 10, 10, 10,s_l)
            f.write(f"{m} {s_l} {pt.allowed_or_excluded} {pt.model_observed_ratio}\n")
'''
'''
d = Doublet()
pt = PyTop(d)
pt.filling_channels_data()

sin_l = np.linspace(0,0.4,100)
sin_r = np.linspace(0,1,100)
mass = np.linspace(1000,2400,100)
#with open("data/kappa_doublet.dat", "w") as f:
#    f.write("m k res ratio channel r\n")
for i in range(2):
    m = rd.choice(mass)
    s_l = rd.choice(sin_l)
    s_r = rd.choice(sin_r)
    if s_l == 0 or s_r == 0:
        continue
    print("-----------------")
    print(f"mass: {m}")
    print(f"sin_left: {s_l}")
    pt.check_doublet_limit_with_TB_doublet(m, 10, 10, s_l, 0.23, 0.1)
        #f.write(f"{m} {pt.m.universal_coupling()} {pt.allowed_or_excluded} {pt.model_observed_ratio} {pt.channel} {pt.m.get_width_mass_ratio_from_zt()}\n")
'''
'''
s = Singlet()
pt = PyTop(s)
pt.filling_couplings_data()

sin_left = np.linspace(0, 1, 500)
mass = np.linspace(1000, 2400, 500)
with open("data/coupling_limit_from_class.dat", "w") as f:
    f.write("mass sin_l res ratio channel width\n")
    for i in range(60000):
        m = rd.choice(mass)
        s_l = rd.choice(sin_left)
        if s_l == 0:
            continue
        print("---------------")
        print(f"mass: {m}")
        print(f"sin_left: {s_l}")
        pt.check_coupling_limit(m, -1, -1, -1, s_l,-1)
        f.write(f"{m} {pt.m.universal_coupling()} {pt.allowed_or_excluded} {pt.model_observed_ratio} {pt.channel} {pt.m.get_width_mass_ratio_from_wb()}\n")
'''
'''
d = Doublet()
pt = PyTop(d)
pt.filling_couplings_data()

sin_left = np.linspace(0, 1, 500)
mass = np.linspace(1000, 2400, 500)
with open("data/coupling_limit_from_class_doublet.dat", "w") as f:
    f.write("mass sin_l res ratio channel width\n")
    for i in range(60000):
        m = rd.choice(mass)
        s_l = rd.choice(sin_left)
        if s_l == 0:
            continue
        print("---------------")
        print(f"mass: {m}")
        print(f"sin_left: {s_l}")
        pt.check_coupling_limit(m, -1, -1, -1, s_l)
        f.write(f"{m} {pt.m.universal_coupling()} {pt.allowed_or_excluded} {pt.model_observed_ratio} {pt.channel} {pt.m.get_width_mass_ratio_from_wb()}\n")
'''
p = PureDecay()

pt = PyTop(p)
pt.filling_channels_data()
print(pt.file_name)

s = Singlet()

pt = PyTop(s)
pt.filling_channels_data()
print('2209.07327_CMS_f9a_pp_TTbar_Singlet.txt' in pt.file_name)

d = Doublet()

pt = PyTop(d)
pt.filling_channels_data()
print(pt.file_name)







