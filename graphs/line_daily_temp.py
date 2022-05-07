from turtle import width
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go

from common_functions import read_from_db


sql_stmt = """
SELECT
CASE WHEN t2.station_owner IS NOT NULL THEN t2.station_owner ELSE t1.stationID END AS stationID
,observation_date
,metric_min_temp AS min_temperature
,metric_max_temp AS max_temperature
from weather.daily_weather_metrics t1
JOIN weather.DIM_weatherstation_details t2 ON t1.stationID = t2.station_id
ORDER BY stationID, observation_date
"""

daily_temp_df = read_from_db(sql_stmt)

# Create list of station ID's
station_list = [i for i in daily_temp_df['stationID'].unique()]

station_list.sort()

first_stationID = station_list[0]

layout = html.Div([

    html.H1('Daily high-low Temperatures'),

    html.Div([
        html.Div(dcc.Dropdown(
            id='dt_station_ID',
            clearable=False,
            value=first_stationID,
            options=[{'label': i, 'value': i} for i in station_list],
            ),
        )
    ],className='row'),
    dcc.Graph(id='daily_temp'
    ),
    
    dcc.Interval(
        id='dt_1-minute-interval',
        interval=60000 #60 seconds, 1 minutes
    )
])

# set up callback function
@callback(
    Output(component_id='daily_temp', component_property='figure'),
    Input(component_id='dt_station_ID', component_property='value')
)

def filtered_daily_temp(selected_stationID=first_stationID):
    if selected_stationID == selected_stationID:
        filtered_daily_temp_df = daily_temp_df[daily_temp_df['stationID'] == selected_stationID]

    line_fig = go.Figure()

    line_fig.add_trace(go.Scatter(
        x=filtered_daily_temp_df['observation_date'],
        y=filtered_daily_temp_df['min_temperature'],
        name = 'min_temperature',
        line=dict(color='blue', width=4)
    ))
    line_fig.add_trace(go.Scatter(
        x=filtered_daily_temp_df['observation_date'],
        y=filtered_daily_temp_df['max_temperature'],
        name = 'max_temperature',
        line=dict(color='red', width=4)
    ))
    return line_fig