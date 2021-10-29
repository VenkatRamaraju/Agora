#!/usr/bin/env python3

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Prepares data for model training
"""

# Imports and dependencies
import pandas as pd
import os


def get_data():
    """
    Returns the training data set required for the model development.
    """
    files = [f for f in os.listdir('Stocks') if f.endswith('.csv')]
    master_dict = {}
    company_dict = {}
    analyst_dict = {}
    training_df = pd.DataFrame(columns=['Symbol', 'Name', 'Buy'])

    # Building training dataset based on the NASDAQ predictions (in Stocks/ directory).
    for file in files:
        if file == 'nasdaq_strong_buy.csv' or file == 'nyse_strong_buy.csv':
            df = pd.read_csv('Stocks/' + str(file))
            for index, row in df.iterrows():
                master_dict[row['Symbol']] = 1
                analyst_dict[row['Symbol']] = "Strong Buy"
                company_dict[row['Symbol']] = row['Name']
        elif file == 'nasdaq_buy.csv' or file == 'nyse_buy.csv':
            df = pd.read_csv('Stocks/' + str(file))
            for index, row in df.iterrows():
                master_dict[row['Symbol']] = 1
                analyst_dict[row['Symbol']] = "Buy"
                company_dict[row['Symbol']] = row['Name']
        elif file == 'nasdaq_hold.csv' or file == 'nyse_hold.csv':
            df = pd.read_csv('Stocks/' + str(file))
            for index, row in df.iterrows():
                master_dict[row['Symbol']] = 0
                analyst_dict[row['Symbol']] = "Hold"
                company_dict[row['Symbol']] = row['Name']

                training_row = {'Symbol': row['Symbol'], 'Name': company_dict[row['Symbol']],
                                'Buy': master_dict[row['Symbol']], 'Analyst': analyst_dict[row['Symbol']]}
                training_df = training_df.append(training_row, ignore_index=True)
        elif file == 'nasdaq_sell.csv' or file == 'nyse__sell.csv':
            df = pd.read_csv('Stocks/' + str(file))
            for index, row in df.iterrows():
                master_dict[row['Symbol']] = 0
                analyst_dict[row['Symbol']] = "Sell"
                company_dict[row['Symbol']] = row['Name']

                training_row = {'Symbol': row['Symbol'], 'Name': company_dict[row['Symbol']],
                                'Buy': master_dict[row['Symbol']], 'Analyst': analyst_dict[row['Symbol']]}
                training_df = training_df.append(training_row, ignore_index=True)
        elif file == 'nasdaq_strong_sell.csv' or file == 'nyse_strong_sell.csv':
            df = pd.read_csv('Stocks/' + str(file))
            for index, row in df.iterrows():
                master_dict[row['Symbol']] = 0
                analyst_dict[row['Symbol']] = "Strong Sell"
                company_dict[row['Symbol']] = row['Name']

                training_row = {'Symbol': row['Symbol'], 'Name': company_dict[row['Symbol']],
                                'Analyst_Numeric': master_dict[row['Symbol']], 'Analyst_String': analyst_dict[row['Symbol']]}
                training_df = training_df.append(training_row, ignore_index=True)

    master_df = pd.DataFrame(columns=['Symbol', 'Name', 'Buy', 'Analyst'])

    for ticker in master_dict:
        db_row = {'Symbol': ticker, 'Name': company_dict[ticker], 'Buy': master_dict[ticker],
                  'Analyst': analyst_dict[ticker]}
        master_df = master_df.append(db_row, ignore_index=True)

    russell_df = pd.read_csv('Russell.csv')
    for index, row in russell_df.iterrows():
        if row['Symbol'] in master_dict:
            if analyst_dict[row['Symbol']] is 'Buy' or analyst_dict[row['Symbol']] is 'Strong Buy':
                training_row = {'Symbol': row['Symbol'], 'Name': company_dict[row['Symbol']], 'Buy': master_dict[row['Symbol']],
                      'Analyst': analyst_dict[row['Symbol']]}
                training_df = training_df.append(training_row, ignore_index=True)

    # Final training datasets
    master_df.to_csv('final_db.csv')
    training_df.to_csv('companies.csv')


def main():
    get_data()


if __name__ == "__main__":
    main()

