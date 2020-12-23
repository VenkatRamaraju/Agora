# Libraries and Dependencies
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def cleanup(line):
    cleaned_text = str.maketrans('', '', r"-()\"#/@;:<>{}-=~|.?,")
    line = line.translate(cleaned_text)

    return str(line).lower()


def get_yahoo_conversations(stock):
    html_page = requests.get('https://finance.yahoo.com/quote/' + stock + '/community?p=' + stock).text
    soup = BeautifulSoup(html_page, 'lxml')
    opinions = soup.find_all('div', class_='C($c-fuji-grey-l) Mb(2px) Fz(14px) Lh(20px) Pend(8px)')
    list_of_conversations = []

    for opinion in opinions:
        list_of_conversations.append(opinion.text)

    return list_of_conversations


def format_to_table(conversations, stock):
    title = 'Recent conversations for ' + stock
    opinion_table = pd.DataFrame(columns=[title])

    for line in conversations:
        opinion_table = opinion_table.append({title: cleanup(line)}, ignore_index=True)

    return opinion_table


def main():
    # Stock Ticker
    stock = 'BABA'
    print("\nFetching conversations for " + stock + "...\n")
    title = 'Recent conversations for ' + stock

    # List of sources
    source_1 = np.array(get_yahoo_conversations(stock))
    overall_conversations = np.concatenate(source_1, axis=None)
    overall_conversations = list(overall_conversations)
    opinion_table = pd.DataFrame(columns=[title])

    # Formatting to a table
    if len(source_1) != 0:
        opinion_table = format_to_table(source_1, stock)
    else:
        print("Invalid ticker or no conversations available.")

    print(opinion_table)


if __name__ == "__main__":
    main()
