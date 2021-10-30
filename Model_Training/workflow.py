import pandas as pd
import numpy as np
import yfinance as yf
import pickle
pd.set_option("display.max_rows", None, "display.max_columns", None)


aggregated_polarities = pd.read_csv("../Polarity_Analysis/aggregated_polarities.csv")
all_companies_data = pd.read_csv("output_csvs/final_db.csv")


def merge_polarities_with_all_stocks():
    # append headline and convo polarity columns
    global aggregated_polarities
    global all_companies_data

    all_companies_data["headline_polarity"] = np.nan
    all_companies_data["convo_polarity"] = np.nan

    for index, row in aggregated_polarities.iterrows():
        company_row = all_companies_data.loc[all_companies_data["Symbol"] == row["Ticker"]]

        all_companies_data["headline_polarity"][company_row.index.item()] = round(row["Headlines"], 2)
        all_companies_data["convo_polarity"][company_row.index.item()] = round(row["Conversations"], 2)


def fetch_metrics_for_all_stocks():
    # generate ticker stock metrics for all tickers in all_companies_data (~4400)
    global all_companies_data

    stock_metric_data = pd.read_csv("output_csvs/stock_metric_data.csv")

    metrics = ['beta', 'profitMargins', 'forwardEps', 'bookValue', 'heldPercentInstitutions',
               'shortRatio', 'shortPercentOfFloat']

    all_companies_data = all_companies_data.reindex(columns=all_companies_data.columns.tolist() + metrics)

    for index, row in stock_metric_data.iterrows():
        company_row = all_companies_data.loc[all_companies_data["Symbol"] == row["Symbol"]]

        all_companies_data["beta"][company_row.index.item()] = row["beta"]
        all_companies_data["profitMargins"][company_row.index.item()] = row["profitMargins"]
        all_companies_data["forwardEps"][company_row.index.item()] = row["forwardEps"]
        all_companies_data["bookValue"][company_row.index.item()] = row["bookValue"]
        all_companies_data["heldPercentInstitutions"][company_row.index.item()] = row["heldPercentInstitutions"]
        all_companies_data["shortRatio"][company_row.index.item()] = row["shortRatio"]
        all_companies_data["shortPercentOfFloat"][company_row.index.item()] = row["shortPercentOfFloat"]


def generate_predictions():
    global all_companies_data

    training_rows = all_companies_data[~all_companies_data['headline_polarity'].isnull() &
                                       ~all_companies_data['convo_polarity'].isnull()]

    del training_rows['Unnamed: 0']
    del training_rows['Name']
    del training_rows['Analyst']

    all_companies_data["agora_pred"] = np.nan

    training_rows = training_rows.dropna()

    # load the pre-trained model
    lr_model = pickle.load(open('pickle_model.sav', 'rb'))

    training_rows['headline_polarity'] = training_rows['headline_polarity'] * 2
    training_rows['convo_polarity'] = training_rows['convo_polarity'] * 2

    x_total = training_rows[[x for x in training_rows.columns if x not in ['Buy', 'Symbol']]]

    # get the predictions for all stocks with headlines/convos
    predictions = lr_model.predict(x_total)

    training_rows["agora_pred"] = predictions

    # append to the full dataset
    for index, row in training_rows.iterrows():
        company_row = all_companies_data.loc[all_companies_data["Symbol"] == row["Symbol"]]
        all_companies_data["agora_pred"][company_row.index.item()] = row["agora_pred"]


def main():
    global all_companies_data
    # take aggregated_polarities.csv from /Polarity_Analysis/ and append to overall company list
    merge_polarities_with_all_stocks()
    # fetch the stock metrics for each of the stocks (~4400) with yahoo finance
    fetch_metrics_for_all_stocks()
    # at this point, all_companies_data should have the 7 stock metrics + headline/convo polarities
    # generate ML predictions for the tickers that have headline/convo polarities
    generate_predictions()

    all_companies_data.to_csv("final_dataset.csv")


if __name__ == "__main__":
    main()
