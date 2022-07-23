import requests
import pandas as pd
import dash_daq as daq
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import dash
import dash_bootstrap_components as dbc

#from common_functions import read_from_db


app_ = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app = app_.server

# PSW
base_url = 'https://api.weather.com/v2/pws/observations'
period = 'current'
format = 'json'
units = 'm'
apiKey = '2af8653072354d19b8653072358d194f'

personal_weather_station = {
    'stationId': ['IAUKHIGH2', 'INEWPL81', 'IUPPER72', 'IKATIKAT9', 
     'ICLYDE9', 'IWGNLYAL3', 'IKATIK3', 'IALEXA39']}


def station_url(base_url, period, stationId, format, units, apiKey):
    url = f'{base_url}/{period}?stationId={stationId}&format={format}&units={units}&apiKey={apiKey}'

    return url

def json_to_pandas_dataframe(weather_observation_data):
    data = pd.DataFrame(list(weather_observation_data.items()),columns = ['stationId', 'temp'])

    return data
    
def get_weather_station_observations(url):
    
    response = requests.get(url)
 
    json_payload = response.json()

    weather_observation = json_payload['observations'][0]['metric']['temp']


    return weather_observation

def weather_stations():

    weather_station_list = personal_weather_station.get('stationId')

    return weather_station_list

def weather_obs():
    weather_station_list = weather_stations()

    station_current_temps_dict = {}
    for weather_station in weather_station_list:
        url = station_url(base_url,
                          period,
                          weather_station,
                          format,
                          units,
                          apiKey)
        
        #  A try/except block has been added due to a weather station going no longer being reachable and causing the job to fail
        try:
            
            station_current_temps_dict[weather_station] = get_weather_station_observations(url)
        
        except Exception as e:
            print('an error occurred: ', e)

    
    #data = json_to_pandas_dataframe(station_current_temps_dict)

    data = station_current_temps_dict

    return  data


current_temps_df = weather_obs()
station_list = weather_stations()
# Add the 'All' values to the list of station
#station_list.append('All')

station_list.sort()

#value = 10

app_.layout = html.Div([

    html.H1('Current Temperature'),

    html.Div([
        html.Div(dcc.Dropdown(
            id='ct_station_ID',
            clearable=False,
            value='INEWPL81',
            options=[{'label': i, 'value': i} for i in station_list],
            ),
        )
    ],className='row'),
    daq.Thermometer(id='current_temp',
    value=0,
    label = 'Current Temperature',
    color='red',
    min=-10,
    max=45,
    style={
        'margin-bottom': '5%'
    }),
    dcc.Interval(
        id='dr_1-minute-interval',
        interval=60000 #60 seconds, 1 minutes
    )
])

# set up callback function
@callback(
    Output(component_id='current_temp', component_property='value'),
    Input(component_id='ct_station_ID', component_property='value')
)

def update_thermostat(selected_stationID='INEWPL81'):
    v = current_temps_df[selected_stationID]
    print(selected_stationID, v)
    temp = v
    
    return temp


if __name__ == '__main__':

   #weather_obs()
    app_.run_server(debug=False)