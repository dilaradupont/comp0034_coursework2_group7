import dash
import dash_bootstrap_components as dbc

# Code from https://dash.plotly.com/urls
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server
