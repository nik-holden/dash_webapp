from dash import html
from dash import dcc
from dash.dependencies import Input, Output

from app import app
from app import server

from apps import line_monthly_rainfall

app.layout = html.Div([
    html.Div([
        dcc.Link('Total Monthly Rainfall', href='/dash_apps/line_monthly_rainfall')
    ], className="row"),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page_content', children=[])
])

@app.callback(
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
    
    app.run_server(debug=True)