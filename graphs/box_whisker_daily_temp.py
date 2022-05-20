from dash import html, dcc, callback, Input, Output
import plotly.express as px

from common_functions import read_from_db

sql_stmt = """
SELECT
CASE WHEN t2.station_owner IS NOT NULL THEN t2.station_owner ELSE t1.stationID END AS stationID
-- ,observation_date
,metric_min_temp AS min_temperature
,metric_max_temp AS max_temperature
from weather.daily_weather_metrics t1
JOIN weather.DIM_weatherstation_details t2 ON t1.stationID = t2.station_id
ORDER BY stationID, observation_date
"""

temp_range_df = read_from_db(sql_stmt)

# Create list of station ID's
station_list = [i for i in temp_range_df['stationID'].unique()]

# Add the 'All' values to the list of station
station_list.append('All')

station_list.sort()

layout = html.Div([

    html.H1('Temperature Ranges'),

    html.Div([
        html.Div(dcc.Dropdown(
            id='dt_station_ID',
            clearable=False,
            value='All',
            options=[{'label': i, 'value': i} for i in station_list],
            ),
        )
    ],className='row'),
    dcc.Graph(id='max_temp_range'),
    dcc.Graph(id='min_temp_range'),
    dcc.Interval(
        id='dt_1-minute-interval',
        interval=60000 #60 seconds, 1 minutes
    )
])

# set up callback function
@callback(
    Output(component_id='max_temp_range', component_property='figure'),
    Output(component_id='min_temp_range', component_property='figure'),
    Input(component_id='dt_station_ID', component_property='value')
)

def filtered_min_daily_temp(selected_stationID = 'All'):
    temp_range_df = read_from_db(sql_stmt)
    if selected_stationID == 'All':
        filtered_dataframe = temp_range_df
    else:
        filtered_dataframe = temp_range_df[temp_range_df['stationID'] == selected_stationID]
    

    filtered_temp_range_df = filtered_dataframe.loc[:, filtered_dataframe.columns!='min_temperature']
    
    max_box_fig = px.box(data_frame=filtered_temp_range_df,
                       x='stationID',
                       y='max_temperature',
                       title=f'Max Temperatures: {selected_stationID}',
                       color='stationID'
                       )
    
    filtered_temp_range_df = filtered_dataframe.loc[:, filtered_dataframe.columns!='max_temperature']
    
    min_box_fig = px.box(data_frame=filtered_temp_range_df,
                       x='stationID',
                       y='min_temperature',
                       title=f'Min Temperatures: {selected_stationID}',
                       color='stationID'
                       )

    
    return min_box_fig, max_box_fig