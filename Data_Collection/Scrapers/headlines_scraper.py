#!/usr/bin/env python3

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Scraper that retrieves headlines from multiple online web sources
- Formats and outputs headlines in a Pandas dataframe
"""

# Libraries and Dependencies
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import yfinance as yf
import re

# Global Variables
overall_headlines_df = pd.DataFrame(columns=['Ticker', 'Headline'])
stocks_dict = {}


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


def contains_company_name(headline, name):
    """
    Returns whether or not the headline contains the name of the company. This function is used to determine
    if a headline is relevant to the company.
    :param name: Name of the company for which the headlines have been scraped.
    :param headline: Headline from the internet. The company name will be searched in this headline.
    :return: True if the company name is in the headline, false otherwise.
    """
    # Remove punctuations and format into array
    company = re.sub(r'[^\w\s]', '', name).lower().strip()
    company_words = company.split(' ')

    # Words to remove for comparison
    words_to_remove = ['a', 'and', 'the', 'company', 'incorporated', 'corporation', 'group', 'inc']

    # Removing words
    for word in words_to_remove:
        if word in company_words:
            company_words.remove(word)

    # Removing empty words and formatting headline into array
    company_words = list(filter(None, company_words))
    headline_words = headline.split(' ')

    for word in company_words:
        if word in headline_words:  # Headline contains company name in it
            return True

    return False


def cleanup_array(overall_array, stock):
    """
    Cleans up the array of headlines by removing headlines that do not contain the stock ticker or company name in it.
    :param overall_array: Array of headlines/conversations from which data points need to be removed.
    :param stock: Ticker of the company for which the headlines have been scraped.
    :return: An array with data points that contain the company or stock in it.
    """

    if len(overall_array) < 15:
        return overall_array

    cleaned_array = []
    ticker = yf.Ticker(stock)
    name = stocks_dict[stock]
    for entry in overall_array:
        if stock in str(entry) or contains_company_name(str(entry).lower(), name.lower()):
            cleaned_array.append(entry)

    return cleaned_array


def output(overall_data, stock):
    """
    Appends to overall dataframe to create the list of headlines.
    :param overall_data: Array of headlines/conversations after retrieving from respective web sources, in text form.
    :param stock: Name of the stock for which all the above data is being retrieved.
    :return None.
    """

    global overall_headlines_df
    if len(overall_data) > 0:
        for headline in overall_data:
            row = {'Ticker': stock, 'Headline': headline}
            overall_headlines_df = overall_headlines_df.append(row, ignore_index=True)
    else:
        print("Invalid ticker/company or no headlines/conversations available.")


# Each of the methods below retrieves the HTML text from the respective web page link and returns an array of the
# headlines on those webpages, leveraging all the above methods as subroutines.

def get_morningstar_headlines(stock):
    request = 'https://www.morningstar.com/stocks/xnas/' + stock.lower() + '/news'
    return create_array(get_soup(request, 'a', 'mdc-link mdc-news-module__headline mds-link mds-link--no-underline'))


def get_usa_today_headlines(stock):
    request = 'https://www.usatoday.com/search/?q=' + stock
    return create_array(get_soup(request, 'a', 'gnt_se_a gnt_se_a__hd gnt_se_a__hi'))


def get_reuters_headlines(stock):
    request = 'https://www.reuters.com/search/news?blob=' + stock
    return create_array(get_soup(request, 'h3', 'search-result-title'))


def get_google_finance_headlines(stock):
    request = 'https://www.google.com/finance/quote/' + stock + ':NASDAQ'
    return create_array(get_soup(request, 'div', 'AoCdqe'))


def get_business_insider_headlines(stock):
    request = 'https://markets.businessinsider.com/stocks/' + stock.lower() + '-stock'
    return create_array(get_soup(request, 'a', 'instrument-stories__link'))


def get_cnn_headlines(stock):
    request = 'https://money.cnn.com/quote/news/news.html?symb=' + stock
    return create_array(get_soup(request, 'a', 'wsod_bold'))


def get_yahoo_headlines(stock):
    request = 'https://finance.yahoo.com/quote/' + stock + '/news?p=' + stock
    return create_array(get_soup(request, 'a', 'js-content-viewer wafer-caas Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) '
                                               'Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 '
                                               'mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) '
                                               'LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled'))


def get_cnbc_headlines(stock):
    request = 'https://www.cnbc.com/quotes/?symbol=' + stock.lower() + '&qsearchterm=' + stock.lower() + '&tab=news'
    li_list = get_soup(request, 'div', 'assets')

    list_of_headlines = []
    for li in li_list:
        headline = li.select_one("span")
        if headline.text != "":
            list_of_headlines.append(headline.text)

    return list_of_headlines


def get_all_headlines(stock):
    """
    Gets headlines from various sources, concatenates the arrays of headlines, cleans up the text and returns the
    overall array.
    :param stock: Name of stock ticker.
    :return: Overall array of headlines from various sources after cleaning (Removal of punctuations).
    """

    print("\nParsing headlines for:", stock)

    # List of sources
    source_1 = np.array([])
    source_2 = np.array([])
    source_3 = np.array([])
    source_4 = np.array([])
    source_5 = np.array([])
    source_6 = np.array([])
    source_7 = np.array([])
    source_8 = np.array([])

    try:
        source_1 = np.array(get_cnbc_headlines(stock))
    except RuntimeError as e:
        print(e, "was handled")

    try:
        source_2 = np.array(get_reuters_headlines(stock))
    except RuntimeError as e:
        print(e, "was handled")

    try:
        source_3 = np.array(get_morningstar_headlines(stock))
    except RuntimeError as e:
        print(e, "was handled")

    try:
        source_4 = np.array(get_usa_today_headlines(stock))
    except RuntimeError as e:
        print(e, "was handled")

    try:
        source_5 = np.array(get_google_finance_headlines(stock))
    except RuntimeError as e:
        print(e, "was handled")

    try:
        source_6 = np.array(get_business_insider_headlines(stock))
    except RuntimeError as e:
        print(e, "was handled")

    try:
        source_7 = np.array(get_cnn_headlines(stock))
    except RuntimeError as e:
        print(e, "was handled")

    try:
        source_8 = np.array(get_yahoo_headlines(stock))
    except RuntimeError as e:
        print(e, "was handled")

    # source_2 = np.array(get_reuters_headlines(stock))
    # source_3 = np.array(get_morningstar_headlines(stock))
    # source_4 = np.array(get_usa_today_headlines(stock))
    # source_5 = np.array(get_google_finance_headlines(stock))
    # source_6 = np.array(get_business_insider_headlines(stock))
    # source_7 = np.array(get_cnn_headlines(stock))
    # source_8 = np.array(get_yahoo_headlines(stock))

    # Combine all sources, clean up the array
    total_headlines = list(np.concatenate((source_1, source_2, source_3, source_4, source_5, source_6, source_7,
                                           source_8), axis=None))

    return cleanup_array(total_headlines, stock)


def main():
    # Tickers and companies

    stocks_df = pd.read_csv("../companies.csv")
    global stocks_dict

    for index, row in stocks_df.iterrows():
        stocks_dict.update(
            {row["Symbol"]: row["Company"]}
        )

    tickers = list(stocks_dict.keys())

    for i in range(0, len(tickers)):
        try:
            total_headlines = get_all_headlines(tickers[i])

            # Combining data and output to CSV
            output(total_headlines, tickers[i])
        except RuntimeError as e:
            print(e, "was handled")

    overall_headlines_df.drop_duplicates(subset=None, keep='first', inplace=True)
    overall_headlines_df.to_csv('../Headlines.csv', index=False)


if __name__ == "__main__":
    main()
