from output import Result
from scipy import interpolate
import numpy as np
import random as rd
from model import check_mass_range
from pyTop import *
import matplotlib.pyplot as plt

#with open("data/coupling_results_2channels.txt","w") as f:
  #f.write("mass s_L res ratio channel\n")

s_l = np.linspace(0.01 ,1, 500)

#mass = np.linspace(1000,2200,500)

cs = np.linspace(10, 0.01, 500)
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
mass = np.linspace(600, 2000, 500)
with open("data/sin_l.dat", "w") as f:
    f.write("mass sin_l res ratio channel width\n")
    for i in range(300000):
        m = rd.choice(mass)
        s_l = rd.choice(sin_left)
        if s_l == 0:
            continue
        print("---------------")
        print("i = ", i)
        print(f"mass: {m}")
        print(f"sin_left: {s_l}")
        pt.check_coupling_limit(m, s_l)
        f.write(f"{m} {pt.m.universal_coupling()} {pt.allowed_or_excluded} {pt.model_observed_ratio} {pt.channel} {pt.m.get_width_mass_ratio()}\n")
'''

'''
s = Singlet()
pt = PyTop(s)
pt.filling_couplings_data()

sin_left = np.linspace(0, 1, 500)
mass = np.linspace(600, 2400, 500)
with open("data/coupling_limit_from_class_singlet.dat", "w") as f:
    f.write("mass sin_l res ratio channel width\n")
    for i in range(300000):
        m = rd.choice(mass)
        s_l = rd.choice(sin_left)
        if s_l == 0:
            continue
        print("---------------")
        print("i = ", i)
        print(f"mass: {m}")
        print(f"sin_left: {s_l}")
        pt.check_coupling_limit(m, s_l)
        f.write(f"{m} {pt.m.universal_coupling()} {pt.allowed_or_excluded} {pt.model_observed_ratio} {pt.channel} {pt.m.get_width_mass_ratio()}\n")
'''

'''
d = Doublet()
pt = PyTop(d)
pt.filling_couplings_data()

sin_left = np.linspace(0, 1, 500)
mass = np.linspace(1000, 2400, 500)
with open("data/coupling_limit_from_class_doublet.dat", "w") as f:
    f.write("mass sin_l res ratio channel width\n")
    for i in range(300000):
        m = rd.choice(mass)
        s_l = rd.choice(sin_left)
        if s_l == 0:
            continue
        print("---------------")
        print(f"mass: {m}")
        print(f"sin_left: {s_l}")
        pt.check_coupling_limit(m, s_l)
        f.write(f"{m} {pt.m.universal_coupling()} {pt.allowed_or_excluded} {pt.model_observed_ratio} {pt.channel} {pt.m.get_width_mass_ratio()}\n")

'''

'''
s = Singlet()

pt = PyTop(s)
pt.filling_channels_data()
pt.check_singlet_limit(800, 1, 1, 0.1, 0.23)
'''

'''
d = Doublet()
pt = PyTop(d)
pt.filling_channels_data()
pt.check_doublet_limit_with_TB_doublet(1000, 10, 1, 0.2, 0.1, 0.2)
pt.check_doublet_limit(1000, 0.9, 0.6, 0.2)
'''
'''
p = PureDecay()

pt = PyTop(p)

pt.filling_channels_data()

pt.check_pure_limit(600, 0.1, 0.2)
'''
'''
pair_prod = [455, 196, 90.3, 44, 22.4, 11.8, 6.39, 3.54, 2, 1.148, 0.666, 0.391]
mass = np.arange(700, 1900, 100)

mass_interp = np.linspace(700, 1800, 4000)


pair_prod_interp = interpolate.interp1d(mass, pair_prod, 'linear')

s = Singlet()
pt = PyTop(s)
pt.filling_channels_data()
with open("data/pair_prod.dat", "w") as f:
    f.write("mass s_l pair_prod ratio result channel\n")
    for s_l in np.linspace(0.0000001, 0.999, 40):
        for m, p in zip(mass_interp, pair_prod_interp(mass_interp)):
            print("m = ", m)
            print("pair_prod = ", p / 1000)
            pt.check_singlet_limit(m, p / 1000, -1, -1, s_l)
            print("------------------------------------------------")
            print("Singlet")
            f.write(f"{m} {s_l} {p / 1000} {pt.model_observed_ratio} {pt.allowed_or_excluded} {pt.channel}\n")


d = Doublet()
pt = PyTop(d)
pt.filling_channels_data()
with open("data/pair_prod_doublet.dat", "w") as f:
    f.write("mass s_r pair_prod ratio result channel\n")
    for s_r in np.linspace(0.0000001, 0.999, 40):
        for m, p in zip(mass_interp, pair_prod_interp(mass_interp)):
            print("m = ", m)
            print("pair_prod = ", p / 1000)
            pt.check_doublet_limit(m, p / 1000, -1, s_r)
            print("------------------------------------------------")
            f.write(f"{m} {s_r} {p / 1000} {pt.model_observed_ratio} {pt.allowed_or_excluded} {pt.channel}\n")

'''
'''
with open("data/branching_ratio_s.dat", "w") as f:
    f.write("mass br_wb br_zt br_ht s_l\n")
    for m in range(300, 3000, 1):
        s = Singlet(m, -1, -1, -1, 0.1)
        f.write(f"{s.mv_theo} {s.br_vbw()} {s.br_vzt()} {s.br_vht()} {s.sin_l}\n")
        print(f"{s.mv_theo} {s.br_vbw()} {s.br_vzt()} {s.br_vht()} {s.sin_l}")
with open("data/branching_ratio_d.dat", "w") as f:
    f.write("mass br_wb br_zt br_ht s_u_r s_d_r\n")
    for m in range(300, 3000, 1):
        d = Doublet(m, -1, -1, 0.1)
        d.set_sin_up_right(0.4)
        d.set_sin_down_right(0.1)
        f.write(f"{d.mv_theo} {d.br_vbw_tb_doublet()} {d.br_vzt_tb_doublet()} {d.br_vht_tb_doublet()} {d.get_sin_up_right()} {d.get_sin_up_right()}\n")

with open("data/branching_ratio_d_xt.dat", "w") as f:
    f.write("mass br_wb br_zt br_ht s_r\n")
    for m in range(300, 3000, 1):
        d = Doublet(m, -1, -1, 0.1)
        f.write(f"{d.mv_theo} {d.br_vbw()} {d.br_vzt()} {d.br_vht()} {d.sin_right()}\n")
'''

'''
data1 = np.loadtxt("data/220107045/2201.07045_ATLAS_fig8a_KT_01.txt")
mass1 = data1[:, 0]
cs_ht1 = data1[:, 1] / 1000
k_t1 = np.ones(len(mass1)) * 0.1

data2 = np.loadtxt("data/220107045/2201.07045_ATLAS_fig8b_KT_03.txt")
mass2 = data2[:, 0]
cs_ht2 = data2[:, 1] / 1000
k_t2 = np.ones(len(mass2)) * 0.3

data3 = np.loadtxt("data/220107045/2201.07045_ATLAS_fig8c_KT_05.txt")
mass3 = data3[:, 0]
cs_ht3 = data3[:, 1] / 1000
k_t3 = np.ones(len(mass3)) * 0.5


data4 = np.loadtxt("data/220107045/2201.07045_ATLAS_fig8d_KT_07.txt")
mass4 = data4[:, 0]
cs_ht4 = data4[:, 1] / 1000
k_t4 = np.ones(len(mass4)) * 0.7

data5 = np.loadtxt("data/220107045/2201.07045_ATLAS_fig8e_KT_09.txt")
mass5 = data5[:, 0]
cs_ht5 = data5[:, 1] / 1000
k_t5 = np.ones(len(mass5)) * 0.9


data6 = np.loadtxt("data/220107045/2201.07045_ATLAS_fig8f_KT_11.txt")
mass6 = data6[:, 0]
cs_ht6 = data6[:, 1] / 1000
k_t6 = np.ones(len(mass6)) * 1.1

mass = np.concatenate([mass1, mass2, mass3, mass4, mass5, mass6], axis=None)
cs_ht = np.concatenate([cs_ht1, cs_ht2, cs_ht3, cs_ht4, cs_ht5, cs_ht6], axis=None)
k_t = np.concatenate([k_t1, k_t2, k_t3, k_t4, k_t5, k_t6], axis=None)

print(cs_ht)

interp = interpolate.LinearNDInterpolator(list(zip(mass, k_t)), cs_ht)

mass = np.linspace(1000, 2300, 650)
k_t = np.linspace(0.1, 1.1, 300)

cs_vbq = cs_ht / 0.25

s = Singlet()
pt = PyTop(s)
pt.filling_channels_data()
with open("data/220107045/res.dat", "w") as f:
    f.write("mass k_t sing_prod ratio result channel label gamma arXiv luminosity\n")
    for k in k_t:
        for m in mass:
            print("m = ", m)
            print("kappa = ", k)
            pt.check_singlet_limit(m, -1, interp(m, k) / 0.25, 0, k)
            print("------------------------------------------------")
            print("Singlet")
            chan = pt.channel
            f.write(f"{m} {k} {interp(m,k)} {pt.model_observed_ratio} {pt.allowed_or_excluded} {chan} {pt.expt[chan]} {pt.m.get_width_mass_ratio()} {pt.label[chan]} {pt.luminosity[chan]}\n")
'''
'''
data1 = np.loadtxt("../../Downloads/2307.07584_ATLAS_Fig8b_K03_Doublet.txt")
m1 = data1[:, 0]
cs_k03 = data1[:, 1]
data2 = np.loadtxt("../../Downloads/2307.07584_ATLAS_Fig8d_K05_Doublet.txt")
m2 = data2[:, 0]
cs_k05 = data2[:, 1]
data3 = np.loadtxt("../../Downloads/2307.07584_ATLAS_Fig8f_K07_Doublet.txt")
m3 = data3[:, 0]
cs_k07 = data3[:, 1]



#cs_k03_1 = interpolate.interp1d(m1, cs_k03, kind = 'linear')
#cs_k05_1 = interpolate.interp1d(m2, cs_k05, kind = 'linear')
#cs_k07_1 = interpolate.interp1d(m3, cs_k07, kind = 'linear')


k_03 = 0.3 * np.ones(len(m1))
k_05 = 0.5 * np.ones(len(m2))
k_07 = 0.7 * np.ones(len(m3))

mass = np.concatenate([m1, m2, m3], axis=None)
cs_zt = np.concatenate([cs_k03, cs_k05, cs_k07], axis=None) / 0.5
k_t = np.concatenate([k_03, k_05, k_07], axis=None)


interp = interpolate.LinearNDInterpolator(list(zip(mass, k_t)), cs_zt)

mass = np.linspace(1000, 1700, 400)
k_t = np.linspace(0.3, 0.7, 300)

cs_vbq = cs_zt / 0.5

d = Doublet()
pt = PyTop(d)
pt.filling_channels_data()
with open("data/doub.dat", "w") as f:
    f.write("mass k_t sing_prod ratio result channel label gamma arXiv luminosity\n")
    for k in k_t:
        for m in mass:
            print("m = ", m)
            print("kappa = ", k)
            pt.check_doublet_limit(m, -1, interp(m, k), k)
            print("------------------------------------------------")
            print("gamma/m_T = ", pt.m.get_width_mass_ratio())
            print("Doublet")
            chan = pt.channel
            f.write(f"{m} {k} {interp(m,k)} {pt.model_observed_ratio} {pt.allowed_or_excluded} {chan} {pt.expt[chan]} {pt.m.get_width_mass_ratio()} {pt.label[chan]} {pt.luminosity[chan]}\n")
'''
'''
data1 = np.loadtxt("/home/mohamed/Downloads/2305.03401_ATLAS_Fig12a_pp_Tqt_Ht_Zt_doublet-k02_theo.txt")
m1 = data1[:, 0]
cs1 = data1[:, 1] / (1000 * 0.5)
data2 = np.loadtxt("/home/mohamed/Downloads/2305.03401_ATLAS_Fig12b_pp_Tqt_Ht_Zt_doublet-k04_theo.txt")
m2 = data2[:, 0]
cs2 = data2[:, 1] / (1000 * 0.5)
data3 = np.loadtxt("/home/mohamed/Downloads/2305.03401_ATLAS_Fig12c_pp_Tqt_Ht_Zt_doublet-k06_theo.txt")
m3 = data3[:, 0]
cs3 = data3[:, 1] / (1000 * 0.5)


k_02 = 0.2 * np.ones(len(m1))
k_04 = 0.4 * np.ones(len(m2))
k_06 = 0.6 * np.ones(len(m3))

mass = np.concatenate([m1, m2, m3], axis=None)
k_t = np.concatenate([k_02, k_04, k_06], axis=None)
cs_zt = np.concatenate([cs1, cs2, cs3], axis=None)

interp = interpolate.LinearNDInterpolator(list(zip(mass, k_t)), cs_zt)

mass = np.linspace(1000, 2100, 300)
k_t = np.linspace(0.2, 0.6, 200)

d = Doublet()
pt = PyTop(d)
pt.filling_channels_data()

with open("data/doub_tb_2.dat", "w") as f:
    f.write("mass k_t sing_prod ratio result channel label gamma arXiv luminosity\n")
    for k in k_t:
        for m in mass:
            print("m = ", m)
            print("kappa = ", k)
            pt.check_TB_doublet_limit(m, -1, interp(m, k), -1, k,-1)
            print(pt.m.universal_coupling())
            print(pt.m.get_width_mass_ratio())
            print("------------------------------------------------")
            print("Doublet")
            chan = pt.channel
            f.write(f"{m} {k} {interp(m,k)} {pt.model_observed_ratio} {pt.allowed_or_excluded} {chan} {pt.expt[chan]} {pt.m.get_width_mass_ratio()} {pt.label[chan]} {pt.luminosity[chan]}\n")
'''
'''
data1 = np.loadtxt("../../Downloads/2307.07584_ATLAS_Fig8b_K03_Doublet.txt")
m1 = data1[:,0]
cs_k03 = data1[:,1]
data2 = np.loadtxt("../../Downloads/2307.07584_ATLAS_Fig8d_K05_Doublet.txt")
m2 = data2[:,0]
cs_k05 = data2[:,1]
data3 = np.loadtxt("../../Downloads/2307.07584_ATLAS_Fig8f_K07_Doublet.txt")
m3 = data3[:,0]
cs_k07 = data3[:,1]


k_03 = 0.3 * np.ones(len(m1))
k_05 = 0.5 * np.ones(len(m2))
k_07 = 0.7 * np.ones(len(m3))

mass = np.concatenate([m1, m2, m3], axis=None)
cs_zt = np.concatenate([cs_k03, cs_k05, cs_k07], axis=None) / 0.5
k_t = np.concatenate([k_03, k_05, k_07], axis=None)

interp = interpolate.CloughTocher2DInterpolator(list(zip(mass, k_t)), cs_zt)

mass = np.linspace(1000, 1700, 200)
k_t = np.linspace(0.3, 0.7, 100)

cs_vbq = cs_zt / 0.5

d = Doublet()
pt = PyTop(d)
pt.filling_channels_data()

with open("data/doub_tb_2_0307.dat", "w") as f:
    f.write("mass k_t sing_prod ratio result channel label gamma arXiv limunosity\n")
    for k in k_t:
        for m in mass:
            print("m = ", m)
            print("kappa = ", k)
            pt.check_TB_doublet_limit(m, -1, interp(m, k), -1, k,-1)
            print(pt.m.universal_coupling())
            print(pt.m.get_width_mass_ratio())
            print("------------------------------------------------")
            print("Doublet")
            chan = pt.channel
            f.write(f"{m} {k} {interp(m,k)} {pt.model_observed_ratio} {pt.allowed_or_excluded} {chan} {pt.expt[chan]} {pt.m.get_width_mass_ratio()} {pt.label[chan]} {pt.luminosity[chan]}\n")
'''
'''
data = np.loadtxt('data/Tbq.txt')
mass = data[:, 0]
vbq_005 = data[:, 1]
vbq_01 = data[:, 2]
vbq_02 = data[:, 3]
vbq_03 = data[:, 4]

width_to_mass = 0.05 * np.ones(len(mass))
width_to_mass2 = 0.1 * np.ones(len(mass))
width_to_mass3 = 0.2 * np.ones(len(mass))
width_to_mass4 = 0.3 * np.ones(len(mass))

t1 = vbq_005
t2 = vbq_01
t3 = vbq_02
t4 = vbq_03

m1 = mass
m2 = mass
m3 = mass
m4 = mass

m = np.concatenate([m1, m2, m3, m4], axis=None)
t_tot = np.concatenate([t1, t2, t3, t4], axis=None)
w = np.concatenate([width_to_mass, width_to_mass2, width_to_mass3, width_to_mass4], axis=None)

interp = interpolate.LinearNDInterpolator(list(zip(m, w)), t_tot)

s = Singlet()
pt = PyTop(s)
pt.filling_channels_data()
for w in [0.05, 0.1, 0.2,0.3]:
        for m in np.linspace(600,1800,800) :
                pt.check_singlet_limit(m, -1, interp(m,w) / 0.25, -1, 0.1, w)
pt.df.to_csv("../../vbq.txt", sep='\t')
'''
'''
gamma = []
kappa = []
mass = []
d = Doublet()
pt = PyTop(d)
pt.filling_channels_data()
for m in np.linspace(1000, 2000, 100):
    pt.doublet_width_ratio_inputs(m, 0.1, 0.1, 0.2)
    pt.check_sm_plus_tb_doublet_limit()
    kappa.append(pt.m.universal_coupling())
    mass.append(m)

plt.scatter(mass,kappa)
plt.show()
'''
'''
pair_prod = [196, 44, 11.8, 3.54, 1.148, 0.391]


data = np.loadtxt('data/Tbq.txt')
mass = data[:, 0]
vbq_005 = data[:, 1]
vbq_01 = data[:, 2]
vbq_02 = data[:, 3]
vbq_03 = data[:, 4]

mass = np.delete(mass, 0)
vbq_005 = np.delete(vbq_005, 0)
vbq_01 = np.delete(vbq_01, 0)
vbq_02 = np.delete(vbq_02, 0)
vbq_03 = np.delete(vbq_03, 0)



gamma_05 = 0.05 * np.ones(len(mass))
gamma_01 = 0.1 * np.ones(len(mass))
gamma_02 = 0.2 * np.ones(len(mass))
gamma_03 = 0.3 * np.ones(len(mass))

gamma = np.concatenate([gamma_05, gamma_01, gamma_02, gamma_03], axis=None)
vbq = np.concatenate([vbq_005, vbq_01, vbq_02, vbq_03], axis=None)
mass = np.concatenate([mass]*4, axis=None)
pair_prod = np.tile(pair_prod, 4) / 1000

s = Singlet()
pt = PyTop(s)
pt.filling_channels_data()
for g,v,m in zip(gamma,vbq,mass):
    pt.singlet_width_ratio_inputs(m, -1, v, -1, g)
    pt.check_singlet_limit()
    print("mass:",m)
pt.df.to_csv("../../example.txt", sep='\t')
'''
'''
data1 = np.loadtxt("data/220107045/2201.07045_ATLAS_fig8a_KT_01.txt")
mass1 = data1[:, 0]
cs_ht1 = data1[:, 1] / 1000
k_t1 = np.ones(len(mass1)) * 0.1

data2 = np.loadtxt("data/220107045/2201.07045_ATLAS_fig8b_KT_03.txt")
mass2 = data2[:, 0]
cs_ht2 = data2[:, 1] / 1000
k_t2 = np.ones(len(mass2)) * 0.3

data3 = np.loadtxt("data/220107045/2201.07045_ATLAS_fig8c_KT_05.txt")
mass3 = data3[:, 0]
cs_ht3 = data3[:, 1] / 1000
k_t3 = np.ones(len(mass3)) * 0.5


data4 = np.loadtxt("data/220107045/2201.07045_ATLAS_fig8d_KT_07.txt")
mass4 = data4[:, 0]
cs_ht4 = data4[:, 1] / 1000
k_t4 = np.ones(len(mass4)) * 0.7

data5 = np.loadtxt("data/220107045/2201.07045_ATLAS_fig8e_KT_09.txt")
mass5 = data5[:, 0]
cs_ht5 = data5[:, 1] / 1000
k_t5 = np.ones(len(mass5)) * 0.9


data6 = np.loadtxt("data/220107045/2201.07045_ATLAS_fig8f_KT_11.txt")
mass6 = data6[:, 0]
cs_ht6 = data6[:, 1] / 1000
k_t6 = np.ones(len(mass6)) * 1.1

mass = np.concatenate([mass1, mass2, mass3, mass4, mass5, mass6], axis=None)
cs_ht = np.concatenate([cs_ht1, cs_ht2, cs_ht3, cs_ht4, cs_ht5, cs_ht6], axis=None)
k_t = np.concatenate([k_t1, k_t2, k_t3, k_t4, k_t5, k_t6], axis=None)

print(cs_ht)

interp = interpolate.LinearNDInterpolator(list(zip(mass, k_t)), cs_ht)

mass = np.linspace(1000, 2300, 200)
k_t = np.linspace(0.1, 1.1, 100)

cs_vbq = cs_ht / 0.25

s = Singlet()
pt = PyTop(s)
pt.filling_channels_data()
for k in k_t:
    for m in mass:
        print("m = ", m)
        print("kappa = ", k)
        pt.singlet_simplified_model_inputs(m, -1, interp(m, k) / 0.25, 0, k)
        pt.check_singlet_limit()
        print("------------------------------------------------")
        print("Singlet")
        chan = pt.channel
pt.df.to_csv("../../sing.txt", sep='\t')



data = np.loadtxt('data/Tbq.txt')
mass = data[:, 0]
vbq_005 = data[:, 1]
vbq_01 = data[:, 2]
vbq_02 = data[:, 3]
vbq_03 = data[:, 4]



m = np.linspace(600,1800,100)

interp_005 = interpolate.interp1d(mass,vbq_005,"linear")
interp_01 = interpolate.interp1d(mass,vbq_01,"linear")
interp_02 = interpolate.interp1d(mass,vbq_02,"linear")
interp_03 = interpolate.interp1d(mass,vbq_03,"linear")

vbq_005 = interp_005(m)
vbq_01 = interp_01(m)
vbq_02 = interp_02(m)
vbq_03 = interp_03(m)






gamma_05 = 0.05 * np.ones(len(m))
gamma_01 = 0.1 * np.ones(len(m))
gamma_02 = 0.2 * np.ones(len(m))
gamma_03 = 0.3 * np.ones(len(m))

gamma = np.concatenate([gamma_05, gamma_01, gamma_02, gamma_03], axis=None)
vbq = np.concatenate([vbq_005, vbq_01, vbq_02, vbq_03], axis=None)
mass2 = np.concatenate([m, m, m, m], axis=None)


vbq_final = interpolate.LinearNDInterpolator(list(zip(mass2, gamma)), vbq)


mass = np.linspace(600, 1800,200)
gamma = np.linspace(0.05, 0.3,100)





s = Singlet()
pt = PyTop(s)
pt.filling_channels_data()
for g in gamma:
    for m in mass:
        pt.singlet_width_ratio_inputs(m, -1, vbq_final(m, g) / 0.25, 0, g)
        pt.check_singlet_limit()
        print("mass:", m)
        print("gamma:", g)
        print("vbq:", vbq_final(m, g))
pt.df.to_csv("../../sing_with_width_input.txt", sep='\t')

data1 = np.loadtxt("../../Downloads/2307.07584_ATLAS_Fig8b_K03_Doublet.txt")
m1 = data1[:,0]
cs_k03 = data1[:,1]
data2 = np.loadtxt("../../Downloads/2307.07584_ATLAS_Fig8d_K05_Doublet.txt")
m2 = data2[:,0]
cs_k05 = data2[:,1]
data3 = np.loadtxt("../../Downloads/2307.07584_ATLAS_Fig8f_K07_Doublet.txt")
m3 = data3[:,0]
cs_k07 = data3[:,1]


k_03 = 0.3 * np.ones(len(m1))
k_05 = 0.5 * np.ones(len(m2))
k_07 = 0.7 * np.ones(len(m3))

mass = np.concatenate([m1, m2, m3], axis=None)
cs_zt = np.concatenate([cs_k03, cs_k05, cs_k07], axis=None) / 0.5
k_t = np.concatenate([k_03, k_05, k_07], axis=None)

interp = interpolate.LinearNDInterpolator(list(zip(mass, k_t)), cs_zt)

mass = np.linspace(1000, 1700, 200)
k_t = np.linspace(0.3, 0.7, 100)

cs_vbq = cs_zt / 0.5

d = Doublet()
pt = PyTop(d)
pt.filling_channels_data()

for k in k_t:
    for m in mass:
        print("m = ", m)
        print("kappa = ", k)
        pt.doublet_simplified_model_inputs(m, -1, interp(m, k), k)
        pt.check_sm_plus_tb_doublet_limit()
pt.df.to_csv("../../doublet_03_07.dat",sep='\t')
'''
'''
data = np.loadtxt('data/Ttq.txt')
mass = data[:, 0]
vtq_005 = data[:, 1]
vtq_01 = data[:, 2]
vtq_02 = data[:, 3]
vtq_03 = data[:, 4]



m = np.linspace(800, 1600, 100)

interp_005 = interpolate.interp1d(mass, vtq_005, "linear")
interp_01 = interpolate.interp1d(mass,vtq_01,"linear")
interp_02 = interpolate.interp1d(mass,vtq_02,"linear")
interp_03 = interpolate.interp1d(mass,vtq_03,"linear")

vtq_005 = interp_005(m)
vtq_01 = interp_01(m)
vtq_02 = interp_02(m)
vtq_03 = interp_03(m)






gamma_05 = 0.05 * np.ones(len(m))
gamma_01 = 0.1 * np.ones(len(m))
gamma_02 = 0.2 * np.ones(len(m))
gamma_03 = 0.3 * np.ones(len(m))

gamma = np.concatenate([gamma_05, gamma_01, gamma_02, gamma_03], axis=None)
vtq = np.concatenate([vtq_005, vtq_01, vtq_02, vtq_03], axis=None)
mass2 = np.concatenate([m]*4, axis=None)


vtq_final = interpolate.LinearNDInterpolator(list(zip(mass2, gamma)), vtq)


mass = np.linspace(800, 1600,200)
gamma = np.linspace(0.05, 0.3,100)

d = Doublet()
pt = PyTop(d)
pt.filling_channels_data()
for g in gamma:
    for m in mass:
        pt.doublet_width_ratio_inputs(m, -1, vtq_final(m, g) / 0.5, g)
        pt.check_sm_plus_tb_doublet_limit()
        print("mass:", m)
        print("gamma:", g)
        print("vbq:", vtq_final(m, g))
pt.df.to_csv("../../doublet_with_width_input.dat", sep='\t')
'''
# initializing and preparing the tables
#s = Singlet()
#pt = PyTop(s)
#pt.filling_channels_data()





#inputs = {
#    "mT": [800, 1000, 1200, 1400, 1600],
#    "cs_pp_TT": np.array([0.196, 0.04, 0.118, 0.00354, 0.00148]),
#    "cs_pp_Tbq": np.array([[], [], [], []]),
#    "cs_pp_Ttq": np.array([[], [], [], []]),
#    "k": [0.05, 0.1, 0.2, 0.3]
#}

#method performs the necessary calculations
#pt.singlet_simplified_inputs(**inputs)

#checking the bounds
#pt.check_singlet_limit()
'''
inputs = {
    "mT": 1000,
    "cs_pp_TT": 0.01,
    "cs_Tbq": 0.01,
    "cs_pp_Ztbq": 2,
    "cs_pp_Htbq": 2,
    "cs_pp_Zttq": 2,
    "k": 0.6
}
pt.singlet_simplified_inputs(**inputs)
pt.check_singlet_limit()

d = Doublet()
pt = PyTop(d)
pt.filling_channels_data()

inputs = {
    "mT": 1000,
    "cs_pp_TT": 0.01,
    "cs_Ttq": 0.01,
    "cs_pp_Zttq": 2,
    "cs_pp_Httq": 2,
    "k": 0.6
}
pt.doublet_simplified_inputs(**inputs)
pt.check_sm_plus_tb_doublet_limit()
'''

'''
data = np.loadtxt("data/Tbq.dat")
mT = data[:, 0]
Tbq_005 = data[:, 1] / 0.25
Tbq_01 = data[:, 2] / 0.25
Tbq_02 = data[:, 3]
Tbq_03 = data[:, 4]

s = Singlet()
pt = PyTop(s)
pt.filling_channels_data()

mT2 = np.concatenate([mT]*2, axis=None)
Tbq_nwa = np.concatenate([Tbq_005, Tbq_01], axis=None)
wr = np.array([0.05, 0.1])

Tbq_interp = linear_interp2d(mT2, wr, Tbq_nwa)


wr = np.linspace(0.05, 0.1, 20)

mT2 = np.linspace(700, 1800, 100)


for w in wr:
    for m in mT2:
        inputs = {
            "mT": m,
            "xs_pp_Tbq": Tbq_interp(m, w),
            "xs_pp_Ttq": 0,
            "wr": w
            }
        pt.singlet_width_inputs(**inputs)
        pt.check_singlet_limit()

pt.df.to_csv("data/NWA_input.dat", sep=' ')
'''
#-------------------------------------- Beyond narrow width inputs --------------------------------
'''
Tbq_01 = Tbq_01 * 0.25

wr = np.array([0.1, 0.2, 0.3])
mT3 = np.concatenate([mT]*3, axis=None)
Tbq_bnw = np.concatenate([Tbq_01, Tbq_02, Tbq_03], axis=None)

Tbq_interp_bnw = linear_interp2d(mT3, wr, Tbq_bnw)

wr = np.linspace(0.10001, 0.3, 30)

for w in wr:
    for m in mT2:
        inputs = {
            "mT": m,
            "xs_pp_Ztbq": Tbq_interp_bnw(m, w),
            "xs_pp_Htbq": 0,
            "xs_pp_Zttq": 0,
            "wr": w
            }
        pt.singlet_width_inputs(**inputs)
        pt.check_singlet_limit()

pt.df.to_csv("data/BNWA_input.dat", sep=' ')
'''
'''
s = Singlet()
pt = PyTop(s)
pt.filling_couplings_data()
for k in np.linspace(0.01,1,20):
    for m in range(600, 1800, 2):
        pt.check_coupling_limit(m, k)

pt.df.to_csv("res.dat", sep=' ')
df = pd.read_table("res.dat",delimiter=' ')
plt.scatter(df.loc[df["obs_ratio"]>1, "mass"], df.loc[df["obs_ratio"]>1, "coupling"], color='red')
plt.show()
'''
'''
d = Doublet()
pt = PyTop(d)
pt.filling_channels_data()
data = np.loadtxt("data/Tbq.dat")
mT = data[:, 0]
Tbq_005 = data[:, 1] / 0.25
Tbq_01 = data[:, 2] / 0.25
Tbq_02 = data[:, 3]
Tbq_03 = data[:, 4]

mT2 = np.concatenate([mT]*2, axis=None)
Tbq_nwa = np.concatenate([Tbq_005, Tbq_01], axis=None)
wr = np.array([0.05, 0.1])

Tbq_interp = linear_interp2d(mT2, wr, Tbq_nwa)

wr = np.linspace(0.05, 0.1, 20)

mT2 = np.linspace(700, 1800, 100)

for w in wr:
    for m in mT2:
        inputs = {
            "mT": m,
            "xs_pp_Ttq": Tbq_interp(m, w),
            "wr": w
            }
        pt.doublet_width_ratio_inputs(**inputs)
        pt.check_singlet_limit()
'''
'''
s = Singlet()
pt = PyTop(s)
pt.filling_channels_data()
for k in np.linspace(0.3, 0.7, 20):
    for m in np.arange(1000, 2400, 2):
        params = {
            "mT": m,
            "k_T": k
        }
        pt.singlet_params(**params)
        pt.check_singlet_limit()

#pt.df.to_csv("~/res_2307.dat", sep=' ')
'''
'''
d = Doublet()
pt = PyTop(d)
pt.filling_channels_data()
for k in np.linspace(0.001, 0.7, 20):
    for m in np.arange(600, 2100, 2):
        pt.check_SM_plus_TB_doublet_limit(m, k)

pt.df.to_csv("~/res_coupling_TB.dat", sep=' ')
'''
'''
s = Singlet()
pt = PyTop(s)
pt.filling_channels_data()
for w in np.linspace(0.05, 0.3, 20):
    for m in np.arange(600, 1800, 1):
        params = {
            "mT": m,
            "w_m": w
        }
        pt.singlet_params(**params)
        pt.check_singlet_limit()
pt.df.to_csv("~/expected_2201.dat", sep=" ")
'''
'''
s = Singlet()
pt = PyTop(s)
pt.filling_couplings_data()
w_range = np.linspace(0.05, 0.3, 60)
m_range = np.arange(600, 1801, 1)
for w in w_range:
    for m in m_range:
        params = {
            "mT": m,
            "w_m": w
        }
        pt.singlet_params(**params)
        pt.check_coupling_limit()
pt.df.to_csv("~/test_width_mass.dat", sep=" ")
'''
d = Doublet()
pt = PyTop(d)
pt.filling_couplings_data()
w_range = np.linspace(0.05, 0.3, 6)
m_range = np.arange(600, 1801, 1)
for w in w_range:
    for m in m_range:
        params = {
            "mT": m,
            "w_m": w
        }
        pt.doublet_TB_params(**params)
        pt.check_coupling_limit()


