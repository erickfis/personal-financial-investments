"""Meu ts."""
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.offline as pyo


def make_df(nome='erick'):
    """Gerando o df."""
    df = pd.read_excel('data/investimentos.xlsx')

    df = df[df.nome == nome]

    df['data'] = pd.to_datetime(df.data)

    df2 = df.groupby(['fundo', 'data']).agg({
                                            'saldoI': max,
                                            'investimento': sum,
                                            'saque': sum
                                            })

    # resample para daily points - padronizando ts
    df2 = df2.reset_index(level=[0])
    df3 = df2.groupby('fundo').resample('D').asfreq()

    df3.drop('fundo', axis=1, inplace=True)

    # fillna diferenciado para cada coluna
    df3.saldoI = df3.saldoI.fillna(method='bfill')
    df3 = df3.fillna(0)

    df3['saldoF'] = df3.saldoI + df3.investimento - df3.saque

    # slicing para multiindex
    # df3.loc[df3.index.get_level_values('fundo') =='WA500']
    #
    # dfWA = df3.query('fundo == "WA500"')

    # index só por data
    # preparando o cumsum nos grupos
    df4 = df3.reset_index(level=0)

    df4['invest_cum'] = df4.groupby('fundo')['investimento'].transform(pd.Series.cumsum)
    df4['saque_cum'] = df4.groupby('fundo')['saque'].transform(pd.Series.cumsum)

    df4['liquido'] = df4.invest_cum - df4.saque_cum
    df4['rendimento'] = df4.saldoF - df4.liquido

    return df4


df = make_df()

df = df[['fundo', 'liquido', 'rendimento']]
df2 = df.reset_index()
df2

df_plot = pd.pivot_table(df2, values='rendimento',
                index='data', columns='fundo'
                )
df_plot = df_plot.fillna(method='bfill').reset_index()
df_plot.set_index('data', inplace=True)
df_plot


df_plot['2017-07':].plot.line(figsize=(12,12))


help(pd.DataFrame.plot.line)


def gera_plotly(df):
    """Gera plotly."""
    data = [
            go.Scatter(
                    x=df[df.fundo == fundo].index,
                    y=df[df.fundo == fundo].rendimento,
                    mode='lines',
                    name=fundo
                    )
            for fundo in df.fundo.unique()
            ]

    layout = go.Layout(
                        title='Investimentos',
                        xaxis=dict(title='Data'),
                        yaxis=dict(title='R$'),
                        hovermode='closest'
                    )

    fig = go.Figure(data=data, layout=layout)
    return fig


fig = gera_plotly(df)
pyo.plot(fig)




# dfWA.rendimento.resample('W').mean().plot()
# dfWA.rendimento.resample('M').mean().plot()
