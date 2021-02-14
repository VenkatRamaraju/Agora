import nltk
import pandas as pd
nltk.download('vader_lexicon')
nltk.download('punkt')

words = pd.DataFrame(columns=['Text', 'Polarity'])
csv_df = pd.read_csv('stock_lex.csv')
csv_df["Polarity"] = (csv_df['Aff_Score'] + csv_df['Neg_Score'])/2
csv_df.drop(['Aff_Score', 'Neg_Score', 'POS'], axis=1, inplace=True)
csv_df.to_csv('new_stock_lex.csv', index=False)
