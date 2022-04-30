import dash
from dash import Dash, html

dash_app = Dash(__name__)

app = dash_app.server

dash_app.layout = html.Div([
    
    html.H1(['Hello'])
        ])