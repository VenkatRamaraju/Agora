#!/usr/bin/env python3

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Reads in Data of analyst ratings from CSV file
"""

# Libraries and Dependencies
import pandas as pd


def analyst_ratings_scraper(stock):
    """
    Parses Benzinga's analyst ratings and returns the highest voted analyst rating
    """
    analyst_ratings = pd.read_html('https://www.benzinga.com/stock/' + stock.lower() + '/ratings')
    return analyst_ratings[0]['Current'].value_counts().idxmax()


def build_analyst_csv():
    """
    Builds the dataframe for all stock tickers in companies.csv
    """
    stocks_df = pd.read_csv("../companies.csv")
    stocks_dict = {}

    for index, row in stocks_df.iterrows():
        stocks_dict.update(
            {row["Symbol"]: row["Company"]}
        )

    stocks = list(stocks_dict.keys())

    # Output to csv
    df = pd.DataFrame(columns=['Ticker', 'Rating'])
    for stock in stocks:
        df = df.append({'Ticker': stock, 'Rating': analyst_ratings_scraper(stock)}, ignore_index=True)

    df.to_csv('Final_Analyst_Rating.csv')


def main():
    build_analyst_csv()


if __name__ == "__main__":
    main()
