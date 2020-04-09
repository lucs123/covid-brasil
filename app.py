import dash
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
app.title = 'Covid Brasil'
server = app.server
app.config.suppress_callback_exceptions = True