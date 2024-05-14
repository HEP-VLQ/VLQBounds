import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df1 = pd.read_table('../2201/Res_2201_005.txt',delimiter = ' ')
df2 = pd.read_table('../2201/Res_2201_01.txt',delimiter = ' ')
df3 = pd.read_table('../2201/Res_2201_02.txt',delimiter = ' ')
df4 = pd.read_table('../2201/Res_2201_03.txt',delimiter = ' ')


df = pd.concat([df1,df2,df3,df4],axis=0)

print(df)
#print(df.columns)
vmin=0.0
vmax=0.02

filt = df['ratio']<=1



#levels = np.linspace(vmin, vmax, 50)

plt.tricontourf(df.loc[filt,'mass'],df.loc[filt,'width_to_mass_ratio']*100,df.loc[filt,'observed_limit'])#,levels=levels,extend='both')

#plt.colorbar(ticks=[0.0,0.02],extend='both',label=r'$\sigma(pp\rightarrow Tbq \rightarrow tZbq)$ (pb)')
#plt.colorbar()

#filt = (df['ratio']<=1.01) & (df['ratio']>=0.99)

#plt.plot(df.loc[filt,'mass'],df.loc[filt,'width_to_mass_ratio']*100,color='r',linewidth=2.5)

plt.ylabel(r'$\Gamma/m_T$ [%]')
plt.xlabel(r'$m_T$ [GeV]')
plt.text(700,17,'Excluded',fontsize = 20,fontweight=400) 
plt.title(r"Top Bounds results for $pp\rightarrow Tbq\rightarrow Ztbq$")


plt.show()
