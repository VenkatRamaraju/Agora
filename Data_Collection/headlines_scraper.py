# Libraries and Dependencies
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def cleanup(line):
    cleaned_text = str.maketrans('', '', r"-()\"#/@;:<>{}-=~|.?,")
    line = line.translate(cleaned_text)

    return str(line).lower()


def format_to_table(headlines, stock):
    title = 'Recent headlines for ' + stock
    headlines_table = pd.DataFrame(columns=[title])

    for line in headlines:
        headlines_table = headlines_table.append({title: cleanup(line)}, ignore_index=True)

    return headlines_table


def get_morningstar_headlines(stock):
    html_page = requests.get('https://www.morningstar.com/stocks/xnas/' + stock.lower() + '/news').text

    list_of_headlines = []
    soup = BeautifulSoup(html_page, 'lxml')
    headlines_list = soup.find_all('a', class_='mdc-link mdc-news-module__headline mds-link mds-link--no-underline')

    for li in headlines_list:
        list_of_headlines.append(' '.join(li.text.split()))

    return list_of_headlines


def get_reuters_headlines(stock):
    html_page = requests.get('https://www.reuters.com/search/news?blob=' + stock).text

    list_of_headlines = []
    soup = BeautifulSoup(html_page, 'lxml')
    headlines_list = soup.find_all('h3', class_='search-result-title')

    for li in headlines_list:
        list_of_headlines.append(li.text)

    return list_of_headlines


def get_cnbc_headlines(stock):
    html_page = requests.get('https://www.cnbc.com/quotes/?symbol=' + stock.lower() +
                             '&qsearchterm=' + stock.lower() + '&tab=news').text

    list_of_headlines = []
    soup = BeautifulSoup(html_page, 'lxml')
    li_list = soup.find_all('div', class_='assets')

    for li in li_list:
        headline = li.select_one("span")
        if headline.text != "":
            list_of_headlines.append(headline.text)

    return list_of_headlines


def main():
    # Stock Ticker
    stock = 'BABA'
    title = 'Recent headlines for ' + stock
    print("\nFetching headlines for " + stock + "...\n")

    # List of sources
    source_1 = np.array(get_cnbc_headlines(stock))
    source_2 = np.array(get_reuters_headlines(stock))
    source_3 = np.array(get_morningstar_headlines(stock))

    # Combining all sources, initializing data frame
    overall_headlines = np.concatenate((source_1, source_2, source_3), axis=None)
    overall_headlines = list(overall_headlines)
    headlines_table = pd.DataFrame(columns=[title])

    # Formatting to a table
    if len(overall_headlines) != 0:
        headlines_table = format_to_table(overall_headlines, stock)
    else:
        print("Invalid ticker or no headlines available.")

    # Printing out formatted table of headlines
    headlines_table.drop_duplicates(subset=title, keep=False, inplace=True)
    print(headlines_table)


if __name__ == "__main__":
    main()
