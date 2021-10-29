from bs4 import BeautifulSoup
import requests


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

