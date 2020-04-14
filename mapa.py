import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


gps_df = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/gps_cities.csv')
df_br = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-total.csv')
cities_cases = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities.csv')
cities_cases = cities_cases.rename(columns={'city':'id'})
df_br = df_br.rename(columns={'state':'id'})
result = cities_cases.append(df_br)
result = pd.merge(result,gps_df,on='id')
result = result[result.totalCases > 0]
result = result.rename(columns={'totalCases':'Confirmados','deaths':'Mortes'})

df_table = df_br.drop(columns=['totalCasesMS','deathsMS','country','URL','notConfirmedByMS'])
df_table = df_table.rename(columns={'id':'Local','totalCases':'Total','deaths':'Fatais'})
trace_size = result.Confirmados*100

fig = go.Figure(go.Scattermapbox(
    lat=result.lat, 
    lon=result.lon, 
    mode='markers',
    marker=go.scattermapbox.Marker(
            sizemode='area',
            size=result.Confirmados,
            sizeref=2
        ),
        
    text=result.id,
    customdata=result.Mortes,
    hovertemplate="<b>%{text}</b><br><br>" +
        "Confirmados: %{marker.size}<br>" +
        "Óbitos: %{customdata}<br>" +
        "<extra></extra>",   
    ))
fig.update_layout(mapbox=dict(
    center=go.layout.mapbox.Center(
            lat=-15,
            lon=-47
        ),
        zoom=3,
        ))                            
fig.update_layout(mapbox_style="carto-positron")
     
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

map_layout = html.Div(children=[
    dbc.Card([
        dbc.Row([
            html.Br(),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('MAPA'),
                    dbc.CardBody(dbc.Col([dcc.Graph(figure=fig)])),
                ])],md=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('CASOS'),
                    dbc.CardBody([
                        html.H5([f'Total de casos:{df_br.totalCases.iloc[0]}'],
                            style={'color': '#666666'}),
                        html.H6([f'Casos fatais:{df_br.deaths.iloc[0]}'],
                            style={'color': '#666666'})                        
                ]),
                ]),
                html.Br(),
                dbc.Card(
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in df_table.columns],
                        data=df_table.to_dict('records'),
                        style_table={
                            'maxHeight': '500px',
                            'overflowY': 'scroll'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }
                        ],
                        style_cell={'textAlign': 'center'},
                    )
                )      
            ]),
            html.Br()
        ],justify='around')    
    ])
])



