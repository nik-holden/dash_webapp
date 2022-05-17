#from turtle import width
from dash import html, dcc, callback, Input, Output
import plotly.express as px

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

# Add the 'All' values to the list of station
station_list.append('All')

station_list.sort()

layout = html.Div([

    html.H1('Daily high-low Temperatures'),

    html.Div([
        html.Div(dcc.Dropdown(
            id='dt_station_ID',
            clearable=False,
            value='All',
            options=[{'label': i, 'value': i} for i in station_list],
            ),
        )
    ],className='row'),
    dcc.Graph(id='max_daily_temp'),
    dcc.Graph(id='min_daily_temp'),
    dcc.Interval(
        id='dt_1-minute-interval',
        interval=60000 #60 seconds, 1 minutes
    )
])

# set up callback function
@callback(
    Output(component_id='max_daily_temp', component_property='figure'),
    Output(component_id='min_daily_temp', component_property='figure'),
    Input(component_id='dt_station_ID', component_property='value')
)

def filtered_min_daily_temp(selected_stationID = 'All'):
    if selected_stationID == 'All':
        filtered_dataframe = daily_temp_df
    else:
        filtered_dataframe = daily_temp_df[daily_temp_df['stationID'] == selected_stationID]
    

    filtered_max_daily_temp = filtered_dataframe.loc[:, filtered_dataframe.columns!='min_temperature']
    max_line_fig = px.line()

    max_line_fig = px.line(data_frame=filtered_max_daily_temp,
                       x='observation_date',
                       y='max_temperature',
                       title=f'Current Days Max Temperatures: {selected_stationID}',
                       color='stationID'
                       )

    max_line_fig.update_layout(yaxis_range=[-5, 35])

    
    filtered_min_daily_temp = filtered_dataframe.loc[:, filtered_dataframe.columns!='max_temperature']
    
    min_line_fig = px.line

    min_line_fig = px.line(data_frame=filtered_min_daily_temp,
                       x='observation_date',
                       y='min_temperature',
                       title=f'Current Days Min Temperatures: {selected_stationID}',
                       color='stationID'
                       )

    min_line_fig.update_layout(yaxis_range=[-5, 35])

    return min_line_fig, max_line_fig