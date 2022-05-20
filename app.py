import dash 
import dash.html as html
import dash.dcc as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from graphs import line_monthly_rainfall, line_current_day_temp, line_daily_temp, bar_day_rainfall, line_daily_temp_2_gphs, stacked_bar_day_rainfall_hr, box_whisker_daily_temp

#from graphs import tile_graphs

app_ = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app = app_.server

app_.layout = html.Div([ 
    dcc.Location(id='url', refresh=False),
    html.Div([
        #dcc.Link('Multiple Graphs', href='/dash_app_s/tile_graphs'),
        dcc.Link('Total Monthly Rainfall', href='/dash_app_s/line_monthly_rainfall'),
        dcc.Link('Daily Rainfall', href='/dash_app_s/bar_day_rainfall'),
        dcc.Link('Hourly Rainfall', href='/dash_app_s/stacked_bar_day_rainfall_hr'),
        dcc.Link('Current Day Temperature', href='/dash_app_s/line_current_day_temp'),
        dcc.Link('Daily high-low Temperatures', href='/dash_app_s/line_daily_temp'),
        dcc.Link('Min - Max Temperature Graphs', href='/dash_app_s/line_daily_temp_2_gphs'),
        dcc.Link('Temperature Range', href='/dash_app_s/box_whisker_daily_temp'),
        #dcc.Link('Temperature Range Graphs', href='/dash_app_s/box_daily_temp')
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
    elif pathname == '/dash_app_s/bar_day_rainfall':
        return bar_day_rainfall.layout
    elif pathname == '/dash_app_s/line_daily_temp_2_gphs':
        return line_daily_temp_2_gphs.layout
    elif pathname == '/dash_app_s/stacked_bar_day_rainfall_hr':
        return stacked_bar_day_rainfall_hr.layout
    elif pathname == '/dash_app_s/box_whisker_daily_temp':
        return box_whisker_daily_temp.layout
    else:
        return line_monthly_rainfall.layout


# Run local app_
if __name__ == '__main__':
    
    app_.run_server(debug=False)

