import pandas as pd
import os

####################################################################
# TODO:
#   - Develop model whose predictions line up with Analyst Ratings
#       - X Values are the polarities (polarity_csv)
#       - Y values are analyst ratings
#       - Must find a multiclass classification model
####################################################################


def get_data():
    """
    Returns the training data set required for the model development.
    """

    polarity_csv = pd.read_csv('../Polarity_Analysis/aggregated_polarities.csv', index_col=0)
    print(polarity_csv)  # Input of training data set
    print()

    file_path = "../Data_Collection/Analyst_Ratings/"
    all_csv_results = [f for f in os.listdir("../Data_Collection/Analyst_Ratings/") if f.endswith("csv")]

    for csv in all_csv_results:
        ticker_analyst_csv = pd.read_csv(file_path + csv)
        print(ticker_analyst_csv)  # "Output" of training data set


def main():
    get_data()


if __name__ == "__main__":
    main()
