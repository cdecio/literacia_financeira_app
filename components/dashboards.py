from app import *
import numpy as np
import pandas as pd
from globals import *
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State

# definir um estilo de espaçamento padrão para gráficos
graph_margin = dict(l=25, r=25, t=25, b=0)

def serve_layout():
    """
    constrói o layout da página
    """
    # definindo o layout
    layout = dbc.Col([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.H1('-', id='literacy-prediction')
                ], id='prediction-card')
            ], width=12)
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(figure=plot_boxplots(), id='boxplot-plots'),
                ], id='boxplot-row')
            ], width=12)
        ])
    ])

    return layout


def plot_boxplots() -> object:
    """
    constroi os boxplots no dashboard

    Returns
    -------
    object
        figura do boxplot
    """

    # construir a figura
    fig = make_subplots(rows=N_ROW, cols=N_COLS,
                        subplot_titles=titulos_boxplot)

    coluna = 0
    for row in range(N_ROW):
        for col in range(N_COLS):
            
            # obtendo o nome da coluna
            nome_coluna = colunas_boxplot[coluna]

            # construindo o boxplot do misced - 1
            fig.add_trace(
                go.Box(x=boxplot_data[nome_coluna].values,
                    fillcolor='rgba(255,255,255,0)',
                    opacity=1, name=""),
                row=row+1, col=col+1
            )

            # amostrar aqueles valores cuja literacia sejam maiores que 500
            literacia_suf = boxplot_data.loc[
                boxplot_data['literacy'] >= SUF_LITERACIA, nome_coluna]
            
            # valor mínimo da variável
            valor_minimo = literacia_suf.values.min()

            fig.add_vline(x=valor_minimo,
                          line_dash="dash", opacity=0.4,
                          row=row+1, col=col+1)

            coluna += 1

    fig.update_layout(
        height=1200,
        #width=1500,
        autosize=True,
        plot_bgcolor='rgba(0,0,0,0.01)',
        showlegend=False
    )
    fig.update_traces(
        overwrite='h',
        marker={'size': 10},
        line_color='red',
        line_width=3
    )

    return fig

layout = serve_layout()

# FUNCTIONS CALLBACKS --------------------------------------------------------------------------------------------
@app.callback(
    [
        Output('literacy-prediction', 'children'),
        Output('store-x', 'data')
    ],
    Input('submit-form', 'n_clicks'),
    [
        State('academia-pai', 'value'),
        State('academia-mae', 'value'),
        State('emprego-pai', 'value'),
        State('emprego-mae', 'value'),
        State('academia-cliente', 'value'),
        State('emprego-cliente', 'value'),
        State('ano-escolaridade', 'value'),
        State('FL167Q01HA', 'value'),
        State('FL167Q02HA', 'value'),
        State('FL167Q04HA', 'value'),
        State('ST166Q02HA', 'value'),
        State('ST166Q05HA', 'value'),
        State('ST216Q01HA', 'value'),
        State('ST216Q02HA', 'value'),
        State('ST216Q03HA', 'value')
    ],
    prevent_initial_call=True
)
def predicoes_boxplot(n: int,
                      isced_pai: str,
                      isced_mae: str,
                      emprego_pai: str,
                      emprego_mae: str,
                      isced_cliente: str,
                      emprego_cliente: str,
                      ano_escola: str,
                      fl167q01ha: str,
                      fl167q02ha: str,
                      fl167q04ha: str,
                      st166q02ha: str,
                      st166q05ha: str,
                      st216q01ha: str,
                      st216q02ha: str,
                      st216q03ha: str) -> list:
    
    # transformando a base de isced e isei em dataframes
    isced_df = pd.DataFrame(isced)
    isei_df = pd.DataFrame(isei)

    if n:

        # criando lista de variáveis para validação
        lista_validacao = [
            isced_pai,
            isced_mae,
            emprego_pai,
            emprego_mae,
            isced_cliente,
            emprego_cliente
        ]
        
        # validação dos valores
        for var in lista_validacao:
            if not var:
                idx = lista_validacao.index(var)
                return f'Campo {titulos_validacao[idx]} em falta'
        
        # preparando o vetor para predição do COGFLEX
        # COGFLEX=['ST216Q01HA','ST216Q02HA','ST216Q03HA','COGFLEX']
        x_cogflex = pd.DataFrame(
            np.array([st216q01ha, st216q02ha, st216q03ha]).reshape(1, -1),
            columns=['ST216Q01HA','ST216Q02HA','ST216Q03HA'],
            index=[0]
        )

        # realizando predição do COGFLEX
        cogflex = models_dict.get('cog_flex').predict(x_cogflex)[0]

        # FLFAMILY=['FL167Q01HA','FL167Q02HA','FL167Q04HA','FLFAMILY']
        # preparando o vetor para predição do FLFAMILY
        x_flfamily = pd.DataFrame(
            np.array([fl167q01ha, fl167q02ha, fl167q04ha]).reshape(1, -1),
            columns=['FL167Q01HA','FL167Q02HA','FL167Q04HA'],
            index=[0]
        )

        # realizando predição FLFAMILY
        flfamily = models_dict.get('flfamily').predict(x_flfamily)[0]


        # METASPAM=['ST166Q02HA','ST166Q05HA','METASPAM']
        # preparando o vetor para predição do METASPAM
        x_metaspam = pd.DataFrame(
            np.array([st166q02ha, st166q05ha]).reshape(1, -1),
            columns=['ST166Q02HA', 'ST166Q05HA'],
            index=[0]
        )

        # realizando predição METASPAM
        metaspam = models_dict.get('metaspam').predict(x_metaspam)[0]
        
        # obtendo os valores do ISCED
        misced = isced_df.loc[isced_df['degree_level'] == isced_mae, 'score'].values[0]
        fisced = isced_df.loc[isced_df['degree_level'] == isced_pai, 'score'].values[0]
        sisced = isced_df.loc[isced_df['degree_level'] == isced_cliente, 'score'].values[0]

        # obtendo os valores do ISEI
        bmmj1 = isei_df.loc[isei_df['Emprego'] == emprego_mae, 'ISEI '].values[0]
        bfmj2 = isei_df.loc[isei_df['Emprego'] == emprego_pai, 'ISEI '].values[0]
        bsmj = isei_df.loc[isei_df['Emprego'] == emprego_cliente, 'ISEI '].values[0]

        # preparando o vetor para predição do LIT_FINANCEIRA
        # cat_literacy=['GRADE' ,'MISCED', 'FISCED', 'BMMJ1', 'BFMJ2', 'BSMJ', 'sisced',
        #               'COGFLEX', 'FLFAMILY', 'METASPAM']
        x = pd.DataFrame(
            np.array([
                float(ano_escola), 
                misced,
                fisced,
                bmmj1,
                bfmj2,
                bsmj,
                sisced,
                cogflex,
                flfamily,
                metaspam    
            ]).reshape(1, -1),
            columns=['GRADE' ,'MISCED', 'FISCED', 'BMMJ1', 'BFMJ2',
                     'BSMJ', 'sisced', 'COGFLEX', 'FLFAMILY', 'METASPAM'],
            index=[0]
        )

        # realizando predição CAT_LITERACY
        cat_literacy = int(models_dict.get('literacy').predict(x)[0])
        prob_literacy = models_dict.get('literacy').predict_proba(x)[0][1]


        # retorna valor para o card
        if cat_literacy == 0:
            return [f'Preferível Recusar]
            #return [f'Preferível Recusar - Confiança {round(prob_literacy * 100, 2)} %', x.to_dict()]
        else:
            return [f'Preferível Aceitar]
            #return [f'Preferível Aceitar - Confiança {round(prob_literacy * 100, 2)} %', x.to_dict()]
    else:
        raise PreventUpdate

@app.callback(
    Output('boxplot-plots', 'figure'),
    [
        Input('store-x', 'data')
    ],
    prevent_initial_call=True
)
def update_boxplots(x: dict) -> object:

    # construir a figura
    fig = make_subplots(rows=N_ROW, cols=N_COLS,
                        subplot_titles=colunas_boxplot)

    print(x)

    coluna = 0
    for row in range(N_ROW):
        for col in range(N_COLS):
            
            # obtendo o nome da coluna
            nome_coluna = colunas_boxplot[coluna]

            # construindo o boxplot do misced - 1
            fig.add_trace(
                go.Box(x=boxplot_data[nome_coluna].values, y0=0,
                    fillcolor='rgba(255,255,255,0)',
                    opacity=1, name=""),
                row=row+1, col=col+1
            )

            fig.add_trace(
                go.Scatter(x=[x[nome_coluna]['0']], y=[0],
                           name='', marker_color='blue',
                           marker_size=20),
                row=row+1, col=col+1
            )

            # amostrar aqueles valores cuja literacia sejam maiores que 500
            literacia_suf = boxplot_data.loc[
                boxplot_data['literacy'] >= SUF_LITERACIA, nome_coluna]
            
            # valor mínimo da variável
            valor_minimo = literacia_suf.values.min()

            fig.add_vline(x=valor_minimo,
                          line_dash="dash",
                          row=row+1, col=col+1)

            coluna += 1

    fig.update_layout(
        height=1200,
        #width=1500,
        autosize=True,
        plot_bgcolor='rgba(0,0,0,0.01)',
        showlegend=False
    )
    fig.update_traces(
        overwrite='h',
        # marker={'size': 10},
        line_color='red',
        line_width=3
    )
    fig.update_yaxes(showticklabels=False)

    return fig
