import pandas as pd
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

import common_functions as cf

connection, sqlalchmey_engine = cf.azure_sql_db_connection()

with sqlalchmey_engine.connect() as conn:

    sql_stmt = """
    SELECT *
    , SUM(metric_precipitationDailyTotal) over(partition by stationID order by observation_date) as running_rainfall_total 
    FROM weather.daily_weather_metrics WHERE current_month_flag = 1"""

    daily_rain_df = pd.read_sql(sql_stmt, conn)

# Create list of station ID's
station_list = [i for i in daily_rain_df['stationID'].unique()]

# Add the 'All' values to the list of station
station_list.append('All')

# Create Dash app

dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
line_graph_app = dash_app.server

dash_app.layout = html.Div(children=[
    html.H1(children='Monthly Total Daily Rain Amount'),
    dcc.Dropdown(id='station_ID',
                 options=[{'label': i, 'value': i} for i in station_list],
                 #options=[{'label': i, 'value': i} for i in daily_rain_df['stationID'].unique()],
                 value='All'),
    dcc.Interval(id='rain_graph_interval', interval=1000, n_intervals=10),
    dcc.Graph(id='total_daily_rain')
])

# set up callback function
@dash_app.callback(
    Output(component_id='total_daily_rain', component_property='figure'),
    Input(component_id='station_ID', component_property='value')
)

def filtered_daily_rain(selected_stationID):
    if selected_stationID == 'All':
        filtered_daily_rain_df = daily_rain_df
    else:
        filtered_daily_rain_df = daily_rain_df[daily_rain_df['stationID'] == selected_stationID]

    line_fig = px.line(data_frame=filtered_daily_rain_df,
                       x='observation_date',
                       y='running_rainfall_total',
                       title=f'Current Mmonths Daily Total Rainfall: {selected_stationID}',
                       color='stationID',
                       width=1200, height=600)

    return line_fig

# Run local server
if __name__ == '__main__':
    dash_app.run_server(debug=True)
