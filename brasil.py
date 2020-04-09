import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime
import pandas as pd
from dash.dependencies import Input, Output
from app import app

def percentage(today,yesterday):
    if today > yesterday:
        return '{:+.2%}'.format(today/yesterday-1)
    elif today < yesterday:
        return '{:.2%}'.format(today/yesterday-1)
    else:
        return ''        

#Dadaset Brasil
br = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv')
br = br[br.state == 'TOTAL']

card_brasil = dbc.Card(id='card_brasil') 

page_brasil = html.Div(children=[

    dcc.Tabs(id='tabs_brasil',value='Total de casos',children=[
        dcc.Tab(label='Total de casos',value='Total de casos'),
        dcc.Tab(label='Novos casos',value='Novos casos'),
        dcc.Tab(label='Casos Fatais',value='Óbitos')
    ]),

    #Casos Brasil
    dbc.Card(
        dcc.Graph(id='graph_brasil')
    )
])

@app.callback(
    [Output('graph_brasil','figure'),
    Output('card_brasil','children')],
    [Input('tabs_brasil','value')]
)
def update_graph_brasil(filtro):
    x = br.date
    if filtro == 'Total de casos':
        y = br.totalCases
    elif filtro == 'Novos casos':
        y = br.newCases
    elif filtro == 'Óbitos':
        y = br.deaths        
    figure = {
        'data': [
            {'x': x, 'y': y, 'type': 'line'},
        ],
        'layout': {
                'title':filtro,
            }
    }

    date = datetime.datetime.strptime(br.date.iloc[-1], '%Y-%m-%d').strftime('%d/%m/%y')
    children = [dbc.CardHeader(
                    html.H5(['Data:'+date],
                        style={'color': '#666666'}            
                    )
                ),
                dbc.CardBody([
                    html.H5([f'Total de casos:{br.totalCases.iloc[-1]} {percentage(br.totalCases.iloc[-1],br.totalCases.iloc[-2])}'],
                        style={'color': '#666666'}),
                    html.H6([f'Novos casos:{br.newCases.iloc[-1]} {percentage(br.newCases.iloc[-1],br.newCases.iloc[-2])}'],
                        style={'color': '#666666'}),
                    html.H6([f'Casos fatais:{br.deaths.iloc[-1]} {percentage(br.deaths.iloc[-1],br.deaths.iloc[-2])}'],
                        style={'color': '#666666'})                        
                ])
                ]      
    return figure,children

