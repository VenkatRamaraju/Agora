import sqlite3
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)

connection = sqlite3.connect('database.db')
cur = connection.cursor()
table2 = "TickerPredictions"

init_cleanup = f"""drop table if exists {table2};"""

cur.execute(init_cleanup)

table2_sql = f"""create table {table2}(
    ticker text primary key,
    company_name text,
    analyst_pred text,
    agora_pred float,
    headline_polarity float,
    conversation_polarity float
)"""

cur.execute(table2_sql)

ticker_predictions = pd.read_csv("../POC/all_companies_w_preds.csv", index_col=False)

del ticker_predictions["Unnamed: 0"]
del ticker_predictions["Unnamed: 0.1"]
del ticker_predictions["Buy"]

ticker_predictions.columns = ['ticker', 'company_name', 'analyst_pred', 'agora_pred', 'headline_polarity',
                              'conversation_polarity']

ticker_predictions.to_sql(table2, connection, if_exists="append", index=False)

connection.commit()
connection.close()
