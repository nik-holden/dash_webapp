import dash
from dash import Dash, html

dash_app = Dash(__name__)

app = dash_app.server

print('from app import ', callable(dash_app))
print('server ', callable(app))

dash_app.layout = html.Div([
    
    html.H1([''])
        ])