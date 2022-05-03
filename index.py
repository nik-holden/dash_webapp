#from app import dash_app as app
#from app import app as server
from dash import html, dcc, Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from graphs import line_monthly_rainfall
from graphs import line_current_day_temp
from graphs import line_daily_temp
from graphs import tile_graphs

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server
print('app ', callable(app))
print('server ', callable(server))

app.layout = html.Div([ 
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Multiple Graphs', href='/dash_apps/tile_graphs'),
        dcc.Link('Total Monthly Rainfall', href='/dash_apps/line_monthly_rainfall'),
        dcc.Link('Current Day Temperature', href='/dash_apps/line_current_day_temp'),
        dcc.Link('Daily high-low Temperatures', href='/dash_apps/line_daily_temp')
    ], className="row"),
    html.Div(id='page_content', children=[])
])

@app.callback(
    Output(component_id='page_content', component_property='children'),
    Input(component_id='url', component_property='pathname')
)

def display_page(pathname):
    if pathname == '/dash_apps/line_monthly_rainfall':
        return line_monthly_rainfall.layout
    elif pathname == '/dash_apps/line_current_day_temp':
        return line_current_day_temp.layout
    elif pathname == '/dash_apps/line_daily_temp':
        return line_daily_temp.layout
    elif pathname == '/dash_apps/tile_graphs':
        return tile_graphs.layout
    else:
        return line_monthly_rainfall.layout 
# Run local app
if __name__ == '__main__':
    
    app.run_server(debug=False)

