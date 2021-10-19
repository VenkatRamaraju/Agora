import requests
import pprint
import re


def get_last_price(ticker):
    url = "http://feeds.financialcontent.com/JSQuote?Ticker=" + ticker
    stuff = requests.get(url).text
    print(stuff)

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

    color = ""

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

    pprint.pprint(stock_dict)

    return stock_dict


# pprint.pprint(get_last_price("AAPL"))