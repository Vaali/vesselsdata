import plotly.graph_objects as go
import pandas as pd
import pandas as pd
import database as db
columns, rows = db.get_data('2023-01-30')
data = pd.DataFrame(rows, columns=columns)
columns, rows = db.get_data('2023-01-31')
df2 = pd.DataFrame(rows, columns=columns)

data['datetime'] = data['date'] + data['time']

# Create an empty figure
fig = go.Figure()

# Create a scattergeo trace for the time series data
trace = go.Scattergeo(
    lat=data['lat'],
    lon=data['long'],
    text=data['vessel_name'],
    #mode='markers',
    marker=dict(
        size=12,
        opacity=0.6,
    )
)

# Add the scattergeo trace to the figure
fig.add_trace(trace)

# Update the layout with map settings
fig.update_layout(
    title='Time Series Data on Geo Map (Animation)',
    #geo=dict(projection_type="mercator", showland=True, landcolor="lightgray"),
)
fig.update_layout(
    mapbox=dict(
        style='carto-positron',
        center=dict(lat=37.0902, lon=-95.7129),  # Center the map on the East Coast of the United States
        zoom=2,
    ),
    margin=dict(l=0, r=0, t=0, b=0),
)
# Add animation settings
animation_settings = dict(
    frame=dict(duration=500, redraw=True),
    fromcurrent=True,
    mode='immediate'
)

# Add a play button for the animation
fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[dict(label='Play', method='animate', args=[None, animation_settings])])])

# Create frames for each step in the animation
frames = []
for date in data['datetime'].unique():
    # Filter data for the current day
    frame_data = data[data['datetime'] == date].copy()

    # Create a scattergeo trace for the current day
    frame_trace = go.Scattergeo(
        lat=frame_data['lat'],
        lon=frame_data['long'],
        text=frame_data['vessel_name'],  # Show both date and time in the tooltip
        marker=dict(size=12,
        opacity=0.6,),
        mode='markers',
    )

    # Create a frame for the current day and append it to the list of frames
    frame = go.Frame(data=[frame_trace], name=str(date))
    frames.append(frame)
# Add frames to the figure
fig.frames = frames

# Show the plot
fig.show()
