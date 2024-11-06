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
```

## Saidas

| Ticker  | Semanal | Quinzenal | Mensal | Trimestral | Anual  |
|---------|---------|-----------|--------|------------|--------|
| SAPR4   | 0.38    | 0.38      | -3.79  | -10.57     | -4.94  |
| CURY3   | -1.67   | -6.14     | -3.60  | 7.00       | 42.17  |
| BBDC4   | -1.14   | -1.14     | -2.93  | -3.69      | -13.51 |
| TIMS3   | -2.36   | -4.84     | -2.71  | -13.88     | -5.58  |
| PETR3   | -0.39   | -3.27     | -2.33  | -2.85      | 10.38  |
| BBDC3   | -0.42   | -5.84     | -2.14  | -3.30      | -13.41 |
| FLRY3   | 2.04    | -4.09     | -1.96  | -5.83      | -16.89 |
| PETR4   | -0.08   | -1.99     | -1.45  | -1.72      | 7.88   |
| DIRR3   | 0.62    | -1.63     | -1.41  | 1.95       | 47.89  |
| SANB11  | 0.26    | 0.26      | -1.21  | -4.02      | -12.00 |


![output1](https://github.com/user-attachments/assets/a4a1ed47-056a-4332-b121-047495618fdd)

![output2png](https://github.com/user-attachments/assets/c5f4fa35-da4a-4f4a-aa97-41faa4558fca)

Mais exemplos de uso em: **['/analyzer.ipynb'](https://github.com/rianlucascs/downtrend-analyzer/blob/master/analyzer.ipynb)**.

## Contato

Estou à disposição para esclarecer dúvidas ou fornecer mais informações. Você pode entrar em contato através das seguintes opções:

- **LinkedIn:** [Visite meu perfil no LinkedIn](www.linkedin.com/in/rian-lucas)
- **GitHub:** [Explore meu repositório no GitHub](https://github.com/rianlucascs)
- **Celular:** +55 61 96437-9500


Fico sempre aberto a colaborações e oportunidades de networking!