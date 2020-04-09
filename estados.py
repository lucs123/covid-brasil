import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime
import pandas as pd
from dash.dependencies import Input, Output
from app import app
from brasil import percentage

#Dadaset Estados
states_time = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv')
only_states = states_time.state != 'TOTAL'
states_time = states_time[only_states]
not_zero = states_time.newCases > 0
states_time = states_time[not_zero]


states_list = states_time.state
states_list = list(states_list.drop_duplicates())
states_options = []
for i in states_list:
    states_options.append({'label':i,'value':i})

card_estados =  dbc.Card(id='card_state')

menu_estados = dbc.Card([
        dbc.CardHeader('Estado'),
        dbc.CardBody(
            dcc.Dropdown(
                id='dropdown_states',
                options=states_options,
                value='SP'
            ),
        )
    ])        

#Layout    
page_estados =  html.Div(children=[

    dcc.Tabs(id='tabs_estados',value='Total de casos',children=[
        dcc.Tab(label='Total de casos',value='Total de casos'),
        dcc.Tab(label='Novos casos',value='Novos casos'),
        dcc.Tab(label='Casos Fatais',value='Óbitos')
    ]), 

    dbc.Card([
        dcc.Graph(id='graph_states'),
    ])
])

@app.callback(
    [Output('graph_states','figure'),
    Output('card_state','children')],
    [Input('dropdown_states','value'),
    Input('tabs_estados','value')]
)
def update_graph_state(estado,filtro):
    state_time = states_time[states_time.state == estado] 
    x = state_time.date
    if filtro == 'Total de casos':
        y = state_time.totalCases
    elif filtro == 'Novos casos':
        y = state_time.newCases
    elif filtro == 'Óbitos':
        y = state_time.deaths  
    figure = {
        'data': [
            {'x': x, 'y': y, 'type': 'line'},
        ],
        'layout': {
                'title':filtro+' em '+estado
            }
    }

    date = datetime.datetime.strptime(state_time.date.iloc[-1], '%Y-%m-%d').strftime('%d/%m/%y')
    children = [dbc.CardHeader(
                    html.H5(['Data:'+date],
                        style={'color': '#666666'}            
                    )
                ),
                dbc.CardBody([
                    html.H5([f'Total de casos:{state_time.totalCases.iloc[-1]} {percentage(state_time.totalCases.iloc[-1],state_time.totalCases.iloc[-2])}'],
                        style={'color': '#666666'}),
                    html.H6([f'Novos casos:{state_time.newCases.iloc[-1]} {percentage(state_time.newCases.iloc[-1],state_time.newCases.iloc[-2])}'],
                        style={'color': '#666666'}),
                    html.H6([f'Casos fatais:{state_time.deaths.iloc[-1]} {percentage(state_time.deaths.iloc[-1],state_time.deaths.iloc[-2])}'],
                        style={'color': '#666666'})                        
                ])
                ] 
    
    return figure,children


