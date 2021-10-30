#!/usr/bin/env python3

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Scraper that retrieves headlines from multiple online web sources
- Formats and outputs headlines in a Pandas dataframe
"""

# Libraries and Dependencies
import pprint

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import yfinance as yf
import re
import hl_dict_creator

pd.set_option('display.max_columns', 7)

# Global Variables
overall_headlines_df = pd.DataFrame(columns=['Ticker', 'Headline', 'URL', 'Publisher'])
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
            result_array.append(str(' '.join(li.text.split())))  # Removes tabs, newlines, and gets text from HTML

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
    company = re.sub(r'[^\w\s]', '', name).strip()
    company_words = company.split(' ')

    # for weird edge cases like amazon
    for i in company_words:
        i.replace('.com', '')

    # Words to remove for comparison
    words_to_remove = ['a', 'and', 'the', 'company', 'incorporated', 'corporation', 'group', 'inc', 'common', 'stock']

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
    name = stocks_dict[stock]
    for entry in overall_array:
        if stock in str(entry) or contains_company_name(str(entry).lower(), name.lower()):
            cleaned_array.append(entry)

    return cleaned_array


def output(final_headlines_list, ticker):
    """
    Appends to overall dataframe to create the list of headlines.
    :param final_headlines_list: Array of headlines after retrieving from respective web sources, in text form.
    :param url: URL of website from where headlines were mined.
    :param publisher: Name of publisher that published the given set of headlines.
    :param stock: Name of the stock for which all the above data is being retrieved.
    :return None.
    """

    global overall_headlines_df
    if len(final_headlines_list) > 0:
        for hl in final_headlines_list:
            headline = hl[0]
            url = hl[1]
            publisher = hl[2]

            row = {'Ticker': ticker, 'Headline': headline, 'URL': url, 'Publisher': publisher}
            overall_headlines_df = overall_headlines_df.append(row, ignore_index=True)

# Each of the methods below retrieves the HTML text from the respective web page link and returns an array of the
# headlines on those webpages, leveraging all the above methods as subroutines.


def get_all_headlines(stock, company_name):
    """
    Gets headlines from various sources, concatenates the arrays of headlines, cleans up the text and returns the
    overall array.
    :param stock: Name of stock ticker.
    :return: Overall array of headlines from various sources after cleaning (Removal of punctuations).
    """

    print("\nParsing headlines for:", stock)

    # List of sources
    total_sources = []

    try:
        hl_list = hl_dict_creator.get_reuters_headlines(stock)
        for hl in hl_list:
            hl_tuple = (hl['title'], hl['url'], hl['publisher'])
            relevant = stock in hl['title'] or contains_company_name(hl['title'], company_name)
            # relevant = True
            if relevant:
                total_sources.append(hl_tuple)
    except Exception as e:
        print("reuters handled exception", e)

    try:
        hl_list = hl_dict_creator.get_cnbc_headlines(stock)
        for hl in hl_list:
            hl_tuple = (hl['title'], hl['url'], hl['publisher'])
            relevant = stock in hl['title'] or contains_company_name(hl['title'], company_name)
            # relevant = True
            if relevant:
                total_sources.append(hl_tuple)
    except Exception as e:
        print("cnbc handled exception", e)

    try:
        hl_list = hl_dict_creator.get_yahoo_headlines(stock)
        for hl in hl_list:
            hl_tuple = (hl['title'], hl['url'], hl['publisher'])
            relevant = stock in hl['title'] or contains_company_name(hl['title'], company_name)
            # relevant = True
            if relevant:
                total_sources.append(hl_tuple)
    except Exception as e:
        print("yahoo handled exception", e)

    try:
        hl_list = hl_dict_creator.get_cnn_headlines(stock)
        for hl in hl_list:
            hl_tuple = (hl['title'], hl['url'], hl['publisher'])
            relevant = stock in hl['title'] or contains_company_name(hl['title'], company_name)
            # relevant = True
            if relevant:
                total_sources.append(hl_tuple)
    except Exception as e:
        print("cnn handled exception", e)

    try:
        hl_list = hl_dict_creator.get_business_insider_headlines(stock)
        for hl in hl_list:
            hl_tuple = (hl['title'], hl['url'], hl['publisher'])
            relevant = stock in hl['title'] or contains_company_name(hl['title'], company_name)
            # relevant = True
            if relevant:
                total_sources.append(hl_tuple)
    except Exception as e:
        print("bi handled exception", e)

    try:
        hl_list = hl_dict_creator.get_google_finance_headlines(stock)
        for hl in hl_list:
            hl_tuple = (hl['title'], hl['url'], hl['publisher'])
            relevant = stock in hl['title'] or contains_company_name(hl['title'], company_name)
            # relevant = True
            if relevant:
                total_sources.append(hl_tuple)
    except Exception as e:
        print("gf handled exception", e)

    try:
        hl_list = hl_dict_creator.get_morningstar_headlines(stock)
        for hl in hl_list:
            hl_tuple = (hl['title'], hl['url'], hl['publisher'])
            relevant = stock in hl['title'] or contains_company_name(hl['title'], company_name)
            # relevant = True
            if relevant:
                total_sources.append(hl_tuple)
    except Exception as e:
        print("ms handled exception", e)

    return total_sources


def main():
    # Tickers and companies
    stocks_df = pd.read_csv("../companies.csv")
    global stocks_dict

    # Create dictionary with format {Ticker: Company Name}
    for index, row in stocks_df.iterrows():
        stocks_dict.update(
            {row["Symbol"]: row["Company"]}
        )

    # fetch headlines per ticker and append to overall_headlines_df
    for ticker, name in stocks_dict.items():
        output(get_all_headlines(ticker, name), ticker)

    # output to file
    overall_headlines_df.to_csv("../headlines.csv", index=False)


if __name__ == "__main__":
    main()
