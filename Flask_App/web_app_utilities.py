import requests
from bs4 import BeautifulSoup

# Contains utilities for fetching latest Stock price and
# getting the trending stocks from Yahoo Finance


def get_last_price(ticker):
    # retrieves the latest price for a given ticker through the Financial Content API
    url = "http://feeds.financialcontent.com/JSQuote?Ticker=" + ticker
    stuff = requests.get(url).text

    start_cp = stuff.find("Last:") + len("Last:")
    end_cp = stuff.find("Open:")

    start_op = stuff.find("Open:") + len("Open:")
    end_op = stuff.find("High:")

    open_price = stuff[start_op:end_op]
    current_price = stuff[start_cp:end_cp]

    current_price = current_price.strip().replace(",", "")
    open_price = open_price.strip().replace(",", "")

    ex_name_start = stuff.find("ExchangeName:") + len("ExchangeName:")
    ex_name_end = stuff.find("ExchangeShortName:")

    exchange = stuff[ex_name_start:ex_name_end]
    exchange = exchange.strip().replace(",", "").replace("'", "")

    if exchange == "Nasdaq Stock Market":
        exchange = "NASDAQ"
    else:
        exchange = "NYSE"

    diff = float(current_price) - float(open_price)

    if diff > 0:
        color = "#006400"
    elif diff < 0:
        color = "#8b0000"
    else:
        color = "#949494"

    stock_dict = {
        "current_price": format(float(current_price), '.2f'),
        "exchange": exchange,
        "color": color
    }

    return stock_dict


def get_trending_stocks():
    url = "https://finance.yahoo.com/trending-tickers"

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all("a", class_="Fw(600) C($linkColor)")
    table_2 = soup.find_all("td", {'class': 'Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)', 'aria-label': 'Last Price'})

    trending_stocks_list = []

    for i in range(len(table)):
        title = table[i].get('title')\
            .replace(", Inc.", "")\
            .replace(" Inc.", "")\
            .replace(" Group", "")\
            .replace(" Company", "")\
            .replace(" Common Stock", "")\
            .replace(" Holdings", "")

        stock_dict = {
            'ticker': table[i].contents[0],
            'url': "https://finance.yahoo.com" + table[i].get('href'),
            'title': title,
            'current_price': table_2[i].find('fin-streamer').get('value')
        }

        trending_stocks_list.append(stock_dict)

    return trending_stocks_list
