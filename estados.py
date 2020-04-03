import dash_core_components as dcc
import dash_html_components as html
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

#Layout    
page_estados =  html.Div(children=[

    dcc.Tabs(id='tabs',value='Total de casos',children=[
        dcc.Tab(label='Total de casos',value='Total de casos'),
        dcc.Tab(label='Novos casos',value='Novos casos')
    ]),

    dcc.Graph(id='graph_states'),

    dcc.Dropdown(
        id='dropdown_states',
        options=states_options,
        value='SP'
    ),
])

@app.callback(
    Output('graph_states','figure'),
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
         
    return {
        'data': [
            {'x': x, 'y': y, 'type': 'line'},
        ],
        'layout': {
                'title':filtro+' em '+estado
            }
    }
