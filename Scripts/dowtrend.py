
import json
from os.path import join
import requests
from pandas import read_csv, DataFrame
from io import StringIO
from yfinance import download
from numpy import nan
from os.path import dirname, abspath
from typing import List
import matplotlib.pyplot as plt

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Dowtrend:
    """
    Classe responsável por calcular e salvar os retornos financeiros de múltiplos tickers.
    """

    def __init__(self, qtd_output=10, type_amostra='indice:IDIV'):
        """
        Inicializa o DowtrendAnalyzer com os parâmetros necessários.
        """
        self.qtd_output = qtd_output
        self.type_amostra = type_amostra
        self.file_path = join(dirname(dirname(abspath(__file__))), 'data', type_amostra.replace(':', '_')+'.json')
    
    def tickers_empresas_listadas(self):
        url = 'https://raw.githubusercontent.com/rianlucascs/b3-scraping-project/master/processed_data/3.%20Empresas%20listadas/todas_empresas_listadas.csv'
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            raise ValueError(f'Erro ao acessar a página: {e}')
        return list(read_csv(StringIO(response.text), delimiter=';')['codigo_de_negociacao'].dropna())

    def tickers_indice(self, indice: str):
        url = f'https://raw.githubusercontent.com/rianlucascs/b3-scraping-project/master/processed_data/1.%20%C3%8Dndices%20de%20Segmentos%20e%20Setoriais/Setores/{indice}/Tabela_{indice}.csv'
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            raise ValueError(f'Erro ao acessar a página: {e}')
        return list(read_csv(StringIO(response.text), delimiter=',')['Código'])

    def amostra(self):
        if self.type_amostra == 'empresas_listadas':
            return self.tickers_empresas_listadas()
        elif 'indice:' in self.type_amostra:
            return self.tickers_indice(self.type_amostra.split(':')[1])
            
    def serie_temporal(self, ticker: str):
        try:
            return download(f'{ticker}.SA', progress=False, period='max')[['Adj Close']]
        except Exception as e:
            print(f"Erro, ticker: {ticker}: ao fazer o download {e}.")
            return DataFrame()

    def retorno(self, df_data, mode):
        _dict = {'semanal': 'W', 'quinzenal': '15D', 'mensal': 'ME', 'trimestral': 'QE', 'anual': 'YE'}
        return df_data['Adj Close'].resample(_dict[mode]).last().pct_change().dropna() * 100

    def get_latest(self, df_data):
        try:
            return float(round(df_data.iloc[-1].iloc[-1], 2))
        except Exception as e:
            logging.error(f"Erro pegar o último valor: {e}")
            return nan
        
    def process_ticker_data(self, ticker: str) -> dict:
        """
        Processa os dados de um único ticker e calcula os retornos.

        :param ticker: O código do ativo (ticker) a ser analisado.
        :return: Dicionário com os retornos calculados para diferentes períodos.
        """
        df = self.serie_temporal(ticker)
        return {
            'semanal': self.get_latest(self.retorno(df, 'semanal')),
            'quinzenal': self.get_latest(self.retorno(df, 'quinzenal')),
            'mensal': self.get_latest(self.retorno(df, 'mensal')),
            'trimestral': self.get_latest(self.retorno(df, 'trimestral')),
            'anual': self.get_latest(self.retorno(df, 'anual'))
        }
    
    def save_data(self, data: dict):
        """
        Salva os dados processados em um arquivo JSON.

        :param data: Dicionário com os dados a serem salvos.
        """
        try:
            with open(join(self.file_path), 'w') as json_file:
                json.dump(data, json_file, indent=4)
            logging.info(f"Dados salvos com sucesso no arquivo {self.file_path}.")
        except Exception as e:
            logging.error(f"Erro ao salvar os dados: {e}")
    
    def read_data(self, type):
        try:
            with open(self.file_path, 'r') as json_file:
                data = json.load(json_file) 
                if type == 'json':
                    return data
                if type == 'DataFrame':
                    return DataFrame(data).T
            return data
        except FileNotFoundError:
            print(f"Arquivo {self.file_path} não encontrado.")
            return None
        except json.JSONDecodeError:
            print(f"Erro ao decodificar o arquivo JSON.")
            return None

    def get_max(self, data, column, type):
        keys = {'DESVALORIZAÇÃO': True, 'VALORIZAÇÃO': False}
        return data.sort_values(by=column, ascending=keys[type]).head(self.qtd_output)

    def loop(self):
        """
        Processa os dados de todos os tickers e salva os resultados no arquivo JSON.
        """
        data = {}
        
        for i, ticker in enumerate(self.amostra()):
            logging.info(f"({i} / {len(self.amostra())}) Processando dados para o ticker: {ticker}")
            data[ticker] = self.process_ticker_data(ticker)
        
        self.save_data(data)
