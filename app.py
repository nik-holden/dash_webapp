from dash import Dash
from dash import html

app = Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1('Hello')
])

if __name__ == '__main__':
    app.run_server(debug=False)