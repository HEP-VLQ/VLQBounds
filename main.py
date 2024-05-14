from initialize import Tables
from Results import Result
from prediction_manip import Theoretical_prediction
import numpy as np




if __name__ == '__main__':


 data = np.loadtxt("data/2201/Tbq_interpolated.txt")
 mass = data[:,0]
 cs_ga_mt_005 = data[:,1]*(0.5/0.25)
 cs_ga_mt_01 = data[:,2]*(0.5/0.25)
 cs_ga_mt_02 = data[:,3]*(0.5/0.25)
 cs_ga_mt_03 = data[:,4]*(0.5/0.25)
 with open('data/2201/two_times_SP_0.3.txt','w') as f:
  f.write("mass result channel_or_id theo_cross_section ratio observed_limit width_to_mass_ratio\n")
  for m,cs in zip(mass,cs_ga_mt_03): 
   theo = Theoretical_prediction()
   theo.Set_Model('Singlet')
   theo.Set_width_to_mass_ratio(0.3)
   theo.Find_Singlet_Limit(m,-1,cs,-1)
   obs_ratio=theo.obsratio
   x = 1/obs_ratio
   f.write(f"{theo.MT_theo} {theo.allowed} {theo.channel} {cs} {theo.obsratio} {x*cs} {theo.width_mass_ratio}\n")
   
   print("Theoretical mass : ",theo.MT_theo)
   print(theo)
   print("---------------------------------------------------------------------")
   
 '''data = np.loadtxt("data/berrouj_s_R_02.txt")
 mass = data[:,0]
 cs_theo = data[:,1]/1000
 with open('data/Res_berrouj_S_R_01_pure.txt','w') as f:
  f.write("mass result channel_or_id theo_cross_section ratio observed_limit sin_R\n")
  for m,cs in zip(mass,cs_theo): 
   theo = Theoretical_prediction()
   theo.Set_Model('Pure')
   theo.Set_width_to_mass_ratio(0.05)
   theo.Pure_decay_input(m,-1,cs,-1,1,0,0)
   obs_ratio=theo.obsratio
   x = 1/obs_ratio
   i = theo.channel
   f.write(f"{theo.MT_theo} {theo.allowed} {theo.channel} {cs} {theo.obsratio} {x*cs} {0.2}\n")
   
   print("Theoretical mass : ",theo.MT_theo)
   print(theo)
   print("The limit given results is :",theo.label[i])
   print("---------------------------------------------------------------------")'''
