import dash
# Create Dash app

application = dash.Dash(__name__, suppress_callback_exceptions=True)
server = application.server

