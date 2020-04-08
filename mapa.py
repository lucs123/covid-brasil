import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

gps_df = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/gps_cities.csv')
df_br = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-total.csv')
cities_cases = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities.csv')
cities_cases = cities_cases.rename(columns={'city':'id'})
df_br = df_br.rename(columns={'state':'id'})
result = cities_cases.append(df_br)
result = pd.merge(result,gps_df,on='id')
result = result[result.totalCases > 0]
result = result.rename(columns={'totalCases':'Confirmados','deaths':'Mortes'})


fig = px.scatter_mapbox(result, lat="lat", lon="lon", hover_name="id", hover_data=['Confirmados','Mortes'],
                        size=result.Confirmados,
                        color_discrete_sequence=["fuchsia"], zoom=3, height=600)
fig.update_layout(mapbox_style="carto-darkmatter")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

map_layout = html.Div(children=[
    dbc.Card([
        dbc.CardHeader('MAPA'),
        dbc.CardBody(dbc.Col([dcc.Graph(figure=fig)],md=8)),
    ])
]
)
