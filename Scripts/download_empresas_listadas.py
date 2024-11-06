from dowtrend import Dowtrend

def main() -> None:
    """
    Função principal que instancia a classe `Dowtrend` para o tipo de amostra 'empresas_listadas' 
    e executa o método `loop()` para processar os dados.
    """
    try:
        # Criando uma instância da classe Dowtrend com o tipo de amostra 'empresas_listadas'
        dowtrend = Dowtrend(type_amostra='empresas_listadas')

        # Processando os dados dos tickers
        dowtrend.loop()
        print("Processamento das empresas listadas concluído com sucesso.")

    except Exception as e:
        # Caso ocorra um erro, será capturado e exibido
        print(f"Erro ao processar os dados: {e}")

if __name__ == '__main__':
    main()
