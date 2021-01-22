#!/usr/bin/env python3

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Reads in Data of analyst ratings from CSV file
"""

# Libraries and Dependencies
import pandas as pd


def get_analyst_ratings(stock):
    """
    Retrieves CSV (From files) of analyst ratings, prints the pandas dataframe generated from it.
    :param stock: Name of ticker for which analyst reviews are being generated
    """

    path = '../Analyst_Ratings/' + stock.upper() + '_Ratings.csv'
    ratings_dataframe = pd.read_csv(path)

    print(ratings_dataframe)


def main():
    stock = 'NFLX'
    get_analyst_ratings(stock)


if __name__ == "__main__":
    main()
