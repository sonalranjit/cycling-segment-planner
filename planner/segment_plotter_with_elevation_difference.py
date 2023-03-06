import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import haversine as hs

plt.rcParams["figure.figsize"] = (16, 6)
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False


def haversine_distance(lat1, lon1, lat2, lon2) -> float:
    distance = hs.haversine(
        point1=(lat1, lon1), point2=(lat2, lon2), unit=hs.Unit.METERS
    )
    return np.round(distance, 2)


route_df = pd.read_csv("./data/rochester-to-fairfax.csv")
print(route_df)

route_df["elevation_diff"] = route_df["elevation"].diff()
print(route_df)

distances = [np.nan]
for i in range(len(route_df)):
    if i == 0:
        continue
    else:
        distances.append(
            haversine_distance(
                lat1=route_df.iloc[i - 1]["latitude"],
                lon1=route_df.iloc[i - 1]["longitude"],
                lat2=route_df.iloc[i]["latitude"],
                lon2=route_df.iloc[i]["longitude"],
            )
        )

route_df["distance"] = distances
print(route_df.head())
print(
    f"Elevation difference: {route_df[route_df['elevation_diff'] >= 0]['elevation_diff'].sum()}"
)
print(f"Total distance: {route_df['distance'].sum()}")

route_df["cum_elevation"] = route_df["elevation_diff"].cumsum()
route_df["cum_distance"] = route_df["distance"].cumsum()
print(route_df.head())

route_df = route_df.fillna(0)
print(route_df.head())
route_df.to_csv("./data/rochester-to-fairfax-elevation-difference.csv")

plt.plot(route_df["cum_distance"], route_df["cum_elevation"], color="#101010", lw=3)
plt.title("Route elevation profile", size=20)
plt.xlabel("Distance in meters", size=14)
plt.ylabel("Elevation in meters", size=14)
plt.show()
