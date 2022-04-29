from dash import Dash, html, dcc, Input, Output, callback

#from graphs import line_monthly_rainfall

app = Dash(__name__, suppress_callback_exceptions=True)

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1([
        dcc.Link('Total Monthly Rainfall', href='/dash_apps/line_monthly_rainfall')
    ], className="row"),
    html.Div(id='page_content', children=[])
])

@callback(
    Output(component_id='page_content', component_property='children'),
    Input(component_id='url', component_property='pathname')
)

def display_page(pathname):
    if pathname == '/dash_apps/line_monthly_rainfall':
        return line_monthly_rainfall.layout
    else:
        return print('line_monthly_rainfall.layout')

# Run local app
if __name__ == '__main__':
    
    app.run_server(debug=False)

