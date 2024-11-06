from dowtrend import Dowtrend

def main() -> None:
    """
    Função principal que cria uma instância da classe `Dowtrend` e executa
    o método `loop()` para processar os dados do índice especificado.
    """
    # Definindo o índice a ser analisado
    indice = 'IDIV'
    indice_amostra = f'indice:{indice}'  # Formatação da string para a amostra

    try:
        # Instanciando a classe Dowtrend com o índice especificado
        dowtrend = Dowtrend(type_amostra=indice_amostra)
        
        # Processando os dados do índice
        dowtrend.loop()
        print(f"Processamento do índice {indice} concluído com sucesso.")

    except Exception as e:
        print(f"Erro ao processar o índice {indice}: {e}")

if __name__ == '__main__':
    main()
