import folium
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

route_df = pd.read_csv("./data/rochester-to-eastern-divide.csv")
print(route_df.head())

route_map = folium.Map(
    location=[43.157130, -77.615550],
    zoom_start=13,
    tiles="CartoDBPositron",
    width=1024,
    height=600,
)

coordinates = [tuple(x) for x in route_df[["latitude", "longitude"]].to_numpy()]
folium.PolyLine(coordinates, weight=6).add_to(route_map)

route_map.save("./data/rochester-to-eastern-divide.html")
