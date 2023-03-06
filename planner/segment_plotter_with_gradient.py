import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (16,6)
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

route_df = pd.read_csv('./data/rochester-to-eastern-divide-elevation-difference.csv')
print(route_df)

gradients = [np.nan]
for ind, row in route_df.iterrows():
    if ind == 0:
        continue
    grade = (row['elevation_diff'] / row['distance']) * 100
    
    if grade > 30:
        gradients.append(np.nan)
    else:
        gradients.append(np.round(grade, 1))

print(gradients[:10])

route_df['gradient'] = gradients
print(route_df.head())
print(route_df[route_df['gradient'].isna()])
route_df['gradient'] = route_df['gradient'].fillna(0)
print(route_df.head())

plt.title('Terrain gradient on the route', size=20)
plt.xlabel('Data point', size=14)
plt.ylabel('Gradient (%)', size=14)
plt.plot(np.arange(len(gradients)), gradients, lw=2, color='#101010')
plt.show()

route_df.to_csv('./data/rochester-to-eastern-divide-gradient.csv', index=False)