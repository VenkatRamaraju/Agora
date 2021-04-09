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


def analyst_ratings_scraper(stock):
    analyst_ratings = pd.read_html('https://www.benzinga.com/stock/' + stock.lower() + '/ratings')
    return analyst_ratings[0]['Current'].value_counts().idxmax()


def build_analyst_csv():
    stocks = ["QCOM", "GE", "PLTR", "AAPL", "COST", "CSCO", "DIS", "FB", "GE", "GOOGL", "INTC", "JNJ", "MSFT",
              "NFLX", "NKE", "NVDA", "PLTR", "PYPL", "QCOM", "T", "TSLA", "TWTR", "VZ"]

    df = pd.DataFrame(columns=['Ticker', 'Rating'])
    for stock in stocks:
        df = df.append({'Ticker': stock, 'Rating': analyst_ratings_scraper(stock)}, ignore_index=True)

    df.to_csv('Final_Analyst_Rating.csv')


def main():
    build_analyst_csv()


if __name__ == "__main__":
    main()
