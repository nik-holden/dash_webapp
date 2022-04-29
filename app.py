import dash 
from dash import html, dcc

app = dash.Dash()

# server = app.server

app.layout = html.Div([
    
    html.H1(['Hello'])
        ])

# Run local app
if __name__ == '__main__':
    
    app.run_server(debug=False)

