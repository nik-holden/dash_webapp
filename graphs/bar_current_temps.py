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
apiKey = '41c4bcd2fc984f7f84bcd2fc981f7f81'

personal_weather_station = {
    'stationId': ['IAUKHIGH2', 'INEWPL81', 'IUPPER72']} #, 'IKATIKAT9', 
     #'ICLYDE9', 'IWGNLYAL3', 'IKATIK3', 'IALEXA39']}

station_id = ['IAUKHIGH2', 'INEWPL81', 'IUPPER72', 'IKATIKAT9', 'ICLYDE9', 'IWGNLYAL3', 'IKATIK3', 'IALEXA39']


def station_url(stationId, base_url=base_url, period=period, format='json', units=units, apiKey=apiKey):
    url = f'{base_url}/{period}?stationId={stationId}&format={format}&units={units}&apiKey={apiKey}'

    return url

    
def get_weather_station_observations(url):
    
    print(url)
    
    response = requests.get(url)

    print(response.status_code)

    if response.status_code == 200:
        json_payload = response.json()

        temp = json_payload['observations'][0]['metric']['temp']

        return temp

    else:
        return 0
    

def get_current_temp(station):
    url = station_url(station)
    temp = get_weather_station_observations(url)

    #temp = observtions['temp']

    return temp

def get_layout(station):

    temp = get_current_temp(station)

    layout = html.Td([dbc.Col([daq.Thermometer(id=f'thermometer_{station}',
        label=station,
        showCurrentValue=True,
        units="C",
        color=get_thermometer_colour(temp),
        value=temp,
        min=0,
        max=40,
        style={
        'margin-bottom': '5%'
        }
    )])])

    return layout


def get_thermometer_colour(temp):
    if temp <9:
        colour = 'Blue'
    elif temp <19:
        colour = 'Orange'

    else:
        colour = 'Red'

    return colour


def main():
    
    app_.layout = html.Div([
        html.H4([
            'Current Temperature'
        ]),
        html.Table(style={'width':'100%'}, children=[
            html.Tbody([
                html.Tr([
                    get_layout(i) for i in station_id        
                ])
            ])

    ])        
        ])
    
    app_.run_server(debug=False)


if __name__ == '__main__':

   #weather_obs()

   main()
    
    