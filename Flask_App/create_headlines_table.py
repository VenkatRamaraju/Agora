import sqlite3
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)

connection = sqlite3.connect('database.db')
cur = connection.cursor()
table2 = "TickerHeadlines"

init_cleanup = f"""drop table if exists {table2};"""

cur.execute(init_cleanup)

table2_sql = f"""create table {table2}(
    headlines text,
    ticker text not null,
    foreign key (ticker) references TickerPredictions(ticker)
)"""

cur.execute(table2_sql)

ticker_headlines = pd.read_csv("../Data_Collection/Headlines.csv", index_col=False)

ticker_headlines.columns = ['ticker', 'headlines']

ticker_headlines = ticker_headlines.drop_duplicates()

ticker_headlines.to_sql(table2, connection, if_exists="append", index=False)

connection.commit()
connection.close()
