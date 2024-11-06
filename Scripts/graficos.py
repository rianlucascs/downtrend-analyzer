import matplotlib.pyplot as plt

class Graficos:

    def __init__(self, dowtrend):
        """
        Inicializa a classe Graficos com uma instância de Dowtrend.
        
        :param dowtrend: Instância da classe Dowtrend que contém os dados financeiros.
        """
        self.dowtrend = dowtrend

    def grafico1(self, ticker):
        """
        Gera um gráfico do preço de fechamento ajustado para um ativo, com as últimas 255 observações.

        :param ticker: O símbolo do ativo (ex: 'AESB3', 'ITUB4', etc.).
        """
        # Obtém os últimos 255 valores de fechamento ajustado
        df = self.dowtrend._obter_serie_temporal(ticker).tail(255)
        
        # Cria a figura do gráfico
        plt.figure(figsize=(14, 7), dpi=300)
        self._plot_price(df, ticker)
        self._add_title_and_labels_g1(ticker)
        self._add_legend()
        self._add_annotation(df, ticker)
        
        # Ajusta o layout e exibe o gráfico
        plt.tight_layout()
        plt.show()

    def grafico2(self, df, period):
        plt.figure(figsize=(14, 5), dpi=300)
        self._plot_bar(df, period)
        self._adjust_y_axis(df, period)
        self._add_title_and_labels_g2(period)
        self._add_legend()
        plt.tight_layout()
        plt.show()

    def _plot_price(self, df, ticker):
        """
        Plota os dados de preço de fechamento ajustado no gráfico.

        :param df: O DataFrame contendo os dados de preço ajustado.
        :param ticker: O símbolo do ativo.
        """
        plt.plot(df.index, df['Adj Close'], color='tab:orange', linewidth=3, label=f'{ticker} - Fechamento Ajustado')

    def _plot_bar(self, df, period):
        lista = []
        for i, value in enumerate(df[period]):
            # Se o valor for negativo, cor vermelha; se positivo, cor verde
            color = 'tab:red' if value < 0 else 'tab:green'
            lista.append(color)
        plt.bar(df.index, df[period], color=lista, alpha=0.9, label=f'Variação {period}')

    def _adjust_y_axis(self, df, period):
        """
        Ajusta o limite do eixo Y dinamicamente com base nos valores de variação do período.

        :param df: O DataFrame contendo os dados do ativo.
        :param period: O nome do período (ex: 'Variação diária', 'Variação semanal', etc.)
        """
        # Determina os valores mínimo e máximo da coluna de variação
        min_value = df[period].min()
        max_value = df[period].max()

        # Definir um fator de multiplicação para dar margem ao gráfico (ajuste a largura)
        margin_factor = 0.1  # 10% a mais para dar margem visual

        # Ajuste de limites com base nos valores encontrados
        plt.ylim(min_value - margin_factor * abs(min_value), max_value + margin_factor * abs(max_value))

    def _add_title_and_labels_g1(self, ticker):
        """
        Adiciona título, subtítulo, e labels ao gráfico.

        :param ticker: O símbolo do ativo.
        """
        plt.title(f'{ticker} - Preço de Fechamento Ajustado', fontsize=18, fontweight='bold', color='black', loc='center')
        plt.suptitle(f'Amostra ({self.dowtrend.type_amostra})', fontsize=12, fontstyle='italic', color='grey')
        plt.xlabel('Data', fontsize=14, fontweight='bold', color='black')
        plt.ylabel('Preço de Fechamento Ajustado (R$)', fontsize=14, fontweight='bold', color='black')
        plt.xticks(rotation=45, ha='right', fontsize=10, color='black')  
        plt.yticks(fontsize=10, color='black')
        plt.grid(True, linestyle='--', alpha=0.7, color='gray')

    def _add_title_and_labels_g2(self, period):
        """
        Adiciona título e labels específicos para o gráfico de barras.

        :param period: O nome do período (ex: 'Variação diária', 'Variação semanal', etc.)
        """
        plt.title(f'Variação {period}', fontsize=18, fontweight='bold', color='black', loc='center')
        plt.suptitle(f'Amostra ({self.dowtrend.type_amostra})', fontsize=12, fontstyle='italic', color='grey')
        plt.xlabel('Data', fontsize=14, fontweight='bold', color='black')
        plt.ylabel(f'Variação de {period} (%)', fontsize=14, fontweight='bold', color='black')
        plt.xticks(rotation=45, ha='right', fontsize=10, color='black')
        plt.yticks(fontsize=10, color='black')
        plt.grid(True, linestyle='--', alpha=0.5, color='gray')  # Grid mais suave

    def _add_legend(self):
        """
        Adiciona a legenda ao gráfico.
        """
        plt.legend(loc='upper left', fontsize=12, fancybox=True, framealpha=0.8, facecolor='w', edgecolor='black')

    def _add_annotation(self, df, ticker):
        """
        Adiciona a anotação no gráfico, com o valor atual do preço ajustado e outras informações.

        :param df: O DataFrame contendo os dados de preço ajustado.
        :param ticker: O símbolo do ativo.
        """
        # Obtém o último preço e a data correspondente
        max_price_value = df['Adj Close'].iloc[-1].iloc[-1]
        max_price_date = df.index[-1]

        # Obtém informações adicionais (semanal, quinzenal, mensal, anual)
        x = self.dowtrend.read_data('json')[ticker]
        other_infos = f'Semanal: {x["semanal"]}%\nQuinzenal: {x["quinzenal"]}%\nMensal: {x["mensal"]}%\nAnual: {x["anual"]}%'

        # Adiciona uma anotação no gráfico com a seta
        plt.annotate(f'Preço atual: R${max_price_value:.2f}\n{other_infos}',
                     xy=(max_price_date, max_price_value),  # Posição do texto
                     xytext=(max_price_date, max_price_value + 2),  # Posição do texto deslocado
                     arrowprops=dict(
                         facecolor='red',           
                         edgecolor='red',       
                         arrowstyle='->',           
                         lw=1,                      
                         connectionstyle='arc3,rad=-0.2'  
                     ),
                     fontsize=8,  # Tamanho da fonte
                     color='red',  # Cor do texto
                     fontweight='bold',  # Negrito
                     bbox=dict(facecolor='white', alpha=0.7, edgecolor='red', boxstyle='round,pad=0.3')  # Caixa de fundo
                     )

