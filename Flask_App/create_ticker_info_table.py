import sqlite3
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)

connection = sqlite3.connect('database.db')
cur = connection.cursor()

init_cleanup = f"""drop table if exists TickerInfo;"""

cur.execute(init_cleanup)

table1 = "TickerInfo"

table1_sql = f"""create table {table1}(
    ticker text primary key,
    company_name text not null,
    analyst_rating text not null,
    headlines_polarity float not null,
    conversations_polarity float not null
)"""

cur.execute(table1_sql)

ticker_info = pd.read_csv("../Model_Training/training_data.csv")
ticker_comps = pd.read_csv("../Data_Collection/companies.csv")
ticker_ar = pd.read_csv("../Data_Collection/Scrapers/Final_Analyst_Rating.csv")
del ticker_ar["Unnamed: 0"]
del ticker_info["Unnamed: 0"]

# Reformat column names
ticker_info = ticker_info[["Ticker", "Headlines", "Conversations"]]
ticker_info.columns = ['ticker', 'headlines_polarity', 'conversations_polarity']
ticker_comps.columns = ['ticker', 'company_name']
ticker_ar.columns = ['ticker', 'analyst_rating']

# Merge columns into one DF
ticker_info = pd.merge(ticker_info, ticker_comps, on=['ticker'], how='left')
ticker_info = pd.merge(ticker_info, ticker_ar, on=['ticker'], how='left')

# print(ticker_info)

# Insert data into table
ticker_info.to_sql(table1, connection, if_exists="append", index=False)

connection.commit()
connection.close()
