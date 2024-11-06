from dowtrend import Dowtrend

# Dicionário de índices, com os códigos e suas respectivas descrições
INDICES = {
    'IDIV': 'Índice Dividendos BM&FBOVESPA (IDIV B3)',
    'MLCX': 'Índice MidLarge Cap (MLCX B3)',
    'SMLL': 'Índice Small Cap (SMLL B3)',
    'IVBX': 'Índice Valor (IVBX 2 B3)',
    'AGFS': 'Índice Agronegócio B3 (IAGRO B3)',
    'IFNC': 'Índice BM&FBOVESPA Financeiro (IFNC B3)',
    'IBEP': 'Índice Bovespa B3 Empresas Privadas (Ibov B3 Empresas Privadas)',
    'IBEE': 'Índice Bovespa B3 Estatais (Ibov B3 Estatais)',
    'IBHB': 'Índice Bovespa Smart High Beta B3 (Ibov Smart High Beta B3)',
    'IBLV': 'Índice Bovespa Smart Low Volatility B3 (Ibov Smart Low B3)',
    'IMOB': 'Índice Imobiliário (IMOB B3)',
    'UTIL': 'Índice Utilidade Pública BM&FBOVESPA (UTIL B3)',
    'ICON': 'Índice de Consumo (ICON B3)',
    'IEEX': 'Índice de Energia Elétrica (IEE B3)',
    'IFIL': 'Índice de Fundos de Investimentos Imobiliários de Alta Liquidez (IFIX L B3)',
    'IMAT': 'Índice de Materiais Básicos BM&FBOVESPA (IMAT B3)',
    'INDX': 'Índice do Setor Industrial (INDX B3)',
    'IBSD': 'Índice Bovespa Smart Dividendos B3 (Ibov Smart Dividendos B3)',
    'BDRX': 'Índice de BDRs Não Patrocinados-GLOBAL (BDRX B3)',
    'IFIX': 'Índice de Fundos de Investimentos Imobiliários (IFIX B3)'
}

def processar_indice(indice: str, numero: int) -> None:
    """
    Processa os dados para um índice específico, instanciando a classe Dowtrend
    e executando o método de processamento para cada um dos índices.

    :param indice: Código do índice a ser analisado (ex.: 'IDIV', 'SMLL').
    :param numero: Número sequencial do índice no dicionário `INDICES`.
    """
    print(f'Processando o {numero}º índice: {indice} ({INDICES[indice]})')
    # Inicializa a classe Dowtrend com o tipo de amostra configurado como o índice
    dowtrend = Dowtrend(type_amostra=f'indice:{indice}')
    dowtrend.loop()
    print(f'Finalizado o processamento do índice: {indice}.\n')

def main() -> None:
    """
    Função principal que executa o processamento de todos os índices presentes
    no dicionário `INDICES`.

    Para cada índice, o código instancia a classe Dowtrend e executa o método `loop`
    para coletar e salvar os dados financeiros.
    """
    for i, indice in enumerate(INDICES.keys()):
        processar_indice(indice, i)

if __name__ == '__main__':
    main()
