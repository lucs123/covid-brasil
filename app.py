import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUX])
app.title = 'Covid Brasil'

app.config.suppress_callback_exceptions = True