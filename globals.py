import os
import pickle
import pandas as pd
from pycaret.regression import load_model

# definir caminhos para arquivos de predição
# e arquivos dos modelos
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(ROOT_PATH, 'data')
MODELS_PATH = os.path.join(ROOT_PATH, 'models')
BOXPLOT_DATA = 'gpcm_ok.csv'
ISCED_DATA = 'isced.csv'
ISEI_DATA = 'isei.csv'
ISCED_NUM = 'isced_num.csv'

# carregar a base de dados para boxplot
boxplot_data = pd.read_csv(os.path.join(DATA_PATH, BOXPLOT_DATA),index_col=[0])

# lista com as colunas para boxplot
colunas_boxplot = ["GRADE", "MISCED", "FISCED", "BMMJ1", "BFMJ2", "BSMJ",
                   "sisced", "COGFLEX", "FLFAMILY", "METASPAM"]

# lista com o título das colunas para boxplot
titulos_boxplot = ["GRADE2", "MISCED2", "FISCED", "BMMJ1", "BFMJ2", "BSMJ",
                   "sisced", "COGFLEX2", "FLFAMILY", "METASPAM"]

# literacia suficiente
SUF_LITERACIA = 475 

# carregar os modelos
files_path = [os.path.join(MODELS_PATH, f) for f in os.listdir(MODELS_PATH)]
files_path.sort()
models_dict = {}
for m, f in zip(['cog_flex', 'flfamily', 'metaspam', 'literacy'], files_path):
    models_dict[m] = load_model(f.split('.')[0])

# carregar os arquivos de mapeamento
isced = pd.read_csv(os.path.join(DATA_PATH, ISCED_DATA)).to_dict()
isei = pd.read_csv(os.path.join(DATA_PATH, ISEI_DATA)).to_dict()
isced_num = pd.read_csv(os.path.join(DATA_PATH, ISCED_NUM)).to_dict()
isced_mapping = {k: v for k, v in zip(isced_num['degree_level'].values(), isced_num['score'].values())}

# conversão do MISCED / FISCED / sisced para os dados numéricos
for col in ['MISCED', 'FISCED', 'sisced']:
    boxplot_data[col] = boxplot_data[col].map(isced_mapping)

# eliminando chaves
isei.get('Emprego').pop(298)
isei.get('ISEI ').pop(298)

# lista dos nomes das variáveis
titulos_validacao = [
    'Grau Académico do Pai',
    'Grau Académico da Mãe',
    'Emprego do Pai',
    'Emprego da Mãe',
    'Expectativa Académica do Cliente',
    'Expectativa Profissional do Cliente'
]

# definir no. de linhas e colunas de boxplot
N_ROW = 2
N_COLS = 5

# checar se a base de predição que precisa ser compartilhada existe
x_literacy = pd.DataFrame(columns=colunas_boxplot) 

