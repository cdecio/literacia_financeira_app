from app import *
from globals import *
from dash import html, dcc
import dash_bootstrap_components as dbc
from components import sidebar, dashboards
from dash.dependencies import Input, Output

# criar a página geral (espaço)
content = html.Div(id='page-content')

# definir o layout geral
app.layout = dbc.Container(children=[
    # criando store para o x da literacia financeira
    dcc.Store(id='store-x', data=x_literacy.to_dict()),
    dbc.Row([
        # coluna da sidebar
        dbc.Col([
            dcc.Location(id='url'),
            sidebar.layout
        ], md=4),
        # espaço para o dashboard
        dbc.Col([
            content
        ], md=8)
    ])
], fluid=True)

# callbacks
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def render_page(pathname: str) -> object:
    """
    renderiza a página de acordo com a url

    Parameters
    ----------
    pathname : str
        url da página

    Returns
    -------
    object
        layout renderizado da página
    """
    return dashboards.layout

if __name__ == '__main__':
    app.run_server(port=8051, debug=True)