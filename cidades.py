import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime
import pandas as pd
from dash.dependencies import Input, Output
from app import app
from brasil import percentage

#Dadaset Cidades
cities_time = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv')
only_cities = cities_time.city != 'TOTAL'     
cities_time = cities_time[only_cities]
not_zero = cities_time.newCases > 0
cities_time = cities_time[not_zero]

cities_list = cities_time.city
cities_list = list(cities_list.drop_duplicates())
cities_options = []
for i in cities_list:
    cities_options.append({'label':i,'value':i})

card_cidades = dbc.Card(id='card_city')

menu_cidades = dbc.Card([
        dbc.CardHeader('Cidade'),
        dbc.CardBody(
            dcc.Dropdown(
                id='dropdown_cities',
                options=cities_options,
                value='São Paulo/SP'
            ),
        )
    ])     

page_cidades = html.Div(children=[

    dcc.Tabs(id='tabs_cidades',value='Total de casos',children=[
        dcc.Tab(label='Total de casos',value='Total de casos'),
        dcc.Tab(label='Novos casos',value='Novos casos'),
        dcc.Tab(label='Casos Fatais',value='Óbitos')
    ]),

    dbc.Card(
        dcc.Graph(id='graph_cities'),
    )

])

@app.callback(
    [Output('graph_cities','figure'),
    Output('card_city','children')],
    [Input('dropdown_cities','value'),
    Input('tabs_cidades','value')]
)
def update_graph_city(cidade,filtro):
    city_time = cities_time[cities_time.city == cidade] 
    x = city_time.date
    if filtro == 'Total de casos':
        y = city_time.totalCases
    elif filtro == 'Novos casos':
        y = city_time.newCases
    elif filtro == 'Óbitos':
        y = city_time.deaths             

    figure = {
        'data': [
            {'x': x, 'y': y, 'type': 'line'},
        ],
        'layout': {
                'title':filtro +' em '+cidade
            }
    }

    date = datetime.datetime.strptime(city_time.date.iloc[-1], '%Y-%m-%d').strftime('%d/%m/%y')
    children = [dbc.CardHeader(
                    html.H5(['Data:'+date],
                        style={'color': '#666666'}            
                    )
                ),
                dbc.CardBody([
                    html.H5([f'Total de casos:{city_time.totalCases.iloc[-1]} {percentage(city_time.totalCases.iloc[-1],city_time.totalCases.iloc[-2])}'],
                        style={'color': '#666666'}),
                    html.H6([f'Novos casos:{city_time.newCases.iloc[-1]} {percentage(city_time.newCases.iloc[-1],city_time.newCases.iloc[-2])}'],
                        style={'color': '#666666'}),
                    html.H6([f'Casos fatais:{city_time.deaths.iloc[-1]} {percentage(city_time.deaths.iloc[-1],city_time.deaths.iloc[-2])}'],
                        style={'color': '#666666'})                        
                ])
                ] 
    return figure,children