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
    print(files)

    for file in files:
        if file == 'buy.csv':
            df = pd.read_csv('Stocks/buy.csv')
            for index, row in df.iterrows():
                master_dict[row['Symbol']] = 1
        else:
            df = pd.read_csv('Stocks/' + str(file))
            for index, row in df.iterrows():
                master_dict[row['Symbol']] = 0

    training_df = pd.read_csv('training_data.csv', index_col=0)
    training_df['Buy'] = -1

    for index, row in training_df.iterrows():
        training_df.at[index, 'Buy'] = master_dict[row['Ticker']]

    training_df.to_csv('recent_training_data.csv')


def main():
    get_data()


if __name__ == "__main__":
    main()

