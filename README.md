# Downtrend Analyzer

## Descrição

Este projeto tem como objetivo identificar e exibir as tendências de alta e baixa de diferentes conjuntos de ações, com base em diversos períodos de análise, como semanal, quinzenal, mensal e anual.

## Como usar

1. Clone o repositório:
    ```bash
    git clone https://github.com/rianlucascs/downtrend-analyzer.git

2. Navegue até o diretório do projeto:
    ```bash
    cd b3-scraping-project

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt

4. Execute os scripts para atualizar:
    ```bash
    # Atualizar todos os índices
    download_indices.py

    # Atualizar apenas um indice especifico
    download_indice.py

    # Atualizar empresas listadas
    download_empresas_listadas.py
    ```
    No arquivo ``download_indices.py``, altere a variável ``indice`` para realizar o download apenas do índice específico desejado.
    ```python

        from dowtrend import Dowtrend

        if __name__ == '__main__':
            indice = 'IDIV'
            indice = f'indice:{indice}'
            dowtrend = Dowtrend(type_amostra=indice)
            dowtrend.loop()
    ```

## Exemplo de uso


```python
# Define o período da análise da série temporal
period = 'mensal'  # Opções: semanal, quinzenal, mensal, trimestral, anual

# Define o tipo de amostra (índice ou outro conjunto de ações)
type_amostra = 'indice:IDIV'

# Cria uma instância da classe Dowtrend com o tipo de amostra selecionado
dowtrend = Dowtrend(type_amostra=type_amostra)

# Lê os dados financeiros em formato DataFrame
data = dowtrend.read_data('DataFrame')

# Obtém a tendência de desvalorização ou valorização com base no período selecionado
# 'type' pode ser 'DESVALORIZAÇÃO' ou 'VALORIZAÇÃO'
dowtrend_data = dowtrend.get_max(data, period, type='DESVALORIZAÇÃO')  # Substitua por 'VALORIZAÇÃO' se necessário

# Exibe o DataFrame com os resultados da análise de tendências
dowtrend_data