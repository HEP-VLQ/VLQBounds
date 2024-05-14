import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import scienceplots

def Tbq_Exclusion(mass,gamma_mT,observed,obsratio):
  
  filtering = obsratio<1
  
  mass_exc = mass[filtering]
  
  gamma_exc = gamma_mT[filtering]
  
  observ_exc = observed[filtering]
  
  #sns.kdeplot(x=mass_allowed,y=gamma,fill=True,color='yellow',levels=1000)
  plt.tricontourf(mass_exc,gamma_exc,observ_exc,colors='lightblue')
  

  plt.xlabel(r'$m_T$ [GeV]')
  plt.ylabel(r'$\kappa_{T}$ ')
  #plt.text(650,0.22,'Excluded',fontsize = 20,fontweight=900)
  #plt.xlim(600,1200)
  plt.ylim(0.05,0.25)
  '''obsratio_equal_one = []
  mass_of_interpolation= []
  gamma_mT_filtered = []

  for i in range(len(mass)):
    if 0.99<= obsratio[i] <= 1.01:
     obsratio_equal_one.append(obsratio[i])
     mass_of_interpolation.append(mass[i])
     gamma_mT_filtered.append(gamma_mT[i])

  plt.plot(mass_of_interpolation,gamma_mT_filtered,color='black',linewidth=4)'''
  plt.title(r'Top Bounds Results for $Tbq\rightarrow tHbq$')

plt.figure(figsize=(7,5))
#data = np.loadtxt("fichier_doublet_1705.txt")
data = np.loadtxt("SL_Tbq.txt")
#data = np.loadtxt("Res_2302.txt")

plt.style.use('science')
#plt.style.use('grid')

mass = data[:,0]

allowed = data[:,1]

channel = data[:,2]

pp_TTbar = data[:,3]

#pp_Tbq = data[:,3]

obsratio = data[:,4]

gamma = data[:,5]

observed = data[:,6]

#kappa = data[:,6]

Tbq_Exclusion(mass,gamma,observed,obsratio)






plt.show()

