from dash import html, dcc, callback, Input, Output
import plotly.express as px

from common_functions import read_from_db


sql_stmt = """
SELECT 
CASE WHEN t2.station_owner IS NOT NULL THEN t2.station_owner ELSE t1.stationID END AS stationID
,observation_date
, SUM(metric_precipitationDailyTotal) over(partition by stationID order by observation_date) as running_rainfall_total 
FROM weather.daily_weather_metrics t1
JOIN weather.DIM_weatherstation_details t2 ON t1.stationID = t2.station_id
WHERE current_month_flag = 1
ORDER BY stationID, observation_date 
"""

#daily_rain_df = pd.read_sql(sql_stmt, conn)
daily_rain_df = read_from_db(sql_stmt)

# Create list of station ID's
station_list = [i for i in daily_rain_df['stationID'].unique()]

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
    dcc.Graph(id='total_daily_rain'),
    dcc.Interval(
        id='mr_1-minute-interval',
        interval=60000 #60 seconds, 1 minutes
    )
])

# set up callback function
@callback(
    Output(component_id='total_daily_rain', component_property='figure'),
    Input(component_id='mr_station_ID', component_property='value')
)

def filtered_daily_rain(selected_stationID='All'):
    if selected_stationID == 'All':
        filtered_daily_rain_df = daily_rain_df
    else:
        filtered_daily_rain_df = daily_rain_df[daily_rain_df['stationID'] == selected_stationID]

    line_fig = px.line(data_frame=filtered_daily_rain_df,
                       x='observation_date',
                       y='running_rainfall_total',
                       title=f'Current Months Daily Total Rainfall: {selected_stationID}',
                       color='stationID',
                       width=700)

    return line_fig