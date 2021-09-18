#!/usr/bin/env python3

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Prepares data for model training
"""

import pandas as pd
import os


def get_data():
    """
    Returns the training data set required for the model development.
    """
    files = [f for f in os.listdir('Stocks') if f.endswith('.csv')]
    master_dict = {}
    company_dict = {}

    for file in files:
        if file == 'nyse_buy.csv' or file == 'nasdaq_buy.csv':
            df = pd.read_csv('Stocks/' + str(file))
            for index, row in df.iterrows():
                master_dict[row['Symbol']] = 1
                company_dict[row['Symbol']] = row['Name']
        else:
            df = pd.read_csv('Stocks/' + str(file))
            for index, row in df.iterrows():
                master_dict[row['Symbol']] = 0
                company_dict[row['Symbol']] = row['Name']

    master_df = pd.DataFrame(columns=['Symbol', 'Name', 'Buy'])

    for ticker in master_dict:
        ticker_row = {'Symbol': ticker, 'Name': company_dict[ticker], 'Buy': master_dict[ticker]}
        master_df = master_df.append(ticker_row, ignore_index=True)

    master_df.to_csv('recent_training_data.csv')


def main():
    get_data()


if __name__ == "__main__":
    main()

