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

# words = pd.DataFrame(columns=['Text', 'Polarity'])
# csv_df = pd.read_csv('setup_csvs/stock_lex.csv')
# csv_df["Polarity"] = (csv_df['Aff_Score'] + csv_df['Neg_Score'])/2
# csv_df.drop(['Aff_Score', 'Neg_Score', 'POS'], axis=1, inplace=True)
# csv_df.to_csv('setup_csvs/new_stock_lex.csv', index=False)
#
# positive_df = pd.read_excel('setup_csvs/WordLists.xlsx', sheet_name='Positive', header=None, index_col=False)
# positive_df.rename(columns={positive_df.columns[0]: 'Word'}, inplace=True)
# positive_df["Polarity"] = ""
#
# negative_df = pd.read_excel('setup_csvs/WordLists.xlsx', sheet_name='Negative', header=None, index_col=False)
# negative_df.rename(columns={negative_df.columns[0]: 'Word'}, inplace=True)
# negative_df["Polarity"] = ""

sia = SentimentIntensityAnalyzer()

cols = ['word']
positive_df = pd.read_csv('setup_csvs/loughran_mcdonald_positive_words.csv', names=cols, header=None,
                          delim_whitespace=True)
positive_df["polarity"] = ""

negative_df = pd.read_csv('setup_csvs/loughran_mcdonald_negative_words.csv', names=cols, header=None,
                          delim_whitespace=True)
negative_df["polarity"] = ""

# positive = positive_df['word'].to_list()
# negative = negative_df['word'].to_list()
#
# custom_lex =
#
# for word in positive:
#     custom_lex.update({word: 2})
# for word in negative:
#     custom_lex.update({word: -2})

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


# for index, row in positive_df.iterrows():
#     text = row[positive_df.columns[0]].lower()
#     row[positive_df.columns[0]] = text
#     row["Polarity"] = 1
#
# for index, row in negative_df.iterrows():
#     text = row[negative_df.columns[0]].lower()
#     row[negative_df.columns[0]] = text
#     row["Polarity"] = -1
#
#
# overall_df = positive_df.append(negative_df)
# overall_df.to_csv('setup_csvs/modified_stock_lex.csv', index=False)


