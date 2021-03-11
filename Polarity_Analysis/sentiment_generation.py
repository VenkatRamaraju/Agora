from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import os
from nltk.stem import WordNetLemmatizer

# Global Variables
sia = SentimentIntensityAnalyzer()
lemmatizer = WordNetLemmatizer()


def update_stock_terminology():
    """
    Creates dictionary with updated terminologies for SentimentIntensityAnalyzer. Includes positive and negative words,
    along with polarized words with weights. Used to improve VADER accuracy
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


def get_sentiments():
    """
    Analyze polarities of the given stock tickers, based on  terminologies inserted in SentimentIntensityAnalyzer.
    Prints out the aggregated results to CSV.
    """
    file_path = "../Data_Collection/CSV_Results/"
    conversations_map = {}
    headlines_map = {}
    all_csv_results = [f for f in os.listdir("../Data_Collection/CSV_Results/") if f.endswith("csv")]

    for csv in all_csv_results:
        csv_df = pd.read_csv(file_path + csv)
        csv_df["Polarity"] = ""
        avg = 0.0
        rows = 0

        for index, row in csv_df.iterrows():
            lemma_text = lemmatizer.lemmatize(row[csv_df.columns[0]])
            scores = sia.polarity_scores(lemma_text)
            row["Polarity"] = scores["compound"]  # compound field shows a holistic view of the derived sentiment

            avg += row["Polarity"]
            rows += 1

        file_name = csv.split(".")[0] + "_+_polarity"
        csv_df.to_csv(f"../Polarity_Analysis/csvs_with_polarity/{file_name}.csv")
        ticker = csv.split(".")[0].split("_")[0]
        category = csv.split(".")[0].split("_")[1]
        polarity = round(avg/rows, 3)

        if category == "headlines":
            headlines_map[ticker] = polarity
        else:
            conversations_map[ticker] = polarity

    return headlines_map, conversations_map


def generate_aggregated_csv(headlines_map, conversations_map):
    """
    Generates a CSV with the aggregated polarities of headlines and conversations for the group of stocks that are
    being analyzed.
    """
    aggregated_df = pd.DataFrame(columns=["Ticker", "Conversations", "Headlines"])

    for ticker, headlines_polarity in headlines_map.items():
        row = {"Ticker": ticker, "Conversations": conversations_map[ticker], "Headlines": headlines_polarity}
        aggregated_df = aggregated_df.append(row, ignore_index=True)

    aggregated_df.to_csv("aggregated_polarities.csv")


def main():
    update_stock_terminology()
    headlines_map, conversations_map = get_sentiments()
    generate_aggregated_csv(headlines_map, conversations_map)


if __name__ == "__main__":
    main()
