import pandas as pd

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
    print(polarity_csv)


def main():
    get_data()


if __name__ == "__main__":
    main()