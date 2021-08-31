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
        df[column] = 0.0

    for index, row in df.iterrows():
        ticker = yf.Ticker(row['Ticker'])
        for col in new_columns:
            if col in ticker.info:
                df.at[index, col] = ticker.info[col]
            else:
                df.at[index, col] = None

    df.to_csv('training_data.csv')


def main():
    get_data()


if __name__ == "__main__":
    main()
