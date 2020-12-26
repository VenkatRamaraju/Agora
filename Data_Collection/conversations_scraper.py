# Libraries and Dependencies
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def cleanup(line):
    cleaned_text = str.maketrans('', '', r"-()\"#/@;:<>{}-=~|.?,")
    line = line.translate(cleaned_text)

    return str(line).lower()


def get_soup(request, element, class_value):
    html_page = requests.get(request).text
    soup = BeautifulSoup(html_page, 'lxml')
    return soup.find_all(element, class_=class_value)


def create_conversation_array(conversation_list):
    list_of_conversations = []
    for li in conversation_list:
        list_of_conversations.append(li.text)  # Gets the text from HTML

    return list_of_conversations


def get_yahoo_conversations(stock):
    request = 'https://finance.yahoo.com/quote/' + stock + '/community?p=' + stock
    opinions = get_soup(request, 'div', 'C($c-fuji-grey-l) Mb(2px) Fz(14px) Lh(20px) Pend(8px)')
    return create_conversation_array(opinions)


def format_to_table(conversations, stock):
    title = 'Recent conversations for ' + stock
    opinion_table = pd.DataFrame(columns=[title])

    for line in conversations:
        opinion_table = opinion_table.append({title: cleanup(line)}, ignore_index=True)

    return opinion_table


def main():
    # Stock Ticker
    stock = 'NFLX'
    print("\nFetching conversations for " + stock + "...\n")
    title = 'Recent conversations for ' + stock

    # List of sources
    source_1 = np.array(get_yahoo_conversations(stock))
    overall_conversations = list(np.concatenate(source_1, axis=None))
    opinion_table = pd.DataFrame(columns=[title])

    # Formatting to a table
    if len(source_1) != 0:
        opinion_table = format_to_table(overall_conversations, stock)
    else:
        print("Invalid ticker or no conversations available.")

    opinion_table.drop_duplicates(subset=title, keep=False, inplace=True)
    print(opinion_table)


if __name__ == "__main__":
    main()
