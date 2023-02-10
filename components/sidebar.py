from app import *
from globals import *
from dash import html, dcc
import dash_bootstrap_components as dbc

# definir o layout da sidebar
layout = dbc.Col([
    dbc.CardGroup([
        html.Img(src='assets/imgs/Logo_Universidade_Europeia_Preto.svg', id='logo-university', alt='Universidade Europeia'),
        dbc.Card([
            html.H2('Scoring de Meios de Movimentação', id='title-primary'),
            html.P('Carlos Décio Cordeiro', id='name-info'),
        ], id='title-card')
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.H4('Grau Académico do Pai'),
            dcc.Dropdown(list(isced.get('degree_level').values()), id='academia-pai')
        ], width=6),
        dbc.Col([
            html.H4('Grau Académico da Mãe'),
            dcc.Dropdown(list(isced.get('degree_level').values()), id='academia-mae')
        ], width=6)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H4('Emprego do Pai'),
            dcc.Dropdown(list(isei.get('Emprego').values()), id='emprego-pai')
        ], width=6),
        dbc.Col([
            html.H4('Emprego da Mãe'),
            dcc.Dropdown(list(isei.get('Emprego').values()), id='emprego-mae')
        ], width=6)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H4('Expectativa Académica do Cliente'),
            dcc.Dropdown(list(isced.get('degree_level').values()), id='academia-cliente')
        ], width=6),
        dbc.Col([
            html.H4('Expectativa Profissional do Cliente'),
            dcc.Dropdown(list(isei.get('Emprego').values()), id='emprego-cliente')
        ], width=6)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H4('Ano de Escolaridade face ao esperado'),
            dcc.Slider(min=-2, max=1, step=1,
                marks={
                    -2: '-2',
                    -1: '-1', 
                    0: '0',
                    1: '1'
                },
                value=0,
                tooltip={'placement': 'bottom', 'always_visible': True},
                id='ano-escolaridade')
        ], width=6)
    ]),
    html.Hr(),
    html.Hr(),
    html.H2('Questionário'),
    dbc.Row([
        html.H5('Com que frequência discutes os assuntos seguintes com os teus pais (ou familiares)?'),
        html.H6('1 - Nunca ou quase nunca - 2 - Uma ou duas vezes por mês - 3 - Uma ou duas vezes por semana - 4 - Quase todos os dias', className='legend'),
        dbc.Col([
            html.H5('As tuas decisões sobre despesas'),
            dcc.Slider(min=1, max=4, step=1,
            marks={
                1: '1',
                2: '2', 
                3: '3',
                4: '4'
            },
            value=0,
            tooltip={'placement': 'bottom', 'always_visible': False},
            id='FL167Q01HA')
        ], width=6),
        dbc.Col([
            html.H5('As tuas decisões sobre poupança'),
            dcc.Slider(min=1, max=4, step=1,
            marks={
                1: '1',
                2: '2', 
                3: '3',
                4: '4'
            },
            value=0,
            tooltip={'placement': 'bottom', 'always_visible': False},
            id='FL167Q02HA')
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.H5('O dinheiro necessário para coisas que queres comprar'),
            dcc.Slider(min=1, max=4, step=1,
            marks={
                1: '1',
                2: '2', 
                3: '3',
                4: '4'
            },
            value=0,
            tooltip={'placement': 'bottom', 'always_visible': False},
            id='FL167Q04HA')
        ], width=6)
    ]),
    html.Hr(),
    dbc.Row([
        html.H5('Recebeste um email de uma operadora de telecomunicações móveis muito conhecida, na tua caixa de correio, dizendo que ganhaste um smartphone. ' +
                'O remetente pede-te que cliques num link para preencheres um formulário com os teus dados, para que te possam enviar o smartphone.' + 
                'Na tua opinião, em que medida as estratégias seguintes são apropriadas como reação a este email?', style={'textAlign': 'justify'}),
        html.H6('1 - Nada apropriada - 6 - Muito apropriada', className='legend'),
        dbc.Col([
            html.H5('Verificar o endereço de email do remetente', style={'height': '77%'}),
            dcc.Slider(min=1, max=6, step=1,
            marks={
                1: '1',
                2: '2', 
                3: '3',
                4: '4',
                5: '5',
                6: '6'
            },
            value=1,
            tooltip={'placement': 'bottom', 'always_visible': False},
            id='ST166Q02HA')
        ], width=6),
        dbc.Col([
            html.H5('Verificar na página da internet da operadora de telecomunicações móveis se existe alguma referência à oferta de smartphones.', style={'height': '76%'}),
            dcc.Slider(min=1, max=6, step=1,
            marks={
                1: '1',
                2: '2', 
                3: '3',
                4: '4',
                5: '5',
                6: '6'
            },
            value=1,
            tooltip={'placement': 'bottom', 'always_visible': False},
            id='ST166Q05HA')
        ], width=6)
    ]),
    html.Hr(),
    dbc.Row([
        html.H5('Em que medida é que cada uma das afirmações seguintes te descreve bem?', style={'textAlign': 'justify'}),
        html.H6('1 - Muitíssimo parecido comigo - 2 - Bastante parecido comigo - 3 - De certa forma parecido comigo - 4 - Não muito parecido comigo - ' +
                ' 5 - Nada parecido comigo', className='legend'),
        dbc.Col([
            html.H5('Eu consigo lidar com situações invulgares.', style={'height': '75%'}),
            dcc.Slider(min=1, max=5, step=1,
            marks={
                1: '1',
                2: '2', 
                3: '3',
                4: '4',
                5: '5',
            },
            value=1,
            tooltip={'placement': 'bottom', 'always_visible': False},
            id='ST216Q01HA')
        ], width=6),
        dbc.Col([
            html.H5('Eu consigo modificar o meu comportamento de modo a corresponder às exigências de situações novas.', style={'height': '75%'}),
            dcc.Slider(min=1, max=5, step=1,
            marks={
                1: '1',
                2: '2', 
                3: '3',
                4: '4',
                5: '5',
            },
            value=1,
            tooltip={'placement': 'bottom', 'always_visible': False},
            id='ST216Q02HA')
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.H5('Eu consigo adaptar-me a situações diferentes, mesmo sob stress ou pressão.'),
            dcc.Slider(min=1, max=5, step=1,
            marks={
                1: '1',
                2: '2', 
                3: '3',
                4: '4',
                5: '5'
            },
            value=1,
            tooltip={'placement': 'bottom', 'always_visible': False},
            id='ST216Q03HA')
        ], width=6)
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            html.Div([
                dbc.Button('Submeter', color='danger', id='submit-form')
            ], id='button-div'),
            width=12
        )
    ])
])
# criar folha de estilo para mudar a cor da legenda (OK)
# corrigir padding do título (OK)
# corrigir height dos slidebar - tentar deixar responsivo (OK)
# verificar sobre a formatação do boxplot (OK)
    # bolinha azul (OK)
    # tracejado azul - valor mínimo que seja 1 (OK)
# mudar a cor do título para vermelho (OK)
    # nome Carlos em preto (OK)
# input das questões pronto (OK)
# tratamento das valores (OK)
# terminar predições (OK)
# pesquisar sobre trigger baseado em evento (OK)
