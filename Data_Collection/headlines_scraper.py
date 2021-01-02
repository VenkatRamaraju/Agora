#!/usr/bin/env python3
"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Scraper that retrieves headlines from multiple online web sources
- Formats and outputs headlines in a Pandas table
"""

# Libraries and Dependencies
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import string
import demoji


def cleanup(line):
    """
    Removes all punctuations, emojis and returns the text in lower case. This cleanup is useful for making the semantics
    and meaning of the text more easily identifiable.
    :param line: Single headline that needs to be cleaned up.
    :return: Headline after removing punctuations, emojis and converting it to lower case.
    """
    cleaned_text = str.maketrans('', '', string.punctuation)
    cleaned_text = str(line.translate(cleaned_text)).lower()
    return demoji.replace(cleaned_text, '')


def get_soup(request, element, class_value):
    """
    Uses the BeautifulSoup library to retrieve the HTML text for a given webpage request.
    :param request: The webpage request for which the HTML text is to be retrieved.
    :param element: The element of the webpage. Ex: div, a, etc.
    :param class_value: The class of the element. Used to identify which parts of the HTML page are to be returned.
    :return: All instances of a given element and class (As an array).
    """
    html_page = requests.get(request).text
    soup = BeautifulSoup(html_page, 'lxml')
    return soup.find_all(element, class_=class_value)


def create_array(data_list):
    """
    Returns all texts from a given soup.
    :param data_list: Soup array with all headlines/conversations embedded as text.
    :return: Array of headlines/conversations, retrieved from the soup.
    """
    result_array = []
    for li in data_list:
        if li.text != "":
            result_array.append(' '.join(li.text.split()))  # Removes tabs, newlines, and gets text from HTML

    return result_array


def format_to_table(data_array, stock):
    """
    Formats a pandas table with all the headlines/conversations obtained from the provided web sources.
    :param data_array: Array with all headlines/conversations obtained from the provided web sources.
    :param stock: Name of the stock for which all the above data is being retrieved.
    :return: A pandas table with a single column, where each index is, sequentially, the elements of the data_array.
    """
    title = 'Recent headlines/conversations for ' + stock
    table = pd.DataFrame(columns=[title])

    for line in data_array:
        table = table.append({title: cleanup(line)}, ignore_index=True)

    return table


# Each of the methods below retrieves the HTML text from the respective web page link and returns an array, leveraging
# all the methods above as subroutines.

def get_morningstar_headlines(stock):
    request = 'https://www.morningstar.com/stocks/xnas/' + stock.lower() + '/news'
    headlines_list = get_soup(request, 'a', 'mdc-link mdc-news-module__headline mds-link mds-link--no-underline')
    return create_array(headlines_list)


def get_usa_today_headlines(stock):
    request = 'https://www.usatoday.com/search/?q=' + stock
    headlines_list = get_soup(request, 'a', 'gnt_se_a gnt_se_a__hd gnt_se_a__hi')
    return create_array(headlines_list)


def get_reuters_headlines(stock):
    request = 'https://www.reuters.com/search/news?blob=' + stock
    headlines_list = get_soup(request, 'h3', 'search-result-title')
    return create_array(headlines_list)


def get_google_finance_headlines(stock):
    request = 'https://www.google.com/finance/quote/' + stock + ':NASDAQ'
    headlines_list = get_soup(request, 'div', 'AoCdqe')
    return create_array(headlines_list)


def get_business_insider_headlines(stock):
    request = 'https://markets.businessinsider.com/stocks/' + stock.lower() + '-stock'
    headlines_list = get_soup(request, 'a', 'instrument-stories__link')
    return create_array(headlines_list)


def get_cnbc_headlines(stock):
    request = 'https://www.cnbc.com/quotes/?symbol=' + stock.lower() + '&qsearchterm=' + stock.lower() + '&tab=news'
    li_list = get_soup(request, 'div', 'assets')

    list_of_headlines = []
    for li in li_list:
        headline = li.select_one("span")
        if headline.text != "":
            list_of_headlines.append(headline.text)

    return list_of_headlines


def output(overall_data, stock):
    """
    Prints out the pandas table after removing duplicates.
    :param overall_data: Array of headlines/conversations after retrieving from respective web sources, in text form.
    :param stock: Name of the stock for which all the above data is being retrieved.
    :return None.
    """
    title = 'Recent headlines/conversations for ' + stock

    # Formatting to a table
    if len(overall_data) != 0:
        headlines_table = format_to_table(overall_data, stock)
    else:
        print("Invalid ticker or no headlines/conversations available.")
        return

    # Printing out formatted table of headlines
    headlines_table.drop_duplicates(subset=title, keep=False, inplace=True)
    print(headlines_table)


def main():
    # Stock Ticker
    stock = 'TSLA'
    print("\nFetching headlines for " + stock + "...\n")

    # List of sources
    source_1 = np.array(get_cnbc_headlines(stock))
    source_2 = np.array(get_reuters_headlines(stock))
    source_3 = np.array(get_morningstar_headlines(stock))
    source_4 = np.array(get_usa_today_headlines(stock))
    source_5 = np.array(get_google_finance_headlines(stock))
    source_6 = np.array(get_business_insider_headlines(stock))

    # Combining all sources, outputting the table
    overall_headlines = list(np.concatenate((source_1, source_2, source_3, source_4, source_5, source_6), axis=None))
    output(overall_headlines, stock)


if __name__ == "__main__":
    main()
