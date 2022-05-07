import dash 
import dash.html as html
import dash.dcc as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from graphs import line_monthly_rainfall
from graphs import line_current_day_temp
from graphs import line_daily_temp
#from graphs import tile_graphs

app_ = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app = app_.server
print('app_ ', callable(app_))
print('app ', callable(app))

app_.layout = html.Div([ 
    dcc.Location(id='url', refresh=False),
    html.Div([
        #dcc.Link('Multiple Graphs', href='/dash_app_s/tile_graphs'),
        dcc.Link('Total Monthly Rainfall', href='/dash_app_s/line_monthly_rainfall'),
        dcc.Link('Current Day Temperature', href='/dash_app_s/line_current_day_temp'),
        dcc.Link('Daily high-low Temperatures', href='/dash_app_s/line_daily_temp')
    ], className="row"),
    html.Div(id='page_content', children=[])
])

@app_.callback(
    Output(component_id='page_content', component_property='children'),
    Input(component_id='url', component_property='pathname')
)

def display_page(pathname):
    if pathname == '/dash_app_s/line_monthly_rainfall':
        return line_monthly_rainfall.layout
    elif pathname == '/dash_app_s/line_current_day_temp':
        return line_current_day_temp.layout
    elif pathname == '/dash_app_s/line_daily_temp':
        return line_daily_temp.layout
    #elif pathname == '/dash_app_s/tile_graphs':
    #    return tile_graphs.layout
    else:
        return line_monthly_rainfall.layout 
# Run local app_
if __name__ == '__main__':
    
    app_.run_server(debug=False)

