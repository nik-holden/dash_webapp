from dash import html, dcc, callback, Input, Output
import plotly.express as px

from common_functions import read_from_db


sql_stmt = """
WITH cte_a AS (SELECT 
CASE WHEN t2.station_owner IS NOT NULL THEN t2.station_owner ELSE t1.stationID END AS stationID, 
observation_date, 
observation_hour,
max(metric_precipitationTotal) as total_rain_fall
FROM [weather].[raw_observations]t1
JOIN weather.DIM_weatherstation_details t2 ON t1.stationID = t2.station_id
WHERE current_date_flag = 1
GROUP BY stationID, 
observation_date, 
observation_hour,
CASE WHEN t2.station_owner IS NOT NULL THEN t2.station_owner ELSE t1.stationID END
)


select 
stationID, 
observation_date, 
observation_hour,
CASE
	WHEN total_rain_fall  - lag(total_rain_fall) OVER (PARTITION BY stationID ORDER BY observation_hour) > 0
	THEN ISNULL(total_rain_fall  - lag(total_rain_fall) OVER (PARTITION BY stationID ORDER BY observation_hour), 0) 
	ELSE total_rain_fall
END AS hourly_rain_fall
FROM cte_a
"""

#daily_rain_df = pd.read_sql(sql_stmt, conn)
hourly_rain_df = read_from_db(sql_stmt)

# Create list of station ID's
station_list = [i for i in hourly_rain_df['stationID'].unique()]

# Add the 'All' values to the list of station
station_list.append('All')

station_list.sort()

layout = html.Div([

    html.H1('Hourly Rain Fall.'),

    html.Div([
        html.Div(dcc.Dropdown(
            id='hr_station_ID',
            clearable=False,
            value='All',
            options=[{'label': i, 'value': i} for i in station_list],
            ),
        )
    ],className='row'),
    dcc.Graph(id='hourly_rain'),
    dcc.Interval(
        id='dr_1-minute-interval',
        interval=60000 #60 seconds, 1 minutes
    )
])

# set up callback function
@callback(
    Output(component_id='hourly_rain', component_property='figure'),
    Input(component_id='hr_station_ID', component_property='value')
)

def filtered_single_day_rain(selected_stationID='All'):
    if selected_stationID == 'All':
        filtered_daily_rain_df = hourly_rain_df
    else:
        filtered_daily_rain_df = hourly_rain_df[hourly_rain_df['stationID'] == selected_stationID]

    bar_fig = px.bar(data_frame=filtered_daily_rain_df,
                       x='stationID',
                       y='hourly_rain_fall',
                       title=f'Current Days Hourly Rainfall: {selected_stationID}',
                       color='observation_hour'
                    )
    return bar_fig