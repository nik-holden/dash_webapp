from app import dash_app as app
from app import app as server
from dash import html, dcc
from dash.dependencies import Input, Output

from graphs import line_monthly_rainfall

#server = app.server
print('from app import ', callable(app))
print('server ', callable(server))

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Total Monthly Rainfall', href='/dash_apps/line_monthly_rainfall')
    ], className="row"),
    html.Div(id='page_content', children=[])
])

@app.callback(
    Output(component_id='page_content', component_property='children'),
    Input(component_id='url', component_property='pathname')
)

def display_page(pathname):
    if pathname == '/apps/line_monthly_rainfall':
        return line_monthly_rainfall.layout
    else:
        return line_monthly_rainfall.layout
# Run local app
if __name__ == '__main__':
    
    app.run_server(debug=False)

