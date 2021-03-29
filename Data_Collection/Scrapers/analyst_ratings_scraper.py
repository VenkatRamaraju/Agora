#!/usr/bin/env python3

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Reads in Data of analyst ratings from CSV file
"""

# Libraries and Dependencies
import pandas as pd
from pathlib import Path
import os


def get_analyst_ratings():
    """
    Retrieves CSV (From files) of analyst ratings, prints the pandas dataframe generated from it.
    """

    # Tickers and companies

    stocks = [f for f in os.listdir('../Analyst_Ratings')]
    for stock in stocks:
        path = str(Path(__file__).resolve().parents[1]) + '/Analyst_Ratings/' + stock
        ratings_dataframe = pd.read_csv(path, index_col=0)

        print(ratings_dataframe[['Analyst', 'Rating', 'Date']])
        print("\n\n")


def main():
    get_analyst_ratings()


if __name__ == "__main__":
    main()
