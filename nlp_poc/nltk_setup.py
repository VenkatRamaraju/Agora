from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import pandas as pd
nltk.download('vader_lexicon')
nltk.download('punkt')

words = pd.DataFrame(columns=['Text', 'Polarity'])
csv_df = pd.read_csv('stock_lex.csv')
csv_df["Polarity"] = (csv_df['Aff_Score'] + csv_df['Neg_Score'])/2
csv_df.drop(['Aff_Score', 'Neg_Score', 'POS'], axis=1, inplace=True)
csv_df.to_csv('new_stock_lex.csv', index=False)

positive_df = pd.read_excel('WordLists.xlsx', sheet_name='Positive', header=None, index_col=False)
positive_df.rename(columns={positive_df.columns[0]: 'Word'}, inplace=True)
positive_df["Polarity"] = ""

negative_df = pd.read_excel('WordLists.xlsx', sheet_name='Negative', header=None, index_col=False)
negative_df.rename(columns={negative_df.columns[0]: 'Word'}, inplace=True)
negative_df["Polarity"] = ""

sia = SentimentIntensityAnalyzer()

for index, row in positive_df.iterrows():
    text = row[positive_df.columns[0]].lower()
    row[positive_df.columns[0]] = text
    row["Polarity"] = 1

for index, row in negative_df.iterrows():
    text = row[negative_df.columns[0]].lower()
    row[negative_df.columns[0]] = text
    row["Polarity"] = -1


overall_df = positive_df.append(negative_df)
overall_df.to_csv('modified_stock_lex.csv', index=False)


