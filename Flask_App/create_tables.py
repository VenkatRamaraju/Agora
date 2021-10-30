import sqlite3
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)

# Combined script for creating tables


def create_headlines_table(connection, cur):
    # creates headlines table
    table2 = "TickerHeadlines"

    init_cleanup = f"""drop table if exists {table2};"""

    cur.execute(init_cleanup)

    table2_sql = f"""create table {table2}(
        headline text,
        ticker text not null,
        url text,
        publisher text,
        foreign key (ticker) references TickerPredictions(ticker)
    )"""

    cur.execute(table2_sql)

    ticker_headlines = pd.read_csv("../Data_Collection/headlines.csv", index_col=False)

    ticker_headlines.columns = ['ticker', 'headline', 'url', 'publisher']

    ticker_headlines = ticker_headlines.drop_duplicates()

    ticker_headlines.to_sql(table2, connection, if_exists="append", index=False)

    connection.commit()


def create_ticker_preds_table(connection, cur):
    # creates Ticker Predictions Table
    table = "TickerPredictions"

    init_cleanup = f"""drop table if exists {table};"""

    cur.execute(init_cleanup)

    table2_sql = f"""create table {table}(
        ticker text primary key,
        company_name text,
        analyst_pred text,
        agora_pred float,
        headline_polarity float,
        conversation_polarity float
    )"""

    cur.execute(table2_sql)

    ticker_predictions = pd.read_csv("../Model_Training/output_csvs/final_dataset.csv", index_col=False)

    del ticker_predictions["Unnamed: 0"]
    del ticker_predictions["Unnamed: 0.1"]
    del ticker_predictions["Buy"]
    del ticker_predictions["beta"]
    del ticker_predictions["profitMargins"]
    del ticker_predictions["forwardEps"]
    del ticker_predictions["bookValue"]
    del ticker_predictions["heldPercentInstitutions"]
    del ticker_predictions["shortRatio"]
    del ticker_predictions["shortPercentOfFloat"]

    print(ticker_predictions.columns)

    ticker_predictions.columns = ['ticker', 'company_name', 'analyst_pred', 'headline_polarity',
                                  'conversation_polarity', 'agora_pred']

    ticker_predictions.to_sql(table, connection, if_exists="append", index=False)

    connection.commit()


def create_stock_metrics_table(connection, cur):
    # creates stock metrics table
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

    new_ticker_info = pd.read_csv("../Model_Training/output_csvs/final_dataset.csv")
    del new_ticker_info['Unnamed: 0']
    del new_ticker_info['Unnamed: 0.1']
    del new_ticker_info['headline_polarity']
    del new_ticker_info['convo_polarity']
    del new_ticker_info['Name']
    del new_ticker_info['Buy']
    del new_ticker_info['Analyst']
    del new_ticker_info["agora_pred"]

    print(new_ticker_info.columns)

    # Reformat column names
    new_ticker_info.columns = ['ticker', 'beta', 'profit_margins', 'forward_eps', 'book_value',
                               'held_percent_institutions', 'short_ratio', 'short_percent_of_float']

    # new_ticker_info = new_ticker_info.round({
    #     'beta': 2,
    #     'profit_margins': 2,
    #     'forward_eps': 2,
    #     'book_value': 2,
    #     'held_percent_institutions': 2,
    #     'short_ratio': 2,
    #     'short_percent_of_float': 2
    # })

    # Insert data into table
    new_ticker_info.to_sql(table1, connection, if_exists="append", index=False)

    connection.commit()


def main():
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()

    create_ticker_preds_table(connection, cur)
    create_headlines_table(connection, cur)
    create_stock_metrics_table(connection, cur)

    connection.close()


if __name__ == "__main__":
    main()