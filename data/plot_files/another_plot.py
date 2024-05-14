import matplotlib.pyplot as plt
import numpy as np


data = np.loadtxt("SL.txt")
#data = np.loadtxt("SL_Tbq.txt")

mass = data[:,0]

allowed = data[:,1]

pp_TTbar = data[:,3]

#pp_Tbq = data[:,3]

obsratio = data[:,4]

y = np.ones(len(mass))

#gamma_mT = data[:,5]*100

#pp_Tbq = pp_Tbq[pp_Tbq<=2]

#gamma = gamma_mT[pp_Tbq<=2]
#filter_condition = pp_Tbq <= 6

#m = m[filter_condition]
#pp_Tbq = pp_Tbq[filter_condition]
#gamma_mT = gamma_mT[filter_condition]

'''m = mass[allowed==0]
gamma = gamma_mT[allowed==0]
Tbq = pp_Tbq[allowed==0]
	
plt.tricontourf(m,gamma, Tbq,colors = 'gray')

m = mass[allowed==1]
gamma = gamma_mT[allowed==1]
Tbq = pp_Tbq[allowed==1]

plt.tricontourf(m,gamma, Tbq,colors = 'green')

plt.text(700, 15, 'Excluded', fontsize = 15)
plt.text(1400, 15, 'Allowed', fontsize = 15)

plt.ylabel(r'$\Gamma/m_T$ [%]')
plt.xlabel(r'$m_T$ (GeV)')
plt.title(r'Top Bounds results on $pp \rightarrow Tbq \rightarrow Ztbq$')'''

#exclu = allowed[allowed==1]

#gamma = gamma_mT[allowed==0]

#mass = m[allowed==1]


#pp_TTbar = pp_TTbar[allowed==1]
#colors = ['red', 'green']

#print(pp_Tbq1) 
#plt.tricontourf(m,pp_TTbar,allowed)
#plt.colorbar()


#plt.colorbar()
#plt.ylabel(r'$\Gamma/m_T$ [%]')
#plt.xlabel(r'$m_T$ (GeV)')

#plt.text(700, 15, 'Excluded', fontsize = 15)
#plt.text(1400, 15, 'Allowed', fontsize = 15)


'''mass_filtered = []
bbar_filtered = []
allowed_filtered = []
for i in range(len(mass)):
 if allowed[i] == 0 :
  mass_filtered.append(mass[i])
  bbar_filtered.append(pp_TTbar[i])
  allowed_filtered.append(allowed[i])
plt.tricontourf(mass_filtered,bbar_filtered,allowed_filtered,colors='gray')  

mass_filtered = []
bbar_filtered = []
allowed_filtered = []
for i in range(len(mass)):
 if allowed[i] == 1 :
  mass_filtered.append(mass[i])
  bbar_filtered.append(pp_TTbar[i])
  allowed_filtered.append(allowed[i])
plt.tricontourf(mass_filtered,bbar_filtered,allowed_filtered,colors='green')  
plt.ylabel(r'$\sigma(pp\rightarrow T\overline{T})$ [pb]')
plt.xlabel(r'$m_T$ (GeV)')  
plt.title(r'Top Bounds Exclusion Results')  
#plt.yscale('log')
plt.text(700, 15, 'Excluded', fontsize = 15)
plt.text(1400, 15, 'Allowed', fontsize = 15)'''

plt.figure(figsize=(10, 8))
plt.plot(mass,obsratio)
plt.plot(mass,y)
plt.xlabel(r'$m_T$ (GeV)')
plt.ylabel(r'$\frac{[\sigma\times BR(T\rightarrow doublet)]_{Model}}{[\sigma\times BR(T \rightarrow doublet)]_{Limit}}$', fontsize=20)
plt.xlim(800,2000)
#plt.ylim(0,18)
plt.yscale('log')
plt.title(r'Top Bounds Exclusion Results') 
plt.show()
