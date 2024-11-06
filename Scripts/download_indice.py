from dowtrend import Dowtrend

if __name__ == '__main__':
    indice = 'indice:IDIV'
    dowtrend = Dowtrend(type_amostra=indice)
    dowtrend.loop()