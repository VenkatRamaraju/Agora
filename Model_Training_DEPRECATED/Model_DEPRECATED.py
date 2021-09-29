#!/usr/bin/env python3

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Prepares data for model training
"""

import pandas as pd
import yfinance as yf


def get_data():
    """
    Returns the training data set required for the model development.
    """
    df = pd.read_csv('../Polarity_Analysis/aggregated_polarities.csv', index_col=0)
    new_columns = ['payoutRatio', 'beta', 'regularMarketVolume', 'profitMargins', '52WeekChange',
                   'forwardEps', 'bookValue', 'sharesShort', 'sharesPercentSharesOut', 'trailingEps',
                   'heldPercentInstitutions', 'heldPercentInsiders', 'mostRecentQuarter', 'nextFiscalYearEnd',
                   'shortRatio', 'enterpriseValue', 'earningsQuarterlyGrowth', 'sharesShortPriorMonth',
                   'shortPercentOfFloat', 'pegRatio']

    df = df.reindex(columns=df.columns.tolist() + new_columns)

    for column in new_columns:
        df[column] = None

    for index, row in df.iterrows():
        ticker = yf.Ticker(row['Ticker'])
        print(ticker)
        if ticker is not None:
            for col in new_columns:
                if col in ticker.info:
                    df.at[index, col] = ticker.info[col]

    df.to_csv('final_training_data.csv')


def add_analyst_rating():
    buy_dict = {}
    df = pd.read_csv('../Data_Collection/companies.csv', index_col=0)
    for index, row in df.iterrows():
        buy_dict[row['Symbol']] = row['Buy']

    training_df = pd.read_csv('final_overall_training_data.csv')
    training_df['Buy'] = -1

    for index, row in training_df.iterrows():
        training_df.at[index, 'Buy'] = buy_dict[row['Ticker']]

    training_df.to_csv('overall_training_data.csv', index=False)


def main():
    get_data()
    add_analyst_rating()


if __name__ == "__main__":
    main()
