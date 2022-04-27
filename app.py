import dash
from dash import html

app = dash.Dash()

server = app.server

app.layout = html.Div([
    html.H1('Hello')
])

if __name__ == '__main__':
    app.run_server(debug=False)