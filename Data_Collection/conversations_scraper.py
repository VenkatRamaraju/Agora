#!/usr/bin/env python3

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Scraper that retrieves conversations from multiple online web sources
- Formats and outputs conversations in a Pandas table
"""

# Libraries and Dependencies
from headlines_scraper import get_soup, create_array, output
import numpy as np


def get_yahoo_conversations(stock):
    request = 'https://finance.yahoo.com/quote/' + stock + '/community?p=' + stock
    opinions = get_soup(request, 'div', 'C($c-fuji-grey-l) Mb(2px) Fz(14px) Lh(20px) Pend(8px)')
    return create_array(opinions)


def get_all_conversations(stock):
    """
    Gets conversations from various sources, concatenates the arrays of conversations, cleans up the text and returns
    the overall array.
    :param stock: Name of stock ticker.
    :return: Overall array of conversations from various sources after cleaning (Removal of punctuations).
    """
    # List of sources
    source_1 = np.array(get_yahoo_conversations(stock))

    return list(np.concatenate(source_1, axis=None))


def main():
    # Stock Ticker
    stock = 'TSLA'
    print("\nFetching conversations for " + stock + "...\n")

    overall_conversations = get_all_conversations(stock)
    output(overall_conversations, stock)


if __name__ == "__main__":
    main()
