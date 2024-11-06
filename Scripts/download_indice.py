from dowtrend import Dowtrend

if __name__ == '__main__':
    indice = 'IDIV'
    indice = f'indice:{indice}'
    dowtrend = Dowtrend(type_amostra=indice)
    dowtrend.loop()