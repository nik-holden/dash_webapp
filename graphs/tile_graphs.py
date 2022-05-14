from dash import html, Dash
import dash_bootstrap_components as dbc

from graphs import line_monthly_rainfall
from graphs import line_current_day_temp
from graphs import line_daily_temp 

#app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = html.Div([

    dbc.Row([
            dbc.Col(html.Div(line_monthly_rainfall.layout), width='600'),
            dbc.Col(html.Div(line_current_day_temp.layout), width='auto'),
    ]),
    dbc.Row([
            dbc.Col(html.Div(line_daily_temp.layout), width='auto'),
            dbc.Col(html.Div("tile 4"), width='auto'),
    ])
])

#if __name__ == "__main__":
#    app.run_server()