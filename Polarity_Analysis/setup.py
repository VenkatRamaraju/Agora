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

# Initializing data
sia = SentimentIntensityAnalyzer()

cols = ['word']
positive_df = pd.read_csv('setup_csvs/loughran_mcdonald_positive_words.csv', names=cols, header=None,
                          delim_whitespace=True)
positive_df["polarity"] = ""

negative_df = pd.read_csv('setup_csvs/loughran_mcdonald_negative_words.csv', names=cols, header=None,
                          delim_whitespace=True)
negative_df["polarity"] = ""

# Populating CSV with +/- 2 polarities for modified sentiment analysis model
for index, row in positive_df.iterrows():
    word = row["word"].lower()
    row["word"] = word
    row["polarity"] = 2

for index, row in negative_df.iterrows():
    word = row["word"].lower()
    row["word"] = word
    row["polarity"] = -2

overall_df = positive_df.append(negative_df)
overall_df.to_csv('setup_csvs/polarized_stock_lex.csv')


