from dash import Dash, html, dcc, Input, Output, callback

#from graphs import line_monthly_rainfall

app = Dash(__name__)

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1(['Hello'])
        ])

# Run local app
if __name__ == '__main__':
    
    app.run_server(debug=False)

