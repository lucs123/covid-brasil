#coding:UTF-8
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from brasil import page_brasil,card_brasil
from estados import page_estados,card_estados,menu_estados
from cidades import page_cidades,card_cidades,menu_cidades
from mapa import map_layout
from app import app

links = dbc.Row(children=[
            dbc.Col(dbc.NavLink('Mapa', href='/',style={'color':'#fff'}),md=2),
            dbc.Col(dbc.NavLink('Timeline', href='/timeline',style={'color':'#fff'}),md=3),
            dbc.Col(dbc.NavLink('Código fonte',href="https://github.com/lucs123/covid-brasil",
                style={'color':'#fff'}),md=6)
],)

navbar = dbc.Navbar(children=[
    dbc.Row([
        dbc.Col([dbc.NavbarBrand(children='Covid no Brasil')]),
    ]),
    html.A(className="github-button",href="https://github.com/lucs123/covid-brasil"),
    dbc.NavbarToggler(id="navbar-toggler"),
    dbc.Collapse(links, id="navbar-collapse", navbar=True,style={'justify-content': 'end'}),
], color="dark",dark = True,className='col-md-12')

graph_layout = html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H2('Casos Brasil'),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([html.Div(page_brasil)],md=8),
                        dbc.Col([html.Div(card_brasil)])
                    ]),
                ])    
        ]),
        html.Br(),
        html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H2('Casos por estado'),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([html.Div(page_estados)],md=8),
                        dbc.Col([html.Div(menu_estados),html.Br(),html.Div(card_estados)])

                    ]),
                ])    
            ])
        ]),
        html.Br(),
        html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H2('Casos por cidade'),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([html.Div(page_cidades)],md=8),
                        dbc.Col([html.Div(menu_cidades),html.Br(),html.Div(card_cidades)])
                    ])
                ])    
            ])
        ])    
  ])  

footer = dbc.Row([
    dbc.Col(
        [dcc.Markdown('''
                ### Fonte de dados
                Foram utilizados dados do repositorio:[https://wcota.me/covid19br](https://wcota.me/covid19br)
                onde casos e óbitos confirmados por dia utilizam informação oficial do [Ministério da Saúde](https://covid.saude.gov.br/), 
                dados no nível municipal vem do [Brasil.IO](https://brasil.io/dataset/covid19/caso) 
                e dados mais recentes são reportados pela equipe do [@CoronavirusBrasil](https://twitter.com/CoronavirusBra1).
                ''')],
        md=8
        ),
    dbc.Col(
        [dcc.Markdown('''
            #### Sobre    
            Feito por Lucas ferreira,[Linkedin](https://www.linkedin.com/in/lfcosta-1996/)   
            Contato:covidbrasil.contato@gmail.com  
            Código fonte:[Github](https://github.com/lucs123/covid-brasil)
            ''')],
        width={'offset':1},
        )
])        
#Layout
app.layout = html.Div(children=[
    html.Script('async defer',src="https://buttons.github.io/buttons.js"),
    dcc.Location(id='url'),
    html.Header(children=navbar),
    html.Br(),
    dbc.Container(id='content',fluid=True),
    html.Br(),
    html.Hr(),
    dbc.Container(footer,fluid=True)                    
    ])         


@app.callback(
    Output('content','children'),
    [Input('url','pathname')]
)
def update_content(url):
    if url == '/':
        return map_layout
    elif url == '/timeline':
        return graph_layout

# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

server = app.server    

if __name__ == '__main__':
    app.run_server(debug=True)    