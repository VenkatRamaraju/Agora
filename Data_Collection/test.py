import pandas as pd

df1 = pd.read_csv("companies.csv")
companies1 = set()

for index, row in df1.iterrows():
    companies1.add(row['Symbol'])

df2 = pd.read_csv("tickers_companies.csv")
companies2 = set()

for index, row in df2.iterrows():
    companies2.add(row['Tickers'])

for ticker in companies1:
    if ticker not in companies2:
        print(ticker)
