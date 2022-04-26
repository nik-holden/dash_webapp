from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

import common_functions as cf
from app import dash_app

sql_stmt = """
SELECT *
, SUM(metric_precipitationDailyTotal) over(partition by stationID order by observation_date) as running_rainfall_total 
FROM weather.daily_weather_metrics WHERE current_month_flag = 1"""

#daily_rain_df = pd.read_sql(sql_stmt, conn)
daily_rain_df = cf.read_from_db(sql_stmt)

# Create list of station ID's
station_list = [i for i in daily_rain_df['stationID'].unique()]

# Add the 'All' values to the list of station
station_list.append('All')

station_list.sort()

layout = html.Div(children=[

    html.H1('Monthly Total Daily Rain Amount'),

    html.Div([
        html.Div(dcc.Dropdown(
            id='station_ID',
            clearable=False,
            value='All',
            options=[{'label': i, 'value': i} for i in station_list],
            ),
        )
    ],className='row'),
    dcc.Graph(id='total_daily_rain'),
])

# set up callback function
@dash_app.callback(
    Output(component_id='total_daily_rain', component_property='figure'),
    Input(component_id='station_ID', component_property='value')
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
                       width=1200, height=600)

    return line_fig

