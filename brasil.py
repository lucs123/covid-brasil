import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from app import app

#Dadaset Brasil
br = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv')
br = br[br.state == 'TOTAL']


page_brasil = html.Div(children=[

    #Casos Brasil
    dcc.Graph(id='graph_brasil',
        figure = {
        'data': [
            {'x': br.date, 'y': br.totalCases, 'type': 'line', 'name': 'SF'},
        ],
        'layout': {
            'title': 'Casos confirmados Brasil'
            }}),
])            