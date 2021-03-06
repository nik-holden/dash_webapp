from dash import html, dcc, callback, Input, Output
import plotly.express as px

from common_functions import read_from_db


line_sql_stmt = """
SELECT 
CASE WHEN t2.station_owner IS NOT NULL THEN t2.station_owner ELSE t1.stationID END AS stationID
,observation_date
,SUM(metric_precipitationDailyTotal) over(partition by stationID order by observation_date) as running_rainfall_total 
FROM weather.daily_weather_metrics t1
JOIN weather.DIM_weatherstation_details t2 ON t1.stationID = t2.station_id
WHERE current_month_flag = 1
ORDER BY stationID, observation_date 
"""

#daily_rain_df = pd.read_sql(sql_stmt, conn)
daily_rain_line_df = read_from_db(line_sql_stmt)

bar_sql_stmt = """SELECT 
CASE WHEN t2.station_owner IS NOT NULL THEN t2.station_owner ELSE t1.stationID END AS stationID
,observation_date
,SUM(metric_precipitationDailyTotal) daily_rainfall_total 
FROM weather.daily_weather_metrics t1
JOIN weather.DIM_weatherstation_details t2 ON t1.stationID = t2.station_id
WHERE current_month_flag = 1
GROUP BY t1.stationID
,t2.station_owner 
,observation_date
ORDER BY stationID, observation_date 
"""

#daily_rain_df = pd.read_sql(sql_stmt, conn)
daily_rain_bar_df = read_from_db(bar_sql_stmt)

# Create list of station ID's
station_list = [i for i in daily_rain_line_df['stationID'].unique()]

# Add the 'All' values to the list of station
station_list.append('All')

station_list.sort()

layout = html.Div([

    html.H1('Monthly Total Daily Rain Amount'),

    html.Div([
        html.Div(dcc.Dropdown(
            id='mr_station_ID',
            clearable=False,
            value='All',
            options=[{'label': i, 'value': i} for i in station_list],
            ),
        )
    ],className='row'),
    dcc.Graph(id='total_daily_rain_line'),
    dcc.Graph(id='total_daily_rain_bar'),

    dcc.Interval(
        id='mr_1-minute-interval',
        interval=60000 #60 seconds, 1 minutes
    )
])

# set up callback function
@callback(
    Output(component_id='total_daily_rain_line', component_property='figure'),
    Output(component_id='total_daily_rain_bar', component_property='figure'),
    Input(component_id='mr_station_ID', component_property='value')
)

def filtered_daily_rain(selected_stationID='All'):
    daily_rain_line_df = read_from_db(line_sql_stmt)
    daily_rain_bar_df = read_from_db(bar_sql_stmt)
    if selected_stationID == 'All':
        filtered_daily_rain_line_df = daily_rain_line_df
        filtered_daily_bar_line_df = daily_rain_bar_df
    else:
        filtered_daily_rain_line_df = daily_rain_line_df[daily_rain_line_df['stationID'] == selected_stationID]
        filtered_daily_bar_line_df = daily_rain_bar_df[daily_rain_bar_df['stationID'] == selected_stationID]

    line_fig = px.line(data_frame=filtered_daily_rain_line_df,
                       x='observation_date',
                       y='running_rainfall_total',
                       title=f'Current Months Daily Total Rainfall: Line: {selected_stationID}',
                       color='stationID',
                       labels={
                           #'observation_date': 'Date',
                           'running_rainfall_total': 'Total Rainfall (mm)'
                       }
                    )
    
    bar_fig = px.bar(data_frame=filtered_daily_bar_line_df,
                       x='stationID',
                       y='daily_rainfall_total',
                       title=f'Current Months Daily Total Rainfall: Bar: {selected_stationID}',
                       color='observation_date',
                       labels={
                           'stationID': 'station ID',
                           'daily_rainfall_total    ': 'Total Rainfall (mm)'
                       }
                    )
    return line_fig, bar_fig