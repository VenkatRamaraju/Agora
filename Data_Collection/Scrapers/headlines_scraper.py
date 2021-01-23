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
import string
import demoji
from os import path
from pathlib import Path


def cleanup_text(line):
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


def cleanup_array(overall_array, stock, company):
    """
    Cleans up the array of headlines/conversations by removing headlines that do not contain the stock ticker or
    company name in it.
    :param overall_array: Array of headlines/conversations from which data points need to be removed.
    :param stock: Ticker of the company for which the headlines have been scraped.
    :param company: Name of the company for which the headlines have been scraped.
    :return: An array with data points that contain the company or stock in it.
    """

    cleaned_array = []
    for entry in overall_array:
        if stock.lower() in str(entry).lower() or company.lower() in str(entry).lower():
            cleaned_array.append(entry)

    return cleaned_array


def output(overall_data, stock, category):
    """
    Prints out the pandas dataframe after removing duplicates.
    :param overall_data: Array of headlines/conversations after retrieving from respective web sources, in text form.
    :param stock: Name of the stock for which all the above data is being retrieved.
    :param category: Headlines or Conversations
    :return None.
    """

    # Removes duplicates by first converting to hash set (Stores only unique values), then converts back to list
    overall_data = list(set(overall_data))
    file_path = str(Path(__file__).resolve().parents[1]) + '/CSV_Results/' + stock.upper() + '_' + \
        category.lower() + '_results.csv'

    if len(overall_data) > 0:
        # Formatting current dataframe, merging with previously existing (if it exists)
        title = 'Recent headlines and conversations for ' + stock
        overall_dataframe = pd.DataFrame(overall_data, columns=[title])
        overall_dataframe[title] = overall_dataframe[title].apply(cleanup_text)
        current_dataframe = pd.DataFrame(columns=[title])
        if path.exists(file_path):
            current_dataframe = pd.read_csv(file_path)

        # Appending to CSV, or creating new one for stock
        overall_dataframe = pd.concat([overall_dataframe, current_dataframe], ignore_index=True)
        overall_dataframe.drop_duplicates(subset=title, inplace=True)
        overall_dataframe.to_csv(file_path, index=False)
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


def get_all_headlines(stock, company):
    """
    Gets headlines from various sources, concatenates the arrays of headlines, cleans up the text and returns the
    overall array.
    :param stock: Name of stock ticker.
    :param company: Name of company.
    :return: Overall array of headlines from various sources after cleaning (Removal of punctuations).
    """

    # List of sources
    source_1 = np.array(get_cnbc_headlines(stock))
    source_2 = np.array(get_reuters_headlines(stock))
    source_3 = np.array(get_morningstar_headlines(stock))
    source_4 = np.array(get_usa_today_headlines(stock))
    source_5 = np.array(get_google_finance_headlines(stock))
    source_6 = np.array(get_business_insider_headlines(stock))
    source_7 = np.array(get_cnn_headlines(stock))
    source_8 = np.array(get_yahoo_headlines(stock))

    # Combine all sources, clean up the array
    total_headlines = list(np.concatenate((source_1, source_2, source_3, source_4, source_5, source_6, source_7,
                                           source_8), axis=None))

    return cleanup_array(total_headlines, stock, company)


def main():
    # Tickers and companies
    stocks = ["TSLA", "NFLX", "AAPL"]
    companies = ['tesla', 'netflix', 'apple']

    for i in range(0, len(stocks)):
        total_headlines = get_all_headlines(stocks[i], companies[i])

        # Combining data and output to CSV
        output(total_headlines, stocks[i], "headlines")


if __name__ == "__main__":
    main()
