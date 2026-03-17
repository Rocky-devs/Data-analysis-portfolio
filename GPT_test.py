import pandas as pd

data_jan = {
'OrderID':['A1001','A1002','A1003'],
'Product':['iPhone','MacBook','AirPods'],
'Price':['$1299','$1999','$299'],
'Quantity':['2 pcs','1 pcs','3 pcs']
}
data_feb = {
'OrderID':['A1004','A1005','A1002'],
'Product':['iPhone','AirPods','MacBook'],
'Price':['$1299','$299','$1999'],
'Quantity':['1 pcs','2 pcs','1 pcs']
}
data_mar = {
'OrderID':['A1006','A1007','A1008'],
'Product':['MacBook','AirPods','iPhone'],
'Price':['$1999','$299','$1299'],
'Quantity':['2 pcs','4 pcs','1 pcs']
}

df_jan = pd.DataFrame(data_jan)
df_feb = pd.DataFrame(data_feb)
df_mar = pd.DataFrame(data_mar)

df = pd.concat([df_jan,df_feb,df_mar],ignore_index=True)

df = df.drop_duplicates(subset=['OrderID'],ignore_index=True)

df['Price'] = df['Price'].str.replace('$','')
df['Price'] = pd.to_numeric(df['Price'],errors='coerce')

df['Quantity'] = df['Quantity'].str.replace('pcs','')
df['Quantity'] = pd.to_numeric(df['Quantity'],errors='coerce')
df['Total'] = df['Quantity'] * df['Price']

product_total = df.groupby('Product')['Total'].sum().sort_values(ascending=False)
product_summary = df.groupby('Product')['Quantity'].sum().sort_values(ascending=False)

with pd.ExcelWriter('data_clean.xlsx',engine='xlsxwriter') as writer:
    df.to_excel(writer,sheet_name='results_clean')
    product_total.to_excel(writer,sheet_name='product_total')
    product_summary.to_excel(writer,sheet_name='product_summary')