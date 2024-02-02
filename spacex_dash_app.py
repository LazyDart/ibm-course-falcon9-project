# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                                    options=[
                                                        {'label': 'All Sites', 'value': 'ALL'},
                                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                    ],
                                                    value='ALL',
                                                    placeholder="Launch Site",
                                                    searchable=True
                                                    ),),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                        100: '100'},
                                                value=[0, 10000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == "ALL":
        spacex_site = spacex_df.copy()
        plot_data = spacex_df.groupby("Launch Site")["class"].mean().reset_index()
        fig = px.pie(plot_data, values='class', 
                        names='Launch Site', 
                        title='Success Rate for Different Sites')
        return fig
    else:
        spacex_site = spacex_df[spacex_df["Launch Site"] == selected_site].copy()
        plot_data = (spacex_df.groupby("class")["Launch Site"].count()/len(spacex_df)).reset_index()
        fig = px.pie(plot_data, values='Launch Site', 
                        names=["Percent Success", "Percent Failed"], 
                        title='Success Ratio for Selected Site')
        return fig
    


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value')]
)
def update_pie_chart(selected_site, selected_range):
    if selected_site == "ALL":
        plot_data = spacex_df[spacex_df["Payload Mass (kg)"].between(selected_range[0], selected_range[1])].copy()
        # plot_data = spacex_df.groupby("Launch Site")["class"].mean().reset_index()
        fig = px.scatter(plot_data, x="Payload Mass (kg)",
                        y="class",
                        title='Success by Payload Mass (kg)',
                        color="Booster Version Category")
        return fig
    else:
        plot_data = spacex_df[(spacex_df["Launch Site"] == selected_site) &
                                spacex_df["Payload Mass (kg)"].between(selected_range[0], selected_range[1])].copy()

        fig = px.scatter(plot_data, x="Payload Mass (kg)", 
                        y="class",
                        title='Success by Payload Mass (kg)',
                        color="Booster Version Category")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

