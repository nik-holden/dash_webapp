from dash import html, dcc, callback, Input, Output
import plotly.express as px

from common_functions import read_from_db, temp_axis_temp_list

temprature_axis_list = temp_axis_temp_list(-4, 40)


sql_stmt = """
SELECT 
CASE WHEN t2.station_owner IS NOT NULL THEN t2.station_owner ELSE t1.stationID END AS stationID
,CAST(substring(observation_10M_reporting_period, 1,13)+':'+substring(observation_10M_reporting_period, 15,2)+':00' as datetime) AS time
,metric_temp AS temperature 
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

    html.H1('Current Days Temperatures'),

    html.Div([
        html.Div(dcc.Dropdown(
            id='cdt_station_ID',
            clearable=False,
            value='All',
            options=[{'label': i, 'value': i} for i in station_list],
            ),
        )
    ],className='row'),
    dcc.Graph(id='curr_day_temp'),
    dcc.Interval(
        id='lcd_1-minute-interval',
        interval=30000, #30 seconds
        n_intervals=0
    )
])

# set up callback function
@callback(
    Output(component_id='curr_day_temp', component_property='figure'),
    Input(component_id='cdt_station_ID', component_property='value'),
    Input(component_id='lcd_1-minute-interval', component_property='n_intervals')
)

def filtered_curr_day_temp(selected_stationID='All'):
    if selected_stationID == 'All':
        filtered_curr_day_temp_df = curr_day_temp_df
    else:
        filtered_curr_day_temp_df = curr_day_temp_df[curr_day_temp_df['stationID'] == selected_stationID]

    line_fig = px.line(data_frame=filtered_curr_day_temp_df,
                       x='time',
                       y='temperature',
                       title=f'Current Days Temperatures: {selected_stationID}',
                       color='stationID',
                       labels={
                           'time': 'Time of Day',
                           'temperature': 'Temperature (C)'
                       }
                       )

    # line_fig.update_layout(yaxis_range=[-5, 35])

    return line_fig