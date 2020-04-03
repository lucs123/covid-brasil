import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
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

card_cidades = dbc.Card(id='card_city') 

page_cidades = html.Div(children=[

    dcc.Tabs(id='tabs',value='Total de casos',children=[
        dcc.Tab(label='Total de casos',value='Total de casos'),
        dcc.Tab(label='Novos casos',value='Novos casos')
    ]),

    dcc.Graph(id='graph_cities'),

    dcc.Dropdown(
        id='dropdown_cities',
        options=cities_options,
        value='São Paulo/SP'
    ),
])

@app.callback(
    [Output('graph_cities','figure'),
    Output('card_city','children')],
    [Input('dropdown_cities','value'),
    Input('tabs','value')]
)
def update_graph_city(cidade,filtro):
    city_time = cities_time[cities_time.city == cidade] 
    x = city_time.date
    if filtro == 'Total de casos':
        y = city_time.totalCases
    elif filtro == 'Novos casos':
        y = city_time.newCases

    figure = {
        'data': [
            {'x': x, 'y': y, 'type': 'line'},
        ],
        'layout': {
                'title':filtro +' em '+cidade
            }
    }

    children = [dbc.CardHeader(city_time.date.iloc[-1]),
                dbc.CardBody('Total de casos:{}\nNovos casos:{}'.format(city_time.totalCases.iloc[-1],
                city_time.newCases.iloc[-2]))]  
    return figure,children