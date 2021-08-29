#!/usr/bin/env python3

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Generates and aggregates polarities across headlines and conversations
"""

# Libraries and Dependencies
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from nltk.stem import WordNetLemmatizer

# Global Variables
sia = SentimentIntensityAnalyzer()
lemmatizer = WordNetLemmatizer()
conversations_map = {}
headlines_map = {}


def update_stock_terminology():
    """
    Creates dictionary with updated terminologies for SentimentIntensityAnalyzer. Includes positive and negative words,
    along with polarized words with weights. Used to improve VADER accuracy.
    """
    stock_lexicon = {}
    csv_df = pd.read_csv('setup_csvs/new_stock_lex.csv')
    for index, row in csv_df.iterrows():
        stock_lexicon[row['Item']] = row['Polarity']

    csv_df = pd.read_csv('setup_csvs/modified_stock_lex.csv')
    for index, row in csv_df.iterrows():
        stock_lexicon[row['Word']] = row['Polarity']

    resulting_lex = {}
    resulting_lex.update(stock_lexicon)
    resulting_lex.update(sia.lexicon)
    sia.lexicon = resulting_lex


def get_headline_sentiments():
    """
    Analyze polarities of the given stock tickers, based on terminologies inserted in SentimentIntensityAnalyzer.
    Prints out the aggregated results to CSV.
    """
    headlines_csv = pd.read_csv("../Data_Collection/Headlines.csv")
    sum_of_polarities = {}
    count_of_headlines = {}

    for index, row in headlines_csv.iterrows():
        lemma_text = lemmatizer.lemmatize(row['Headline'])
        scores = sia.polarity_scores(lemma_text)
        row["Polarity"] = scores["compound"]

        if row['Ticker'] not in sum_of_polarities:
            sum_of_polarities[row['Ticker']] = scores["compound"]
            count_of_headlines[row['Ticker']] = 1
        else:
            sum_of_polarities[row['Ticker']] = sum_of_polarities[row['Ticker']] + scores["compound"]
            count_of_headlines[row['Ticker']] = count_of_headlines[row['Ticker']] + 1

    for ticker in sum_of_polarities:
        headlines_map[ticker] = sum_of_polarities[ticker]/count_of_headlines[ticker]


def generate_aggregated_csv():
    """
    Generates a CSV with the aggregated polarities of headlines and conversations for the group of stocks that are
    being analyzed.
    """
    aggregated_df = pd.DataFrame(columns=["Ticker", "Conversations", "Headlines"])

    for ticker, headlines_polarity in headlines_map.items():
        row = {"Ticker": ticker, "Conversations": conversations_map[ticker], "Headlines": headlines_polarity}
        aggregated_df = aggregated_df.append(row, ignore_index=True)

    aggregated_df.to_csv("aggregated_polarities.csv")


def get_conversation_sentiments():
    list_of_conversations = [f for f in os.listdir('../Data_Collection/Conversations/') if f.endswith('.csv')]
    sum_of_polarities = {}
    count_of_conversations = {}

    for ticker_csv in list_of_conversations:
        conversations_csv = pd.read_csv('../Data_Collection/Conversations/' + str(ticker_csv))
        ticker = ticker_csv.split("_")[0].upper()
        for index, row in conversations_csv.iterrows():
            lemma_text = lemmatizer.lemmatize(row['Conversation'])
            scores = sia.polarity_scores(lemma_text)
            row["Polarity"] = scores["compound"]

            if ticker not in sum_of_polarities:
                sum_of_polarities[ticker] = scores["compound"]
                count_of_conversations[ticker] = 1
            else:
                sum_of_polarities[ticker] = sum_of_polarities[ticker] + scores["compound"]
                count_of_conversations[ticker] = count_of_conversations[ticker] + 1

        conversations_map[ticker] = sum_of_polarities[ticker]/count_of_conversations[ticker]


def main():
    update_stock_terminology()
    get_headline_sentiments()
    get_conversation_sentiments()
    generate_aggregated_csv()


if __name__ == "__main__":
    main()
