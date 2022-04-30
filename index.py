from app import dash_app, app
from dash import html, dcc

print('dash_app ', callable(dash_app))
print('app ', callable(app))

app.layout = html.Div([
    
    html.H1(['Hello'])
        ])

# Run local app
if __name__ == '__main__':
    
    dash_app.run_server(debug=False)

