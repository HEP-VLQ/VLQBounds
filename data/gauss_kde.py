import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

df2 = pd.read_table("coupling_results_2channels.txt",delimiter = ' ')

filt2 = df2['ratio'] >= 1

x = df2.loc[filt2, 'mass']
y = df2.loc[filt2, 's_L']


kde = gaussian_kde(np.vstack([x, y]))


x_grid, y_grid = np.meshgrid(np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100))
z = kde(np.vstack([x_grid.ravel(), y_grid.ravel()]))


z = z.reshape(x_grid.shape)


plt.figure(figsize=(8, 6))
plt.contourf(x_grid, y_grid, x_grid, colors='green', levels=20)  # Adjust levels for smoother or more detailed plot
plt.colorbar(label='Density')
plt.xlabel('mass')
plt.ylabel('s_L')
plt.title('2D Kernel Density Estimation Plot')
plt.show()

