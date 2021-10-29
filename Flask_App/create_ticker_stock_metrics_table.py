import sqlite3
import pandas as pd

pd.set_option('display.max_columns', None)

connection = sqlite3.connect('database.db')
cur = connection.cursor()

table1 = "TickerStockMetrics"

init_cleanup = f"""drop table if exists {table1};"""

cur.execute(init_cleanup)

table1_sql = f"""create table {table1}(
    ticker text,
    beta float,
    profit_margins float,
    forward_eps float,
    book_value float,
    held_percent_institutions float,
    short_ratio float,
    short_percent_of_float float,
    foreign key (ticker) references TickerPredictions(ticker)
)"""

cur.execute(table1_sql)

new_ticker_info = pd.read_csv("../Model_Training/finalized_stock_metrics_all.csv")
del new_ticker_info['Unnamed: 0']
del new_ticker_info['Name']
del new_ticker_info['Buy']
del new_ticker_info['Analyst']

# Reformat column names
new_ticker_info.columns = ['ticker', 'beta', 'profit_margins', 'forward_eps', 'book_value',
                           'held_percent_institutions', 'short_ratio', 'short_percent_of_float']

new_ticker_info = new_ticker_info.round({
    'beta': 2,
    'profit_margins': 2,
    'forward_eps': 2,
    'book_value': 2,
    'held_percent_institutions': 2,
    'short_ratio': 2,
    'short_percent_of_float': 2
})

# Insert data into table
new_ticker_info.to_sql(table1, connection, if_exists="append", index=False)

connection.commit()

select_query = """select * from TickerStockMetrics"""
data = connection.execute(select_query)
connection.close()
