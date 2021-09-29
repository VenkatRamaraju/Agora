#!/usr/bin/env python3

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Sets up the dictionary that NLTK will use to judge polarities.
"""

# Libraries and Dependencies
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import pandas as pd
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('wordnet')

sia = SentimentIntensityAnalyzer()

cols = ['word']
positive_df = pd.read_csv('setup_csvs/loughran_mcdonald_positive_words.csv', names=cols, header=None,
                          delim_whitespace=True)
positive_df["polarity"] = ""

negative_df = pd.read_csv('setup_csvs/loughran_mcdonald_negative_words.csv', names=cols, header=None,
                          delim_whitespace=True)
negative_df["polarity"] = ""


for index, row in positive_df.iterrows():
    word = row["word"].lower()
    row["word"] = word
    row["polarity"] = 2

for index, row in negative_df.iterrows():
    word = row["word"].lower()
    row["word"] = word
    row["polarity"] = -2

print(positive_df)
print(negative_df)

overall_df = positive_df.append(negative_df)
overall_df.to_csv('setup_csvs/polarized_stock_lex.csv')


