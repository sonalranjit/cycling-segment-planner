import gpxpy
import gpxpy.gpx
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

with open('./data/rochester-to-eastern-divide.gpx', 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)
    print(f"Number of track points: {gpx.get_track_points_no()}")
    print(f"Elevation extremes: {gpx.get_elevation_extremes()}")
    print(f"Uphill and Downhill: {gpx.get_uphill_downhill()}")

route_info = []
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            route_info.append({
                'latitude': point.latitude,
                'longitude': point.longitude,
                'elevation': point.elevation
            })
print(route_info[:3])
route_df = pd.DataFrame(route_info)
print(route_df.head())

route_df.to_csv('./data/rochester-to-eastern-divide.csv', index=False)

plt.figure(figsize=(14, 8))
plt.scatter(route_df['longitude'], route_df['latitude'], color='#101010')
plt.title('Route latitude and longitude points', size=20)
plt.show()