import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

from .graphs import line_monthly_rainfall

dash_app = dash.Dash(__name__, suppress_callback_exceptions=True)

app = dash_app.server

dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Total Monthly Rainfall', href='/dash_apps/line_monthly_rainfall')
    ], className="row"),
    html.Div(id='page_content', children=[])
])

@dash_app.callback(
    Output(component_id='page_content', component_property='children'),
    Input(component_id='url', component_property='pathname')
)

def display_page(pathname):
    if pathname == '/dash_apps/line_monthly_rainfall':
        return line_monthly_rainfall.layout
    else:
        return line_monthly_rainfall.layout

# Run local app
if __name__ == '__main__':
    
    dash_app.run_server(debug=False)

