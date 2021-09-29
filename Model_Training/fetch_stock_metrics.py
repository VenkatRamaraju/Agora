import pandas
import yfinance as yf
import pandas as pd

all_comps = pd.read_csv("final_db.csv", index_col=0)


def get_stock_metrics(company_df: pandas.DataFrame):
    new_columns = ['beta', 'profitMargins', 'forwardEps', 'bookValue', 'heldPercentInstitutions',
                   'shortRatio', 'shortPercentOfFloat']

    company_df = company_df.reindex(columns=company_df.columns.tolist() + new_columns)

    for column in new_columns:
        company_df[column] = None

    for index, row in company_df.iterrows():
        ticker = yf.Ticker(row["Symbol"])
        print(ticker)
        if ticker is not None:
            for col in new_columns:
                if col in ticker.info:
                    company_df.at[index, col] = ticker.info[col]

    company_df.to_csv("finalized_stock_metrics_all.csv")


get_stock_metrics(all_comps)
