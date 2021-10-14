from bs4 import BeautifulSoup
import requests
import pprint
import re

# link: https://finance.yahoo.com/trending-tickers


def get_trending_stocks():
    url = "https://finance.yahoo.com/trending-tickers"

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all("a", class_="Fw(600) C($linkColor)")

    trending_stocks_list = []

    for company in table:
        title = company.get('title')\
            .replace(", Inc.", "")\
            .replace(" Inc.", "")\
            .replace(" Group", "")\
            .replace(" Company", "")\
            .replace(" Common Stock", "")\
            .replace(" Holdings", "")

        stock_dict = {
            'ticker': company.contents[0],
            'url': "https://finance.yahoo.com" + company.get('href'),
            'title': title
        }

        trending_stocks_list.append(stock_dict)

    return trending_stocks_list

