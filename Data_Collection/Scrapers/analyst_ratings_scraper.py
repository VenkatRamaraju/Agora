#!/usr/bin/env python3

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Reads in Data of analyst ratings from CSV file
"""

# Libraries and Dependencies
import pandas as pd
from pathlib import Path


def get_analyst_ratings(stock):
    """
    Retrieves CSV (From files) of analyst ratings, prints the pandas dataframe generated from it.
    :param stock: Name of ticker for which analyst reviews are being generated
    """

    path = str(Path(__file__).resolve().parents[1]) + '/Analyst_Ratings/' + stock.upper() + '_Ratings.csv'
    ratings_dataframe = pd.read_csv(path)

    print(ratings_dataframe[['Analyst', 'Rating', 'Date']])
    print("\n\n")


def main():
    # Tickers and companies
    stocks = ["TSLA", "NFLX", "AAPL", "TWTR", "GME"]

    for stock in stocks:
        get_analyst_ratings(stock)


if __name__ == "__main__":
    main()
