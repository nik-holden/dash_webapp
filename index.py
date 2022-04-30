from app import dash_app as app
#from app import app as server
from dash import html, dcc

server = app.server
print('from app import ', callable(app))
print('server ', callable(server))

app.layout = html.Div([
    
    html.H1(['Hello'])
        ])

# Run local app
if __name__ == '__main__':
    
    app.run_server(debug=False)

