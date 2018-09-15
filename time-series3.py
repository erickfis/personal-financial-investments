import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('data/investimentos.xlsx')

df.tail()

df = df[df.nome=='erick']

df['data'] = pd.to_datetime(df.data)

df2 = df.groupby(['fundo', 'data']).agg({'saldoI': max, 'investimento': sum, 'saque': sum})

df2


df2.index
df2 = df2.reset_index(level=[0])


df2
df3 = df2.groupby('fundo').resample('D').asfreq()


df3.drop('fundo', axis=1, inplace=True)

df3

df3.saldoI = df3.saldoI.fillna(method='bfill')
df3 = df3.fillna(0)

df3['saldoF'] = df3.saldoI + df3.investimento - df3.saque

# slicing
# df3.loc[df3.index.get_level_values('fundo') =='WA500']
#
# dfWA = df3.query('fundo == "WA500"')

###########


df3

liquido = df3.investimento.sum() - df3.saque.sum()
liquido

# df3['liquido'] = df3.investimento.cumsum() - df3.saque.cumsum()
# df3['rendimento'] = df3.saldoF - df3.liquido

df4 = df3.reset_index(level=0)

df4

df3.rendimento.plot()
plt.show()

df3.rendimento.resample('W').mean().plot()
df3.rendimento.resample('M').mean().plot()
