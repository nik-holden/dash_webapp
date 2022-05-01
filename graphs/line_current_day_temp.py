from dash import html, dcc, callback, Input, Output
import plotly.express as px

from common_functions import read_from_db


sql_stmt = """
SELECT 
CASE WHEN t2.station_owner IS NOT NULL THEN t2.station_owner ELSE t1.stationID END AS stationID
,observation_10M_reporting_period AS time
,metric_temp AS temprature 
FROM weather.raw_observations t1
JOIN weather.DIM_weatherstation_details t2 ON t1.stationID = t2.station_id
WHERE current_date_flag = 1 
ORDER BY t2.station_id, t1.observation_10M_reporting_period
"""

curr_day_temp_df = read_from_db(sql_stmt)

# Create list of station ID's
station_list = [i for i in curr_day_temp_df['stationID'].unique()]

# Add the 'All' values to the list of station
station_list.append('All')

station_list.sort()

layout = html.Div([

    html.H1('Current Days Tempratures'),

    html.Div([
        html.Div(dcc.Dropdown(
            id='station_ID',
            clearable=False,
            value='All',
            options=[{'label': i, 'value': i} for i in station_list],
            ),
        )
    ],className='row'),
    dcc.Graph(id='curr_day_temp'),
])

# set up callback function
@callback(
    Output(component_id='curr_day_temp', component_property='figure'),
    Input(component_id='station_ID', component_property='value')
)

def filtered_curr_day_temp(selected_stationID='All'):
    if selected_stationID == 'All':
        filtered_curr_day_temp_df = curr_day_temp_df
    else:
        filtered_curr_day_temp_df = curr_day_temp_df[curr_day_temp_df['stationID'] == selected_stationID]

    line_fig = px.line(data_frame=filtered_curr_day_temp_df,
                       x='time',
                       y='temprature',
                       title=f'Current Days Tempratures: {selected_stationID}',
                       color='stationID',
                       width=1200, height=600)

    return line_fig