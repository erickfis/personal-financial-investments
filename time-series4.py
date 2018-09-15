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

df4 = df3.reset_index(level=0)
df4

df4['invest_cum'] = df4.groupby('fundo')['investimento'].transform(pd.Series.cumsum)
df4['saque_cum'] = df4.groupby('fundo')['saque'].transform(pd.Series.cumsum)


df4['liquido'] = df4.invest_cum - df4.saque_cum
df4['rendimento'] = df4.saldoF - df4.liquido


df4


dfWA = df4[df4.fundo == 'WA500']

dfWA
dfWA.rendimento.plot()
plt.show()

dfWA.rendimento.resample('W').mean().plot()
dfWA.rendimento.resample('M').mean().plot()
