from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import os

sia = SentimentIntensityAnalyzer()

file_path = "../Thesis-Source-Code/Data_Collection/CSV_Results/"

csvs = [f for f in os.listdir("../Thesis-Source-Code/Data_Collection/CSV_Results/") if f.endswith("csv")]

print(csvs)

for csv in csvs:
    csv_df = pd.read_csv(file_path + csv)
    csv_df["polarity"] = ""

    for index, row in csv_df.iterrows():
        text = row[csv_df.columns[0]]
        scores = sia.polarity_scores(text)  # print 'scores' object to see all of the fields offered
        row["polarity"] = scores["compound"]  # compound field shows a holistic view of the derived sentiment

    print(csv_df.head)

    file_name = csv.split(".")[0] + "_+_polarity"

    csv_df.to_csv(f"../Thesis-Source-Code/nlp_poc/csvs_with_polarity/{file_name}.csv")

##############################################################
# TODO:
#   - Polish the scrapers to include punctuation and capitalization
#   - Work on getting the sentiment in a better way
#   - Start looking at what a weighted average would look like
#   - Determine a way to factor in the Analyst Ratings data as well
##############################################################




