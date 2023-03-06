import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo

route_df = pd.read_csv('./data/rochester-to-eastern-divide-gradient.csv')
print(route_df.head())
print(route_df['gradient'].describe())

bins = pd.IntervalIndex.from_tuples([
    (-30, -10),
    (-10, -5),
    (-5, -3),
    (-3, -1),
    (-1, 0),
    (0, 1),
    (1, 3),
    (3, 5),
    (5, 7),
    (7, 10),
    (10, 12),
    (12, 15),
    (15, 20)
], closed='left')

print(bins)
route_df['gradient_range'] = pd.cut(route_df['gradient'], bins=bins)
print(route_df.head())

gradient_details = []

# for each unique gradient range
for gr_range in route_df['gradient_range'].unique():
    # keep that subset only
    subset = route_df[route_df['gradient_range'] == gr_range]

    #statistics
    total_distance = subset['distance'].sum()
    pct_of_total_ride = (subset['distance'].sum() / route_df['distance'].sum()) * 100
    elevation_gain = subset[subset['elevation_diff'] > 0]['elevation_diff'].sum()
    elevation_lost = subset[subset['elevation_diff'] < 0]['elevation_diff'].sum()

    #save results
    gradient_details.append({
        'gradient_range': gr_range,
        'total_distance': np.round(total_distance, 2),
        'pct_of_total_ride': np.round(pct_of_total_ride, 2),
        'elevation_gain': np.round(elevation_gain, 2),
        'elevation_lost': np.round(np.abs(elevation_lost), 2)
    })

gradient_details_df = pd.DataFrame(gradient_details).sort_values(by='gradient_range').reset_index(drop=True)
print(gradient_details_df.head())

colors = [
    '#0d46a0', '#2f3e9e', '#2195f2', '#4fc2f7',
    '#a5d6a7', '#66bb6a', '#fff59d', '#ffee58',
    '#ffca28', '#ffa000', '#ff6f00', '#f4511e', '#bf360c'
]

custom_text = [f'''<b>{gr}%</b> - {dst}km''' for gr, dst in zip(
    gradient_details_df['gradient_range'].astype('str'),
    gradient_details_df['total_distance'].apply(lambda x: round(x / 1000, 2))
)]

fig = go.Figure(
    data = [go.Bar(
        x = gradient_details_df['gradient_range'].astype(str),
        y = gradient_details_df['total_distance'].apply(lambda x: round(x / 1000, 2)),
        marker_color = colors,
        text = custom_text
    )],
    layout = go.Layout(
        bargap = 0,
        title = 'Gradient profile of a route',
        xaxis_title = 'Gradient range (%)',
        yaxis_title = 'Distance covered (km)',
        autosize=False,
        width = 1440,
        height = 800,
        template = 'simple_white'
    )
)

fig.show()