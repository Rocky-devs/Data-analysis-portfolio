import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Online_Retail.csv',encoding='ISO-8859-1',dtype=str)

df['Quantity'] = pd.to_numeric(df['Quantity'],errors='coerce')
df['UnitPrice'] = pd.to_numeric(df['UnitPrice'],errors='coerce')
df['Revenue'] = df['Quantity'] * df['UnitPrice']

country_rank10 = df[df['Country'] != 'United Kingdom'].groupby('Country')['Revenue'].sum().sort_values(ascending=False)[:10]

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
sale_trend_month = df.groupby(df['InvoiceDate'].dt.to_period('M'))['Revenue'].sum()

bestseller = df[df['Quantity']>0].groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)

bestseller.plot()

plt.xticks(rotation=45,fontsize=8)
plt.show()

#print(df.columns.tolist())





