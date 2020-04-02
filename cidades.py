import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from app import app

#Dadaset Cidades
cities_time = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv')
only_cities = cities_time.city != 'TOTAL'    
cities_time = cities_time[only_cities]

cities_list = cities_time.city
cities_list = list(cities_list.drop_duplicates())
cities_options = []
for i in cities_list:
    cities_options.append({'label':i,'value':i})

page_cidades = html.Div(children=[
    #Casos Cidades
    dcc.Graph(id='graph_cities'),

    dcc.Dropdown(
        id='dropdown_cities',
        options=cities_options,
        value='São Paulo/SP'
    ),
])

@app.callback(
    Output('graph_cities','figure'),
    [Input('dropdown_cities','value'),]
)
def update_graph_city(cidade):
    city_time = cities_time[cities_time.city == cidade] 
    x = city_time.date
    y = city_time.totalCases
    return {
        'data': [
            {'x': x, 'y': y, 'type': 'line', 'name': 'SF'},
        ],
        'layout': {
            'title': 'Casos confirmados em ' + cidade
            }
    }