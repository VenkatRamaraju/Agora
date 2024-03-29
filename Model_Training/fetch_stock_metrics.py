#!/usr/bin/env python
# coding: utf-8

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Prepares data for model training from the yFinance API
"""

import pandas
import yfinance as yf
import pandas as pd

all_comps = pd.read_csv("output_csvs/final_db.csv", index_col=0)


def get_stock_metrics(company_df: pandas.DataFrame):
    """
    Populates a dataset using metrics for a group of tickers.
    :param company_df: Dataframe with list of stock tickers for which metrics need to be queried
    """
    # Selected columns (From feature selection)
    new_columns = ['beta', 'profitMargins', 'forwardEps', 'bookValue', 'heldPercentInstitutions',
                   'shortRatio', 'shortPercentOfFloat']

    del company_df["Name"]
    del company_df["Buy"]
    del company_df["Analyst"]

    company_df = company_df.reindex(columns=company_df.columns.tolist() + new_columns)

    for column in new_columns:
        company_df[column] = None

    # Building the CSV
    for index, row in company_df.iterrows():
        ticker = yf.Ticker(row["Symbol"])
        print("Getting metrics for:", row["Symbol"])
        print()
        if ticker is not None:
            for col in new_columns:
                if col in ticker.info:
                    if ticker.info[col] is not None:
                        company_df.at[index, col] = round(ticker.info[col], 2)
                    else:
                        company_df.at[index, col] = None

    company_df.to_csv("stock_metric_data.csv")


def main():
    get_stock_metrics(all_comps)


if __name__ == "__main__":
    main()
