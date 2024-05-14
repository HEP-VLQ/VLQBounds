import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df1 = pd.read_table('../Res_berrouj_S_R_01.txt', delimiter=' ')
df2 = pd.read_table('../Res_berrouj_S_R_02.txt', delimiter=' ')

df = pd.concat([df1, df2], axis=0, ignore_index=True)
print(df)
sorted_df = df.sort_values(by='mass')
print(sorted_df)
# Plot KDE for ratio < 1
filt = df['ratio'] < 1
sns.kdeplot(
    x=sorted_df.loc[filt, 'mass'],
    y=sorted_df.loc[filt, 'sin_R'],
    fill=False,
    color='yellow',
    levels=1000
)

sns.kdeplot(
    x=sorted_df.loc[filt, 'mass'],
    y=sorted_df.loc[filt, 'sin_R'],
    fill=False,
    color='black',
    levels=2
)


#plt.scatter(df.loc[filtered,"mass"],df.loc[filtered,'sin_R'],c=df.loc[filtered,'ratio'])
# Set plot limits based on data range
plt.xlim(sorted_df['mass'].min(), sorted_df['mass'].max())
plt.ylim(0.1, 0.22)

plt.show()

