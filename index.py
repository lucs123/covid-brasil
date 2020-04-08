#coding:UTF-8
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from brasil import page_brasil,card_brasil
from estados import page_estados,card_estados,menu_estados
from cidades import page_cidades,card_cidades,menu_cidades
from mapa import mapa
from app import app

links = dbc.Row(justify='end',children=[
            dbc.Col([dbc.NavItem(dbc.NavLink('Mapa', href='/'))]),
            dbc.Col([dbc.NavItem(dbc.NavLink('Timeline', href='/timeline'))]),
])

navbar = dbc.Navbar(children=[
    dbc.Row([
        dbc.Col([dbc.NavbarBrand(children='Covid no Brasil')]),
    ]),
    dbc.NavbarToggler(id="navbar-toggler"),
    dbc.Collapse(links, id="navbar-collapse", navbar=True),
])

#Layout
app.layout = html.Div(children=[
    dcc.Location(id='url'),
    html.Div(children=navbar),
    dbc.Container([
        html.Br(),
        dbc.Card([
            dbc.CardHeader('CASOS BRASIL'),
            dbc.CardBody(
                dbc.Row([
                    dbc.Col([html.Div(page_brasil)],md=8),
                    dbc.Col([html.Div(card_brasil)])
                ]),
            )    
        ]),
        html.Br(),
        dbc.Card([
            dbc.CardHeader('CASOS POR ESTADO'),
            dbc.CardBody(
                dbc.Row([
                    dbc.Col([html.Div(page_estados)],md=8),
                    dbc.Col([html.Div(menu_estados),html.Br(),html.Div(card_estados)])

                ]),
            )    
        ]),
        html.Br(),
        dbc.Card([
            dbc.CardHeader('CASOS POR CIDADE'),
            dbc.CardBody(
                dbc.Row([
                    dbc.Col([html.Div(page_cidades)],md=8),
                    dbc.Col([html.Div(menu_cidades),html.Br(),html.Div(card_cidades)])
                ])
            )    
        ]),
        html.Br()                
    ])         
])

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

if __name__ == '__main__':
    app.run_server(debug=True)    