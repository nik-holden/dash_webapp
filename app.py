from dash import html, Dash

dash_app = Dash(__name__)

app = dash_app.server

print('dash_app ', callable(dash_app))
print('app ', callable(app))

dash_app.layout = html.Div([
    
    html.H1(['Hello'])
        ])

# Run local app
if __name__ == '__main__':
    
    dash_app.run_server(debug=False)

