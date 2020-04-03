#coding:UTF-8
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from brasil import page_brasil
from estados import page_estados
from cidades import page_cidades
from app import app

app.layout = html.Div(children=[
    dcc.Location(id='url'),
    html.H1(children='Covid no Brasil'),

    dcc.Link('Casos Brasil', href='/'),
    html.Br(),
    dcc.Link('Casos por estado', href='/estados'),
    html.Br(),
    dcc.Link('Casos por cidade', href='/cidades'),

    html.Div(id='page_layout')
])

@app.callback(Output('page_layout', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/':
        return page_brasil
    elif pathname == '/estados':
        return page_estados
    elif pathname == '/cidades':
        return page_cidades    
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)    