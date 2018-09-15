import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('data/investimentos.xlsx')

df.head()

df.tail()

df = df[(df.nome=='erick') & (df.fundo=='WA500')]
df.tail()


# liquido = (saldoI + saque) - investimento




df = df[['data', 'saldoI']]
df.head()
df.set_index('data', inplace=True)

df.head()

df.index = pd.DatetimeIndex(df.index)


df['2017']

df2 = df.copy()

df2.tail()

df2.resample('M').mean()
df2.resample('D').pad()
df2.asfreq('D', method='ffill')


df3 = df2.resample('M').mean()



df3.plot()
plt.show()
