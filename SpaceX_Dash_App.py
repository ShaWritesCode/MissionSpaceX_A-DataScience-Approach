import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Extract the max and min payload mass for the range slider
max_payload = int(spacex_df['Payload Mass (kg)'].max())  # Convert to integer
min_payload = int(spacex_df['Payload Mass (kg)'].min())  # Convert to integer

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                             ],
                                             value='ALL',
                                             placeholder="Select a Launch Site",
                                             style={'width': '50%', 'padding': '3px', 'font-size': '20px', 'textAlign': 'center'}
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=max_payload, step=1000,
                                                marks={i: str(i) for i in range(0, max_payload, 5000)},
                                                value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2: Callback function to update the pie chart based on selected site
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Group data by launch success and count total launches
        pie_data = spacex_df.groupby('class').size().reset_index(name='count')
        fig = px.pie(pie_data, names='class', values='count', title='Total Success vs Failed Launches')
    else:
        # Filter data based on selected site and show success vs failed launches for the site
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        pie_data = site_data.groupby('class').size().reset_index(name='count')
        fig = px.pie(pie_data, names='class', values='count', title=f'Success vs Failed Launches for {selected_site}')
    return fig

# TASK 4: Callback function to update scatter plot based on selected site and payload range
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_plot(selected_site, payload_range):
    low, high = payload_range
    # Filter data based on site and payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    
    if selected_site != 'ALL':
        # Further filter data based on selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    # Create scatter plot for the filtered data
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                     title=f'Launch Success vs Payload Mass for {selected_site} (Filtered)')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8052)







