#!/usr/bin/env python3

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Scraper that retrieves conversations from multiple online web sources
- Formats and outputs conversations in a Pandas table
"""

# Libraries and Dependencies
import demoji
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from headlines_scraper import create_array
from pathlib import Path
import numpy as np

# Setup
demoji.download_codes()

def get_yahoo_conversations(stock):
    """
    Parses yahoo finance conversations page to get conversations related to the stock.
    """
    url = "https://finance.yahoo.com/quote/" + stock + "/community?p=" + stock

    # Selenium Web Driver to click load more button and continue to retrieve conversation
    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # Runs without opening browser
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)

    # Attempt to scroll as much as possible
    try:
        driver.get(url)
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        i = 0
        while i < 5:
            WebDriverWait(driver, 5, ignored_exceptions).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="canvass-0-CanvassApplet"]/div/button')))

            element = driver.find_element_by_xpath('//*[@id="canvass-0-CanvassApplet"]/div/button')
            driver.execute_script("arguments[0].click();", element)
            i += 1
    except Exception as e:
        print(e)

    # Retrieving soup after load more button is clicked
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()

    return create_array(soup.find_all('div', class_='C($c-fuji-grey-l) Mb(2px) Fz(14px) Lh(20px) Pend(8px)')), \
        create_array(soup.find_all('span', class_='Fz(12px) C(#828c93)'))


def get_all_conversations(stock):
    """
    Gets conversations from various sources, concatenates the arrays of conversations, cleans up the text and returns
    the overall array.
    :param stock: Name of stock ticker.
    :return: Overall array of conversations from various sources after cleaning (Removal of punctuations).
    """
    yahoo_conversations, yahoo_dates = get_yahoo_conversations(stock)
    yahoo_conversations = np.array(yahoo_conversations)
    yahoo_dates = np.array(yahoo_dates)

    return list(np.concatenate(yahoo_conversations, axis=None)), list(np.concatenate(yahoo_dates, axis=None))


def output(overall_data, stock):
    """
    Prints out the pandas dataframe after removing duplicates.
    :param overall_data: Array of headlines/conversations after retrieving from respective web sources, in text form.
    :param stock: Name of the stock for which all the above data is being retrieved.
    :return None.
    """

    # Removes duplicates by first converting to hash set (Stores only unique values), then converts back to list
    overall_data = list(set(overall_data))
    file_path = str(Path(__file__).resolve().parents[1]) + '/Conversations/' + stock.upper() + '_conversations.csv'

    if len(overall_data) > 0:
        # Formatting current dataframe, merging with previously existing (if it exists)
        title = 'Conversation'
        overall_dataframe = pd.DataFrame(overall_data, columns=[title])
        overall_dataframe[title] = overall_dataframe[title].apply(demoji.replace)
        overall_dataframe.to_csv(file_path, index=False)
    else:
        print("Invalid ticker/company or no headlines/conversations available.")


def main():
    # Tickers and companies
    stocks_df = pd.read_csv("../companies.csv")
    stocks_dict = {}

    for index, row in stocks_df.iterrows():
        stocks_dict.update(
            {row["Symbol"]: row["Company"]}
        )

    tickers = list(stocks_dict.keys())

    for stock in tickers:
        print("Getting conversations for:", stock)
        try:
            overall_conversations, dates = get_all_conversations(stock)
            output(overall_conversations, stock)
        except RuntimeError as e:
            print(e, "was handled")


if __name__ == "__main__":
    main()
