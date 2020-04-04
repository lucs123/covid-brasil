#coding:UTF-8
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from brasil import page_brasil,card_brasil
from estados import page_estados,card_estados,menu_estados
from cidades import page_cidades,card_cidades,menu_cidades
from app import app

links = dbc.Row(justify='end',children=[
            dbc.Col([dbc.NavItem(dbc.NavLink('Brasil', href='/brasil'))]),
            dbc.Col([dbc.NavItem(dbc.NavLink('Estados', href='/estados'))]),
            dbc.Col([dbc.NavItem(dbc.NavLink('Municipios', href='#cidades'))]),
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
        dbc.Row([
            dbc.Col([html.Div(page_brasil)]),
            dbc.Col([html.Div(card_brasil)])
        ]),
        dbc.Row([
            dbc.Col([html.Div(page_estados)]),
            dbc.Col([html.Div(menu_estados),html.Div(card_estados)])

        ]),
        dbc.Row([
            dbc.Col([html.Div(page_cidades)]),
            dbc.Col([html.Div(menu_cidades),html.Div(card_cidades)])
        ])
    ])         
])


# @app.callback([Output('page_layout', 'children'),
#                Output('card','children')], 
#               [Input('url', 'pathname')])

# def display_page(pathname):
#     if pathname == '/brasil':
#         return page_brasil,card_brasil
#     elif pathname == '/estados':
#         return page_estados,card_estados
#     elif pathname == '/municipios':
#         return page_cidades,card_cidades    
#     else:
#         return '404'

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