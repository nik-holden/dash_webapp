from dash import html, dcc, callback, Input, Output
import plotly.express as px

from common_functions import read_from_db


line_sql_stmt = """WITH cte_YTD_rain AS (SELECT 
CASE WHEN t2.station_owner IS NOT NULL THEN t2.station_owner ELSE t1.stationID END AS stationID
,CONCAT(DATEPART(year, observation_date),'-',DATEPART(month, observation_date)) AS observation_month
,SUM(metric_precipitationDailyTotal) as running_rainfall_total 
FROM weather.daily_weather_metrics t1
JOIN weather.DIM_weatherstation_details t2 ON t1.stationID = t2.station_id
WHERE FORMAT(observation_date, 'yyyy') = FORMAT(CURRENT_TIMESTAMP, 'yyyy')
GROUP BY CASE WHEN t2.station_owner IS NOT NULL THEN t2.station_owner ELSE t1.stationID END
, CONCAT(DATEPART(year, observation_date),'-',DATEPART(month, observation_date))
)

SELECT stationID,
observation_month,
SUM(running_rainfall_total) over (partition by stationID ORDER BY observation_month) AS YTD_rainfall
FROM cte_YTD_rain
ORDER BY stationID, observation_month 
"""


monthly_rain_line_df = read_from_db(line_sql_stmt)

bar_sql_stmt = """SELECT 
CASE WHEN t2.station_owner IS NOT NULL THEN t2.station_owner ELSE t1.stationID END AS stationID
,observation_date
,CONCAT(DATEPART(year, observation_date),'-',DATEPART(month, observation_date)) AS observation_month
,SUM(metric_precipitationDailyTotal) monthly_rainfall_total 
FROM weather.daily_weather_metrics t1
JOIN weather.DIM_weatherstation_details t2 ON t1.stationID = t2.station_id
WHERE FORMAT(observation_date, 'yyyy') = FORMAT(CURRENT_TIMESTAMP, 'yyyy')
GROUP BY CASE WHEN t2.station_owner IS NOT NULL THEN t2.station_owner ELSE t1.stationID END
,observation_date
,CONCAT(DATEPART(year, observation_date),'-',DATEPART(month, observation_date))
"""

monthly_rain_bar_df = read_from_db(bar_sql_stmt)

# Create list of station ID's
station_list = [i for i in monthly_rain_line_df['stationID'].unique()]

# Add the 'All' values to the list of station
station_list.append('All')

station_list.sort()

layout = html.Div([

    html.H1('YTD Total Daily Rain Amount'),

    html.Div([
        html.Div(dcc.Dropdown(
            id='mr_station_ID',
            clearable=False,
            value='All',
            options=[{'label': i, 'value': i} for i in station_list],
            ),
        )
    ],className='row'),
    dcc.Graph(id='monthly_rain_line'),
    dcc.Graph(id='monthly_rain_bar'),

    dcc.Interval(
        id='mr_1-minute-interval',
        interval=60000 #60 seconds, 1 minutes
    )
])

# set up callback function
@callback(
    Output(component_id='monthly_rain_line', component_property='figure'),
    Output(component_id='monthly_rain_bar', component_property='figure'),
    Input(component_id='mr_station_ID', component_property='value')
)

def filtered_daily_rain(selected_stationID='All'):
    monthly_rain_line_df = read_from_db(line_sql_stmt)
    monthly_rain_bar_df = read_from_db(bar_sql_stmt)
    if selected_stationID == 'All':
        filtered_monthly_rain_line_df = monthly_rain_line_df
        filtered_monthly_rain_bar_df = monthly_rain_bar_df
        
    else:
        filtered_monthly_rain_line_df = monthly_rain_line_df[monthly_rain_line_df['stationID'] == selected_stationID]
        filtered_monthly_rain_bar_df = monthly_rain_bar_df[monthly_rain_bar_df['stationID'] == selected_stationID]

    filtered_monthly_rain_line_df = filtered_monthly_rain_line_df.sort_values(by=['observation_month','stationID'])    


    filtered_monthly_rain_bar_df = filtered_monthly_rain_bar_df.sort_values(by=['observation_month','stationID'])    

    line_fig = px.line(data_frame=filtered_monthly_rain_line_df,
                       x='observation_month',
                       y='YTD_rainfall',
                       title=f'Monthly Total Rainfall: Line: {selected_stationID}',
                       color='stationID',
                       labels={
                           'observation_month' : 'month',
                           'monthly_running_rainfall_total': 'Total Rainfall (mm)'
                       }
                    )
    
    bar_fig = px.bar(data_frame=filtered_monthly_rain_bar_df,
                       x='stationID',
                       y='monthly_rainfall_total',
                       title=f'Monthly Total Rainfall: Bar: {selected_stationID}',
                       color='observation_month',
                       labels={
                           'stationID': 'station ID',
                           'ytd_rainfall_total    ': 'Total Rainfall (mm)'
                       }
                    )
    return line_fig, bar_fig