import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
from app import app

#Dadaset Estados
states_time = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv')
only_states = states_time.state != 'TOTAL'
states_time = states_time[only_states]


states_list = states_time.state
states_list = list(states_list.drop_duplicates())
states_options = []
for i in states_list:
    states_options.append({'label':i,'value':i})

card_estados =  dbc.Card(id='card_state')  
#Layout    
page_estados =  html.Div(children=[

    dcc.Tabs(id='tabs',value='Total de casos',children=[
        dcc.Tab(label='Total de casos',value='Total de casos'),
        dcc.Tab(label='Novos casos',value='Novos casos')
    ]),

    html.Div([
        dcc.Dropdown(
            id='dropdown_states',
            options=states_options,
            value='SP'
        ),
    ]),  

    html.Div([
    dcc.Graph(id='graph_states'),
    ])
])

@app.callback(
    [Output('graph_states','figure'),
    Output('card_state','children')],
    [Input('dropdown_states','value'),
    Input('tabs','value')]
)
def update_graph_state(estado,filtro):
    state_time = states_time[states_time.state == estado] 
    x = state_time.date
    if filtro == 'Total de casos':
        y = state_time.totalCases
    elif filtro == 'Novos casos':
        y = state_time.newCases

    figure = {
        'data': [
            {'x': x, 'y': y, 'type': 'line'},
        ],
        'layout': {
                'title':filtro+' em '+estado
            }
    }

    children = [dbc.CardHeader(state_time.date.iloc[-1]),
                dbc.CardBody('Total de casos:{}\nNovos casos:{}'.format(state_time.totalCases.iloc[-1],
                state_time.newCases.iloc[-1]))]
    
    return figure,children


