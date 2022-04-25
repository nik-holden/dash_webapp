import dash
# Create Dash app

dash_app = dash.Dash(__name__, suppress_callback_exceptions=True)
app = dash_app.server

