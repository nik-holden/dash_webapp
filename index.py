from .app import app
from .app import dash_app

from dash import html

dash_app.layout = html.Div([
    html.H1('Hello')
])

if __name__ == '__main__':
    dash_app.run_server(debug=False)