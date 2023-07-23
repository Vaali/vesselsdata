import plotly.graph_objects as go
import pandas as pd
import database as db
columns, rows = db.get_data('2023-01-30')
df1 = pd.DataFrame(rows, columns=columns)
columns, rows = db.get_data('2023-01-31')
df2 = pd.DataFrame(rows, columns=columns)
columns, rows = db.get_data('2023-01-29')
df3 = pd.DataFrame(rows, columns=columns)
# Sample data for three layers with East Coast latitude and longitude coordinates

# Create the figure using Plotly graph_objects and add scatter traces for each layer
fig = go.Figure()

layer1_trace = go.Scattermapbox(
    lat=df1['lat'],
    lon=df1['long'],
    text=df1['vessel_name'],
    marker=dict(
        size=12,
        opacity=0.6,
    ),
    name='Layer 1',  # Display the layer name in the legend
)

layer2_trace = go.Scattermapbox(
    lat=df2['lat'],
    lon=df2['long'],
    text=df2['vessel_name'],
    marker=dict(
        size=12,
        opacity=0.6,
    ),
    name='Layer 2',  # Display the layer name in the legend
)

layer3_trace = go.Scattermapbox(
    lat=df3['lat'],
    lon=df3['long'],
    text=df3['vessel_name'],
    marker=dict(
        size=12,
        opacity=0.6,
    ),
    name='Layer 3',  # Display the layer name in the legend
)

fig.add_trace(layer1_trace)
fig.add_trace(layer2_trace)
fig.add_trace(layer3_trace)

# Set the map layout
fig.update_layout(
    mapbox=dict(
        style='carto-positron',
        center=dict(lat=37.0902, lon=-95.7129),  # Center the map on the East Coast of the United States
        zoom=2,
    ),
    margin=dict(l=0, r=0, t=0, b=0),
)

# Create an animation slider
steps = []
for i, trace in enumerate(fig.data):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              {"title": "Layer: " + trace.name}],
    )
    step["args"][0]["visible"][i] = True  # Show the corresponding layer
    steps.append(step)

# Add a "Show All" button to reset visibility to all layers
show_all_button = dict(
    label="Show All",
    method="update",
    args=[{"visible": [True] * len(fig.data)},
          {"title": "All Layers"}],
)

steps.append(show_all_button)

sliders = [dict(
    active=0,
    pad={"t": 50},
    steps=steps,
)]

# Create a dropdown menu for selecting layers
layer_names = [trace.name for trace in fig.data]
buttons = []
for i, layer_name in enumerate(layer_names):
    button = dict(
        label=layer_name,
        method="update",
        args=[{"visible": [layer == i for layer in range(len(fig.data))]},
              {"title": "Layer: " + layer_name}],
    )
    buttons.append(button)

updatemenus = list([
    dict(
        buttons=buttons + [show_all_button],
        active=0,
        pad={"t": 50},
    )
])

# Update the layout with the slider, dropdown menu, and clickmode for selection
fig.update_layout(sliders=sliders, updatemenus=updatemenus, clickmode='event+select')

# Define a callback function to handle selection events
def display_selected_points(trace, points, selector):
    if points.point_inds:
        selected_data = trace.customdata[points.point_inds[0]]
        print(f"Selected Data: {selected_data}")

# Assign the callback function to each trace
for trace in fig.data:
    trace.on_click(display_selected_points)

# Show the plot
fig.show()
