import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from app import app

#Dadaset Brasil
br = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv')
br = br[br.state == 'TOTAL']


page_brasil = html.Div(children=[

    dcc.Tabs(id='tabs',value='Total de casos',children=[
        dcc.Tab(label='Total de casos',value='Total de casos'),
        dcc.Tab(label='Novos casos',value='Novos casos')
    ]),

    #Casos Brasil
    dcc.Graph(id='graph_brasil')
])

@app.callback(
    Output('graph_brasil','figure'),
    [Input('tabs','value')]
)
def update_graph_brasil(filtro):
    x = br.date
    if filtro == 'Total de casos':
        y = br.totalCases
    elif filtro == 'Novos casos':
        y = br.newCases
    return {
        'data': [
            {'x': x, 'y': y, 'type': 'line'},
        ],
        'layout': {
                'title':filtro
            }
    }
    