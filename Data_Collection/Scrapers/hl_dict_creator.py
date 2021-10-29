#!/usr/bin/env python3

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- methods to fetch headlines as a list from each news publication
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd

# Global data
nasdaq = pd.read_csv("nasdaq.csv", index_col=False)
nyse = pd.read_csv("nyse.csv", index_col=False)

nasdaq = nasdaq[['Symbol', 'Name']]
nyse = nyse[['Symbol', 'Name']]


# Each method below gathers and formats headlines for a specific stock ticker on a different website. At the end,
# is aggregated for sentiment analysis. We populate the dataset with the headline, and the link to it (so it can
# be clicked on in the interface).

def get_reuters_headlines(ticker: str):
    url = 'https://www.reuters.com/search/news?blob=' + ticker

    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page, 'lxml')

    h3_tags = soup.find_all('h3', class_='search-result-title')

    reuters_hls = []

    for h3 in h3_tags:
        try:
            a = h3.find('a')
            hl_dict = {
                "ticker": ticker,
                "title": a.contents[0].replace("&amp;", "").strip(),
                "url": "https://reuters.com" + a.get('href'),
                "publisher": "Reuters"
            }
            reuters_hls.append(hl_dict)
        except Exception as e:
            print("Reuters:", e)
            continue

    deduped = []
    temp_hls = []
    for i in reuters_hls:
        if i['title'] not in temp_hls:
            temp_hls.append(i['title'])
            deduped.append(i)

    return deduped


def get_morningstar_headlines(ticker):
    url = 'https://www.morningstar.com/stocks/xnas/' + ticker.lower() + '/news'

    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page, 'lxml')

    links = soup.find_all('a', class_="mdc-link mdc-news-module__headline mds-link mds-link--no-underline")

    ms_hls = []
    for link in links:
        try:
            href = link.get('href')
            title = link.contents[0].strip()
            hl_dict = {
                "ticker": ticker,
                "title": title.replace("&amp;", "").strip(),
                "url": "https://morningstar.com" + href,
                "publisher": "Morningstar"
            }

            ms_hls.append(hl_dict)
        except Exception as e:
            print("MS:", e)
            continue

    deduped = []
    temp_hls = []
    for i in ms_hls:
        if i['title'] not in temp_hls:
            temp_hls.append(i['title'])
            deduped.append(i)

    return deduped


def get_google_finance_headlines(ticker):
    url = ""
    if ticker in nasdaq.Symbol.values:
        url = 'https://www.google.com/finance/quote/' + ticker + ":NASDAQ"
    elif ticker in nyse.Symbol.values:
        url = 'https://www.google.com/finance/quote/' + ticker + ":NYSE"

    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page, 'lxml')

    sections = soup.find_all('div', class_='z4rs2b')

    gf_hls = []
    for sec in sections:
        try:
            link = sec.find('a', {'rel': 'noopener noreferrer'})
            title = link.find('div', class_='AoCdqe').contents[0].strip()

            hl_dict = {
                "ticker": ticker,
                "title": title.replace("\n", "").replace("&amp;", "").strip(),
                "url": link.get('href'),
                "publisher": "Google Finance"
            }

            gf_hls.append(hl_dict)
        except Exception as e:
            print("GF:", e)
            continue

    deduped = []
    temp_hls = []
    for i in gf_hls:
        if i['title'] not in temp_hls:
            temp_hls.append(i['title'])
            deduped.append(i)

    return deduped


def get_business_insider_headlines(ticker):
    url = 'https://markets.businessinsider.com/stocks/' + ticker.lower() + '-stock'

    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page, 'lxml')

    links = soup.find_all('a', class_="instrument-stories__link")

    bi_hls = []

    for link in links:
        try:
            hl_dict = {
                "ticker": ticker,
                "title": link.contents[0].replace("&amp;", "").strip(),
                "url": "https://markets.businessinsider.com" + link.get('href'),
                "publisher": "Business Insider"
            }

            bi_hls.append(hl_dict)
        except Exception as e:
            print("BI:", e)
            continue

    deduped = []
    temp_hls = []
    for i in bi_hls:
        if i['title'] not in temp_hls:
            temp_hls.append(i['title'])
            deduped.append(i)

    return deduped


def get_cnn_headlines(ticker):
    url = 'https://money.cnn.com/quote/news/news.html?symb=' + ticker

    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page, 'lxml')

    links = soup.find_all('a', class_="wsod_bold")

    cnn_hls = []

    for link in links:
        try:
            hl_dict = {
                "ticker": ticker,
                "title": link.contents[0].replace("&amp;", "").strip(),
                "url": link.get('href'),
                "publisher": "CNN"
            }

            cnn_hls.append(hl_dict)
        except Exception as e:
            print("CNN:", e)
            continue

    deduped = []
    temp_hls = []
    for i in cnn_hls:
        if i['title'] not in temp_hls:
            temp_hls.append(i['title'])
            deduped.append(i)

    return deduped


def get_yahoo_headlines(ticker):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/71.0.3578.98 Safari/537.36'}

    url = 'https://finance.yahoo.com/quote/' + ticker + '/news?p=' + ticker
    html_page = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_page, 'lxml')

    links = soup.find_all("a", 'js-content-viewer wafer-caas Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) Fz('
                               '17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 mega-item-header-link Td(n) '
                               'C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 '
                               'not-isInStreamVideoEnabled')

    yf_hls = []
    for link in links:
        try:
            hl_dict = {
                "ticker": ticker,
                "title": link.contents[2].replace("&amp;", "").strip(),
                "url": "https://finance.yahoo.com" + link.get('href'),
                "publisher": "Yahoo! Finance"
            }

            yf_hls.append(hl_dict)
        except Exception as e:
            print("YF:", e)
            continue

    return yf_hls


def get_cnbc_headlines(ticker):
    url = 'https://www.cnbc.com/quotes/?symbol=' + ticker.lower() + '&qsearchterm=' + ticker.lower() + '&tab=news'

    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page, 'lxml')

    links = soup.find_all("a", class_="LatestNews-headline")

    cnbc_hls = []
    for link in links:
        try:
            hl_dict = {
                "ticker": ticker,
                "title": link.contents[0].replace("&amp;", "").strip(),
                "url": link.get('href'),
                "publisher": "CNBC"
            }

            cnbc_hls.append(hl_dict)
        except Exception as e:
            print("CNBC:", e)
            continue

    return cnbc_hls

