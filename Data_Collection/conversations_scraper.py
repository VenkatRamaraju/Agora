# Libraries and Dependencies
from headlines_scraper import *


def get_yahoo_conversations(stock):
    request = 'https://finance.yahoo.com/quote/' + stock + '/community?p=' + stock
    opinions = get_soup(request, 'div', 'C($c-fuji-grey-l) Mb(2px) Fz(14px) Lh(20px) Pend(8px)')
    return create_array(opinions)


def main():
    # Stock Ticker
    stock = 'AAPL'
    print("\nFetching conversations for " + stock + "...\n")

    # List of sources
    source_1 = np.array(get_yahoo_conversations(stock))

    # Combining all sources, initializing data frame
    overall_conversations = list(np.concatenate(source_1, axis=None))
    output(overall_conversations, stock)


if __name__ == "__main__":
    main()
