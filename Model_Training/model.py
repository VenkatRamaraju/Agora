import pandas as pd
import yfinance as yf
import os
import glob
import pprint
from collections import Counter


####################################################################
# TODO:
#   - Develop model whose predictions line up with Analyst Ratings
#       - X Values are the polarities (polarity_csv)
#       - Y values are analyst ratings
#       - Must find a multiclass classification model
####################################################################


def liquidity(current_assets, current_liabilites):
    return current_assets / current_liabilites


def roe(net_income, common_equity):
    return net_income / common_equity


def roic(ebit, tax_provision, invested_capital):
    return (ebit - tax_provision) / invested_capital


def get_yf_data():
    """
    Returns the training data set required for the model development.
    """

    df = pd.read_csv('../Polarity_Analysis/aggregated_polarities.csv', index_col=0)
    # new_columns = ['payoutRatio', 'beta', 'regularMarketVolume', 'profitMargins', '52WeekChange',
    #                'forwardEps', 'bookValue', 'sharesShort', 'sharesPercentSharesOut', 'trailingEps',
    #                'heldPercentInstitutions', 'heldPercentInsiders', 'mostRecentQuarter', 'nextFiscalYearEnd',
    #                'shortRatio', 'enterpriseValue', 'earningsQuarterlyGrowth', 'sharesShortPriorMonth',
    #                'shortPercentOfFloat', 'pegRatio']

    df = df[df.Ticker != 'PLTR']
    new_columns = ['liquidityRatio', 'ROE', 'shortRatio']

    df = df.reindex(columns=df.columns.tolist() + new_columns)

    for column in new_columns:
        df[column] = 0.0

    for index, row in df.iterrows():
        ticker = yf.Ticker(row['Ticker'])
        print("Determining Liquidity ratio, ROE, and Short Ratio for:", row['Ticker'])
        balance_sheet = ticker.quarterly_balance_sheet.reset_index()
        financials = ticker.quarterly_financials.reset_index()
        ticker_info = ticker.get_info()

        current_assets_index = balance_sheet.index[balance_sheet['index'] == 'Total Current Assets'].tolist()[0]
        current_liabilities_index = balance_sheet.index[balance_sheet['index'] ==
                                                        'Total Current Liabilities'].tolist()[0]
        common_equity_index = balance_sheet.index[balance_sheet['index'] == 'Total Stockholder Equity'].tolist()[0]

        current_assets = balance_sheet.iloc[current_assets_index, 1]
        current_liabilities = balance_sheet.iloc[current_liabilities_index, 1]
        common_equity = balance_sheet.iloc[common_equity_index, 1]

        net_income_index = financials.index[financials['index'] == 'Net Income'].tolist()[0]
        net_income = financials.iloc[net_income_index, 1]

        liq = liquidity(current_assets, current_liabilities)
        ret_on_equity = roe(net_income, common_equity)

        df.at[index, 'liquidityRatio'] = liq
        df.at[index, 'ROE'] = ret_on_equity
        df.at[index, 'shortRatio'] = ticker_info['shortRatio']

    print("\n\n", df)

    df.to_csv('training_data_v2.csv')


def organize_analyst_ratings():
    """
    Normalizes Analyst Ratings --> the "y" data in our KNN model; returns the determined rating (highest frequency)
    as a dictionary with the corresponding ticker
    """

    analyst_dfs = {}

    # read in the CSVs, perform normalization of rating column
    for file in glob.glob('../Data_Collection/Analyst_Ratings/*.csv'):
        temp_df = pd.read_csv(file, na_filter=False)
        ticker = os.path.basename(file).partition('.csv')
        temp_df["Rating"] = temp_df["Rating"].apply(lambda x: x.lower())
        temp_df = normalize_ratings(df=temp_df)

        analyst_dfs[ticker[0]] = temp_df

    determined_ratings = {}

    # determine the most common rating provided by analyst
    for ticker, df in analyst_dfs.items():
        ratings = list(df["normalized_rating"])
        r_count = Counter(ratings)
        most_common = r_count.most_common(1)
        determined_ratings[ticker] = most_common[0][0]
        # print(ticker + ":", most_common[0][0])

    return determined_ratings


def normalize_ratings(df):
    """
    Adds the "normalized_rating" column to a given ticker dataframe
    """
    sell_ratings = ["sell"]
    underperform_ratings = ["market perform - under perform", "underperform", "underweight"]
    hold_ratings = ["equal weight", "equal-weight", "equal weight - overweight", "hold", "in-line",
                    "market perform", "neutral", "neutral - overweight", "outperform - sector perform",
                    "overweight", "peer perform", "positive - neutral", "perform", "positive - sector perform",
                    "sector perform", "sell - overweight"]
    outperform_ratings = ["buy - conviction-buy", "buy - hold", "buy - overweight", "hold - buy", "in-line - buy"
                          "neutral - buy", "outperform", "positive - buy", "positive - overweight",
                          "top pick - outperform"]
    buy_ratings = ["buy"]

    present_cols = list(df)

    df = df.reindex(columns=present_cols + ["normalized_rating"])

    for index, row in df.iterrows():
        rating = row["Rating"]
        if rating in sell_ratings:
            df.loc[index, "normalized_rating"] = "sell"
        elif rating in underperform_ratings:
            df.loc[index, "normalized_rating"] = "underperform"
        elif rating in hold_ratings:
            df.loc[index, "normalized_rating"] = "hold"
        elif rating in outperform_ratings:
            df.loc[index, "normalized_rating"] = "outperform"
        elif rating in buy_ratings:
            df.loc[index, "normalized_rating"] = "buy"

    return df


def main():
    get_yf_data()
    print("\n\nAnalyst Ratings for each company:")
    pprint.pprint(organize_analyst_ratings())


if __name__ == "__main__":
    main()
