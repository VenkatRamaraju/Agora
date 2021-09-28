import sqlite3
import pandas as pd
# pd.set_option("display.max_rows", None, "display.max_columns", None)

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

# ticker_info = pd.read_csv("../Model_Training/training_data.csv")
# ticker_comps = pd.read_csv("../Data_Collection/companies.csv")
# ticker_ar = pd.read_csv("../Data_Collection/Scrapers/Final_Analyst_Rating.csv")

new_ticker_info = pd.read_csv("../POC/finalized_stock_metrics_all.csv")
del new_ticker_info['Unnamed: 0']
del new_ticker_info['Name']
del new_ticker_info['Buy']
del new_ticker_info['Analyst']
print(new_ticker_info.columns)
# full_company_list = pd.read_csv("../POC/all_companies_w_preds.csv")

# print(new_ticker_info)
#
# del ticker_ar["Unnamed: 0"]
# del ticker_info["Unnamed: 0"]

################ OTHER SCRIPT SHIT ################
# del full_company_list["Unnamed: 0"]
# full_company_list.drop("Buy", 1)

# Reformat column names
# new_ticker_info = new_ticker_info[["Ticker", "Headlines", "Conversations", 'beta', 'profitMargins', 'forwardEps', 'bookValue', 'heldPercentInstitutions', 'shortRatio', 'shortPercentOfFloat']]
# ticker_info = ticker_info[["Ticker", "Headlines", "Conversations"]]
new_ticker_info.columns = ['ticker', 'beta', 'profit_margins', 'forward_eps', 'book_value',
                                   'held_percent_institutions', 'short_ratio', 'short_percent_of_float']

################ PUT THIS SHIT IN ANOTHER SCRIPT ################
# ticker_info.columns = ['ticker', 'headlines_polarity', 'conversations_polarity']
# full_company_list.columns = ['ticker', 'company_name', 'analyst_rating', 'agora_pred']
# ticker_comps.columns = ['ticker', 'company_name']
# ticker_ar.columns = ['ticker', 'analyst_rating']

# Merge columns into one DF
# ticker_info = pd.merge(ticker_info, ticker_comps, on=['ticker'], how='left')
# ticker_info = pd.merge(ticker_info, ticker_ar, on=['ticker'], how='left')

# print(ticker_info)

# Insert data into table
new_ticker_info.to_sql(table1, connection, if_exists="append", index=False)

connection.commit()

select_query = """select * from TickerStockMetrics"""
data = connection.execute(select_query)
print(data.fetchall())
connection.close()
