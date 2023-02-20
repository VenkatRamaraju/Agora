#!/usr/bin/env python3

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Leverages the pickled RandomForestClassifier to generate a new set of improved predictions on the dataset.
"""

import pandas as pd
import pickle
import numpy as np


def generate_improved_prediction():
    df = pd.read_csv('final_dataset.csv', index_col=0)
    training_df = df.dropna()
    training_df = training_df.drop(['Unnamed: 0.1', 'Symbol', 'beta', 'profitMargins','Name', 'Buy', 'Analyst', 'agora_pred'],
                          axis=1)
    pickled_model = pickle.load(open('improved_models/RF_pickled_final_df.pkl', 'rb'))

    predictions = pickled_model.predict(training_df)
    predictions_index = 0
    df['Improved Agora Predictions'] = None

    for index, row in df.iterrows():
        all_present = True
        for column in df.columns:
            if pd.isna(row[column]) and column != 'Improved Agora Predictions':
                all_present = False
                break

        if all_present:
            df.loc[index,'Improved Agora Predictions'] = predictions[predictions_index]
            predictions_index += 1

    df.to_csv('improved_models/final_dataset_improved_predictions.csv')


def main():
    generate_improved_prediction()


if __name__ == "__main__":
    main()