import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('data/investimentos.xlsx')

df.tail()

df = df[(df.nome=='erick') & (df.fundo=='WA500')]
df.drop(['nome', 'fundo'], axis=1, inplace=True)

df = df.groupby('data').agg({'saldoI': max, 'investimento': sum, 'saque': sum})
# df.to_excel('wa2.xls')

df

# df.set_index('data', inplace=True)
df.index = pd.to_datetime(df.index)

df2 = df.asfreq('D')
# df2 = df.copy()

df2
df2.saldoI = df2.saldoI.fillna(method='bfill')
df2 = df2.fillna(0)
df2['saldoF'] = df2.saldoI + df2.investimento - df2.saque

df2

liquido =  df2.investimento.sum() - df2.saque.sum()
liquido

df2['liquido'] = df2.investimento.cumsum() - df2.saque.cumsum()
df2['rendimento'] = df2.saldoF - df2.liquido


df2.rendimento.plot()
plt.show()

df2.rendimento.resample('W').mean().plot()
df2.rendimento.resample('M').mean().plot()
