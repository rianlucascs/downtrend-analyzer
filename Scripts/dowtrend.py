
import json
from os.path import join
import requests
from pandas import read_csv, DataFrame
from io import StringIO
from yfinance import download
from numpy import nan
from os.path import dirname, abspath
from typing import List, Dict, Optional

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Dowtrend:
    """
    Classe responsável por calcular e salvar os retornos financeiros de múltiplos tickers.

    A classe `Dowtrend` fornece funcionalidades para:
    - Obter tickers de empresas listadas ou de índices específicos.
    - Baixar séries temporais de dados financeiros de ações utilizando o `yfinance`.
    - Calcular e processar os retornos financeiros em diferentes períodos, como semanal, quinzenal, mensal, trimestral e anual.
    - Salvar e ler os dados extraídos em arquivos no formato JSON.
    - Identificar os tickers com os maiores ou menores retornos financeiros com base em um critério de valorização ou desvalorização.

    **Atributos:**
    - `qtd_output` (int): Quantidade de resultados a serem retornados, geralmente o número de maiores ou menores valores de valorização/desvalorização.
    - `type_amostra` (str): Tipo de amostra a ser utilizada para a extração de dados, podendo ser `'empresas_listadas'` ou um índice específico no formato `'indice:NOME'`.
    - `file_path` (str): Caminho do arquivo onde os dados processados serão salvos, com base no tipo de amostra.

    **Métodos:**
    - `__init__(self, qtd_output=10, type_amostra='indice:IDIV')`: Inicializa a classe `Dowtrend` com os parâmetros necessários.
    - `_get_tickers_empresas_listadas(self)`: Obtém a lista de tickers de todas as empresas listadas na B3.
    - `_get_tickers_indice(self, indice: str)`: Obtém a lista de tickers de um índice específico.
    - `_obter_amostra(self)`: Retorna a lista de tickers com base no tipo de amostra configurado.
    - `_obter_serie_temporal(self, ticker: str)`: Obtém a série temporal de um ticker específico com dados históricos de preços ajustados.
    - `_calcular_retorno(self, df_data: DataFrame, periodo: str)`: Calcula o retorno de um ativo em um período específico (semanal, quinzenal, mensal, trimestral ou anual).
    - `_obter_ultimo_valor(self, df_data: DataFrame)`: Obtém o último valor de um DataFrame contendo os retornos calculados.
    - `processar_dados_ticker(self, ticker: str)`: Processa os dados de um único ticker e calcula os retornos para diferentes períodos.
    - `save_data(self, data: Dict[str, Dict[str, float]])`: Salva os dados processados em um arquivo JSON.
    - `read_data(self, tipo: str)`: Lê os dados salvos de um arquivo JSON e os retorna no formato especificado (JSON ou DataFrame).
    - `obter_maximos(self, data: DataFrame, column: str, tipo: str)`: Obtém os tickers com os maiores ou menores retornos com base em um critério (VALORIZAÇÃO ou DESVALORIZAÇÃO).
    - `loop(self)`: Processa os dados de todos os tickers da amostra e salva os resultados no arquivo JSON.
    """

    def __init__(self, qtd_output=10, type_amostra='indice:IDIV'):
        """
        Inicializa a classe `Dowtrend` com os parâmetros necessários.

        :param qtd_output: Quantidade de resultados a serem retornados, geralmente o número de maiores ou menores valores de valorização ou desvalorização.
        :param type_amostra: Tipo de amostra a ser utilizada, como 'empresas_listadas' ou um índice específico como 'indice:IDIV'.
        """
        self.qtd_output = qtd_output
        self.type_amostra = type_amostra
        self.file_path = join(dirname(dirname(abspath(__file__))), 'data', type_amostra.replace(':', '_')+'.json')
    
    def _get_tickers_empresas_listadas(self) -> List[str]:
        """
        Obtém a lista de tickers de todas as empresas listadas na B3.

        :return: Lista de strings contendo os códigos de negociação das empresas listadas na B3.
        :raises ValueError: Se houver um erro ao acessar a URL para baixar os dados.
        """
        url = 'https://raw.githubusercontent.com/rianlucascs/b3-scraping-project/master/processed_data/3.%20Empresas%20listadas/todas_empresas_listadas.csv'
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            raise ValueError(f'Erro ao acessar a página: {e}')
        return list(read_csv(StringIO(response.text), delimiter=';')['codigo_de_negociacao'].dropna())

    def _get_tickers_indice(self, indice: str) -> List [str]:
        """
        Obtém a lista de tickers de um índice específico.

        :param indice: O nome do índice para o qual os tickers devem ser obtidos (exemplo: 'IDIV').
        :return: Lista de strings contendo os códigos dos tickers pertencentes ao índice especificado.
        :raises ValueError: Se houver um erro ao acessar a URL para baixar os dados.
        """
        url = f'https://raw.githubusercontent.com/rianlucascs/b3-scraping-project/master/processed_data/1.%20%C3%8Dndices%20de%20Segmentos%20e%20Setoriais/Setores/{indice}/Tabela_{indice}.csv'
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            raise ValueError(f'Erro ao acessar a página: {e}')
        return list(read_csv(StringIO(response.text), delimiter=',')['Código'])

    def _obter_amostra(self) -> List[str]:
        """
        Retorna a lista de tickers com base no tipo de amostra configurado na instância.

        O tipo de amostra pode ser 'empresas_listadas' ou um índice no formato 'indice:NOME'.

        :return: Lista de tickers a serem analisados.
        :raises ValueError: Se o tipo de amostra fornecido for desconhecido.
        """
        if self.type_amostra == 'empresas_listadas':
            return self._get_tickers_empresas_listadas()
        elif 'indice:' in self.type_amostra:
            indice = self.type_amostra.split(':')[1]
            return self._get_tickers_indice(indice)
        else:
            raise ValueError(f"Tipo de amostra '{self.type_amostra}' desconhecido.")
            
    def _obter_serie_temporal(self, ticker: str) -> DataFrame:
        """
        Obtém a série temporal de um ticker específico com dados históricos de preços ajustados.

        :param ticker: Código do ativo (ticker) para o qual os dados serão obtidos.
        :return: DataFrame contendo a série temporal de preços ajustados (Adj Close) para o ativo.
        :raises Exception: Se houver erro ao baixar os dados do ticker.
        """
        try:
            return download(f'{ticker}.SA', progress=False, period='max')[['Adj Close']]
        except Exception as e:
            logging.error(f"Erro ao baixar dados para o ticker {ticker}: {e}")
            return DataFrame()

    def _calcular_retorno(self, df_data: DataFrame, periodo: str) -> DataFrame:
        """
        Calcula o retorno de um ativo em um período específico.

        :param df_data: DataFrame contendo os preços ajustados (Adj Close) do ativo.
        :param periodo: O período para o qual o retorno será calculado (exemplo: 'semanal', 'quinzenal', 'mensal', 'trimestral', 'anual').
        :return: DataFrame contendo os retornos calculados para o período especificado.
        """
        periodos_map  = {'semanal': 'W', 'quinzenal': '15D', 'mensal': 'ME', 'trimestral': 'QE', 'anual': 'YE'}
        return df_data['Adj Close'].resample(periodos_map [periodo]).last().pct_change().dropna() * 100

    def _obter_ultimo_valor(self, df_data: DataFrame) -> float:
        """
        Obtém o último valor de um DataFrame de retornos calculados.

        :param df_data: DataFrame contendo os retornos calculados.
        :return: O último valor presente no DataFrame ou `nan` se ocorrer um erro.
        :raises Exception: Se houver um erro ao acessar o último valor.
        """
        try:
            return float(round(df_data.iloc[-1].iloc[-1], 2))
        except Exception as e:
            logging.error(f"Erro pegar o último valor: {e}")
            return nan
        
    def processar_dados_ticker(self, ticker: str) -> Dict[str, float]:
        """
        Processa os dados de um único ticker e calcula os retornos para diferentes períodos.

        Para cada ticker, os retornos são calculados para os períodos semanal, quinzenal, mensal, trimestral e anual.

        :param ticker: Código do ativo (ticker) a ser analisado.
        :return: Dicionário com os retornos calculados para os diferentes períodos (semanal, quinzenal, mensal, trimestral e anual).
        """
        df = self._obter_serie_temporal(ticker)
        return {
            'semanal': self._obter_ultimo_valor(self._calcular_retorno(df, 'semanal')),
            'quinzenal': self._obter_ultimo_valor(self._calcular_retorno(df, 'quinzenal')),
            'mensal': self._obter_ultimo_valor(self._calcular_retorno(df, 'mensal')),
            'trimestral': self._obter_ultimo_valor(self._calcular_retorno(df, 'trimestral')),
            'anual': self._obter_ultimo_valor(self._calcular_retorno(df, 'anual'))
        }
    
    def save_data(self, data: Dict[str, Dict[str, float]]) -> None:
        """
        Salva os dados processados em um arquivo JSON.

        :param data: Dicionário contendo os dados a serem salvos em formato JSON.
        :raises Exception: Se ocorrer um erro ao salvar o arquivo JSON.
        """
        try:
            with open(join(self.file_path), 'w') as json_file:
                json.dump(data, json_file, indent=4)
            logging.info(f"Dados salvos com sucesso no arquivo {self.file_path}.")
        except Exception as e:
            logging.error(f"Erro ao salvar os dados: {e}")
    
    def read_data(self, type) -> Optional[Dict[str, Dict[str, float]]]:
        """
        Lê os dados salvos de um arquivo JSON e os retorna no formato especificado.

        :param tipo: Tipo de leitura ('json' para dicionário ou 'DataFrame' para DataFrame).
        :return: Dados carregados no formato especificado (dicionário ou DataFrame).
        :raises FileNotFoundError: Se o arquivo JSON não for encontrado.
        :raises json.JSONDecodeError: Se houver erro ao decodificar o arquivo JSON.
        """
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

    def obter_maximos(self, data: DataFrame, column: str, tipo: str) -> DataFrame:
        """
        Obtém os tickers com os maiores ou menores retornos com base em um critério (VALORIZAÇÃO ou DESVALORIZAÇÃO).

        :param data: DataFrame contendo os dados de retorno.
        :param column: Nome da coluna com os valores de retorno (exemplo: 'semanal', 'quinzenal', etc.).
        :param tipo: Tipo de critério para ordenação ('VALORIZAÇÃO' para maiores retornos ou 'DESVALORIZAÇÃO' para menores retornos).
        :return: DataFrame contendo os tickers classificados conforme o critério.
        """
        criterios = {'DESVALORIZAÇÃO': True, 'VALORIZAÇÃO': False}
        return data.sort_values(by=column, ascending=criterios[tipo]).head(self.qtd_output)

    def loop(self):
        """
        Processa os dados de todos os tickers da amostra e salva os resultados no arquivo JSON.

        Este método percorre a lista de tickers definida pela amostra, processa os dados para cada um e salva os resultados.
        """
        data = {}
        
        for i, ticker in enumerate(self._obter_amostra()):
            logging.info(f"({i} / {len(self._obter_amostra())}) Processando dados para o ticker: {ticker}")
            data[ticker] = self.processar_dados_ticker(ticker)
        
        self.save_data(data)
