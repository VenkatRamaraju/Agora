import os
import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns", None)


def main():
    master_df = pd.DataFrame(columns=['Symbol', 'Name', 'Last Sale', 'Net Change', '% Change', 'Market Cap',
                                      'Country', 'IPO Year', 'Volume', 'Sector', 'Industry', 'Buy'])
    companies_df = pd.DataFrame(columns=['Symbol', 'Company'])

    files = [f for f in os.listdir('Stocks') if f.endswith('.csv')]
    for file in files:
        df = pd.read_csv('Stocks/' + file)

        if file == 'buy.csv':
            df['Buy'] = 1
        elif file == 'sell.csv':
            df['Buy'] = 0
        elif file == 'strong_buy.csv':
            df['Buy'] = 1
        elif file == 'strong_sell.csv':
            df['Buy'] = 0
        elif file == 'hold.csv':
            df['Buy'] = 0

        for index, row in df.iterrows():
            row['Last Sale'] = float(str(row['Last Sale'])[1:])
            row['% Change'] = float(str(row['% Change'])[:-1])
            master_df = master_df.append(row, ignore_index=True)
            companies_df = companies_df.append({"Symbol": row['Symbol'], "Company": row['Name']}, ignore_index=True)

    master_df.to_csv('modified_training_dataset.csv', index=False)
    companies_df.to_csv('companies.csv', index=False)


if __name__ == "__main__":
    main()