#coding:UTF-8
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

#Dadaset Brasil
br = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv')
br = br[br.state == 'TOTAL']

#Dadaset Estados
states_time = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv')
only_states = states_time.state != 'TOTAL'
states_time = states_time[only_states]

states_list = states_time.state
states_list = list(states_list.drop_duplicates())
states_options = []
for i in states_list:
    states_options.append({'label':i,'value':i})

#Dadaset Cidades
cities_time = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv')
only_cities = cities_time.city != 'TOTAL'    
cities_time = cities_time[only_cities]

cities_list = cities_time.city
cities_list = list(cities_list.drop_duplicates())
cities_options = []
for i in cities_list:
    cities_options.append({'label':i,'value':i})


app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    #Casos Brasil
    dcc.Graph(id='graph_brasil',
        figure = {
        'data': [
            {'x': br.date, 'y': br.totalCases, 'type': 'line', 'name': 'SF'},
        ],
        'layout': {
            'title': 'Casos confirmados Brasil'
            }}),

    #Casos Estados
    dcc.Graph(id='graph_states'),

    dcc.Dropdown(
        id='dropdown_states',
        options=states_options,
        value='SP'
    ),

    #Casos Cidades
    dcc.Graph(id='graph_cities'),

    dcc.Dropdown(
        id='dropdown_cities',
        options=cities_options,
        value='São Paulo/SP'
    ),
])

@app.callback(
    Output('graph_states','figure'),
    [Input('dropdown_states','value'),]
)
def update_graph_state(estado):
    state_time = states_time[states_time.state == estado] 
    x = state_time.date
    y = state_time.totalCases
    return {
        'data': [
            {'x': x, 'y': y, 'type': 'line', 'name': 'SF'},
        ],
        'layout': {
            'title': 'Casos confirmados em ' + estado
            }
    }

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

if __name__ == '__main__':
    app.run_server(debug=True)    