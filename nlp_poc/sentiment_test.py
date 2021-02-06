from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import os

##############################################################
# TODO:
#   - Work on getting the sentiment in a better way
#   - Start looking at what a weighted average would look like
##############################################################

sia = SentimentIntensityAnalyzer()


def get_sentiments():
    file_path = "../Data_Collection/CSV_Results/"
    
    all_csv_results = [f for f in os.listdir("../Data_Collection/CSV_Results/") if f.endswith("csv")]
    
    for csv in all_csv_results:
        csv_df = pd.read_csv(file_path + csv)
        csv_df["polarity"] = ""

        avg = 0.0
        rows = 0

        positive = 0
        zero = 0
        negative = 0

        for index, row in csv_df.iterrows():
            text = row[csv_df.columns[0]]
            scores = sia.polarity_scores(text)  # print 'scores' object to see all of the fields offered
            row["polarity"] = scores["compound"]  # compound field shows a holistic view of the derived sentiment
            if scores["compound"] == 0.0:
                zero += 1
            elif scores["compound"] > 0.0:
                positive += 1
            else:
                negative += 1

            avg += scores["compound"]
            rows += 1

        print(csv.split(".")[0].split("_")[0], csv.split(".")[0].split("_")[1])
        file_name = csv.split(".")[0] + "_+_polarity"
    
        csv_df.to_csv(f"../nlp_poc/csvs_with_polarity/{file_name}.csv")

        print("Average: ", avg/rows)
        print("Positive: ", positive)
        print("Negative: ", negative)
        print("Zero: ", zero)
        print()


def main():
    get_sentiments()


if __name__ == "__main__":
    main()


