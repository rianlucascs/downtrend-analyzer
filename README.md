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

