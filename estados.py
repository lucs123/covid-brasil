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

page_estados =  html.Div(children=[   
    #Casos Estados
    dcc.Graph(id='graph_states'),

    dcc.Dropdown(
        id='dropdown_states',
        options=states_options,
        value='SP'
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
