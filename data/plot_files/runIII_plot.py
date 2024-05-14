import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df1 = pd.read_table('../Res_berrouj_S_R_01.txt',delimiter = ' ')
df2 = pd.read_table('../Res_berrouj_S_R_02.txt',delimiter = ' ')



df = pd.concat([df1,df2],axis=0)

y = np.ones(len(df1['mass']))

#print(df.columns)
#print(df)
#filt = df['result']==1
#filt2 = df['result']==0
#sns.kdeplot(x=df.loc[filt,'mass'],y=df.loc[filt,'sin_R'],fill=True,color='green',levels=1000)
#sns.kdeplot(x=df.loc[filt2,'mass'],y=df.loc[filt2,'sin_R'],fill=True,color='yellow',levels=1000)
plt.plot(df1["mass"],df1["ratio"],color='g',label = r'$sin(\theta_R) = 0.1$')
plt.plot(df2["mass"],df2["ratio"],color='b',label = r'$sin(\theta_R) = 0.2$')
plt.plot(df1['mass'],y,color = 'r',label=r'$\sigma(Tbq)_{theo}/\sigma(Tbq)_{obs}=1$')
plt.yscale('log')

plt.xlim(df['mass'].min(),df['mass'].max())

plt.legend()

plt.xlabel(r'$m_T$ [GeV]')
plt.ylabel(r'$\sigma(Tbq)_{theo}/\sigma(Tbq)_{obs}$')
#
#
#plt.tricontourf(df.loc[filt,'mass'],df.loc[filt,'sin_R'],df.loc[filt,'observed_limit'],colors='lightgreen')
#plt.scatter(df.loc[filt,'mass'],df.loc[filt,'sin_R'],c=df.loc[filt,'result'],color='green')
#plt.scatter(df.loc[filt2,'mass'],df.loc[filt2,'sin_R'],c=df.loc[filt2,'result'],color='r')
#contour.set_facecolor('#ADD8E6') 
#plt.scatter(df['mass'],df['sin_R'],c=df['result'])
#plt.colorbar()
#plt.colorbar(ticks=[0.0,0.02,0.04,0.06,0.08,0.08,0.1,0.12,0.14],extend='both',label=r'$\sigma(pp\rightarrow Tbq \rightarrow tZbq)$ (pb)')




'''
plt.ylabel(r'$\Gamma/m_T$ [%]')
plt.xlabel(r'$m_T$ [GeV]')
#plt.text(700,17,'Excluded',fontsize = 20,fontweight=400) 
plt.title(r"Top Bounds results for $pp\rightarrow Tbq\rightarrow Ztbq$")
'''

plt.show()
