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


def format_to_dataframe(data_array, stock):
    """
    Formats a pandas dataframe with all the headlines/conversations obtained from the provided web sources.
    :param data_array: Array with all headlines/conversations obtained from the provided web sources.
    :param stock: Name of the stock for which all the above data is being retrieved.
    :return: A pandas dataframe with a single column, where each index is, sequentially, the elements of the data_array.
    """
    title = 'Recent headlines/conversations for ' + stock
    dataframe = pd.DataFrame(columns=[title])

    for line in data_array:
        dataframe = dataframe.append({title: cleanup(line)}, ignore_index=True)

    return dataframe


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


def output(overall_data, stock):
    """
    Prints out the pandas dataframe after removing duplicates.
    :param overall_data: Array of headlines/conversations after retrieving from respective web sources, in text form.
    :param stock: Name of the stock for which all the above data is being retrieved.
    :return None.
    """
    title = 'Recent headlines/conversations for ' + stock

    # Formatting to a dataframe
    if len(overall_data) != 0:
        overall_dataframe = format_to_dataframe(overall_data, stock)
    else:
        print("Invalid ticker or no headlines/conversations available.")
        return

    overall_dataframe.drop_duplicates(subset=title, keep=False, inplace=True)
    print(overall_dataframe)


# Each of the methods below retrieves the HTML text from the respective web page link and returns an array of the
# headlines on those webpages, leveraging all the above methods as subroutines.

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


def get_cnn_headlines(stock):
    request = 'https://money.cnn.com/quote/news/news.html?symb=' + stock
    headlines_list = get_soup(request, 'a', 'wsod_bold')
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


def main():
    # Ticker and company
    stock = 'TSLA'
    company = 'tesla'
    print("\nFetching headlines for " + stock + "...\n")

    # List of sources
    source_1 = np.array(get_cnbc_headlines(stock))
    source_2 = np.array(get_reuters_headlines(stock))
    source_3 = np.array(get_morningstar_headlines(stock))
    source_4 = np.array(get_usa_today_headlines(stock))
    source_5 = np.array(get_google_finance_headlines(stock))
    source_6 = np.array(get_business_insider_headlines(stock))
    source_7 = np.array(get_cnn_headlines(stock))

    # Combining all sources, cleaning up data and outputting the dataframe
    total_headlines = list(np.concatenate((source_1, source_2, source_3, source_4, source_5, source_6, source_7),
                                          axis=None))
    total_headlines = cleanup_array(total_headlines, stock, company)
    output(total_headlines, stock)


if __name__ == "__main__":
    main()
